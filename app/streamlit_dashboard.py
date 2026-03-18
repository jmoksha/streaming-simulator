"""
Interactive Streamlit Dashboard for Streaming Platform Engagement Simulator
Author: Data Scientist
Date: 2024

A comprehensive, production-grade dashboard for modeling and analyzing user
behavior using Markov chains and stochastic processes.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.markov_model import MarkovChainModel, DEFAULT_TRANSITION_MATRIX
from src.simulation import SimulationEngine, EnhancedSimulationEngine
from src.visualization import (
    MarkovChainVisualizer, 
    SimulationVisualizer,
    create_interactive_dashboard
)


# Page config
st.set_page_config(
    page_title="Streaming Platform Simulator",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "markov_chain" not in st.session_state:
        st.session_state.markov_chain = MarkovChainModel(DEFAULT_TRANSITION_MATRIX)
    
    if "simulation_result" not in st.session_state:
        st.session_state.simulation_result = None
    
    if "transition_matrix" not in st.session_state:
        st.session_state.transition_matrix = DEFAULT_TRANSITION_MATRIX.copy()


def render_sidebar():
    """Render sidebar with controls."""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Simulation parameters
        st.subheader("📊 Simulation Parameters")
        
        n_users = st.slider(
            "Initial Number of Users",
            min_value=100,
            max_value=10000,
            value=1000,
            step=100,
            help="Number of users to simulate"
        )
        
        n_steps = st.slider(
            "Number of Time Steps",
            min_value=10,
            max_value=200,
            value=50,
            step=5,
            help="Duration of simulation"
        )
        
        # Poisson arrivals
        st.subheader("🚀 Poisson Arrivals (Optional)")
        
        use_arrivals = st.checkbox(
            "Enable New User Arrivals",
            value=False,
            help="Add Poisson process for new users"
        )
        
        lambda_rate = 0
        if use_arrivals:
            lambda_rate = st.slider(
                "Arrival Rate (λ) - Users per Step",
                min_value=0.0,
                max_value=100.0,
                value=10.0,
                step=1.0,
                help="Rate parameter for Poisson process"
            )
        
        # Transition matrix editor
        st.subheader("🔄 Transition Probabilities")
        
        edit_mode = st.radio(
            "Edit Mode",
            options=["View Only", "Advanced Edit"],
            help="Select how to modify transition probabilities"
        )
        
        transition_data = {}
        state_names = ["Visitor", "Browsing", "Watching", "Binge Watching", "Subscriber", "Churn"]
        
        if edit_mode == "Advanced Edit":
            st.info("Use the matrix editor to modify transition probabilities. Each row must sum to 1.")
            
            # Create editable matrix
            cols = st.columns(6)
            for j in range(6):
                cols[j].write(f"**→ {state_names[j][:4]}**")
            
            matrix_values = []
            for i in range(6):
                st.write(f"**{state_names[i]}**")
                row = st.columns(6)
                row_values = []
                
                for j in range(6):
                    value = row[j].number_input(
                        f"P({i},{j})",
                        min_value=0.0,
                        max_value=1.0,
                        value=float(st.session_state.transition_matrix[i, j]),
                        step=0.01,
                        label_visibility="collapsed"
                    )
                    row_values.append(value)
                
                # Check row sum
                row_sum = sum(row_values)
                if not np.isclose(row_sum, 1.0, atol=0.01):
                    st.warning(f"Row {i} sum: {row_sum:.3f} (should be 1.0)")
                
                matrix_values.append(row_values)
            
            custom_matrix = np.array(matrix_values)
            
            if st.button("✅ Apply Custom Matrix"):
                try:
                    test_chain = MarkovChainModel(custom_matrix)
                    st.session_state.transition_matrix = custom_matrix
                    st.session_state.markov_chain = test_chain
                    st.success("✓ Matrix applied successfully!")
                except ValueError as e:
                    st.error(f"❌ Invalid matrix: {str(e)}")
        
        # Quick adjustments
        st.subheader("⚡ Quick Adjustments")
        
        adjustment_type = st.selectbox(
            "Select Adjustment",
            options=[
                "None",
                "Increase Trial→Subscriber",
                "Decrease Churn Rate",
                "Increase Engagement",
                "Aggressive Conversion"
            ]
        )
        
        if st.button("🎯 Apply Adjustment"):
            adjusted_matrix = st.session_state.transition_matrix.copy()
            
            if adjustment_type == "Increase Trial→Subscriber":
                # Increase visitor -> subscriber
                adjusted_matrix[0, 4] = min(0.15, adjusted_matrix[0, 4] + 0.05)
                adjusted_matrix[0, 0] -= 0.05
                adjusted_matrix[0, 0] = max(0, adjusted_matrix[0, 0])
            
            elif adjustment_type == "Decrease Churn Rate":
                # Reduce churn from all states
                for i in range(5):
                    adjusted_matrix[i, 5] *= 0.5
                    # Redistribute to subscriber or binge watching
                    diff = adjusted_matrix[i, 5] / 2
                    adjusted_matrix[i, 4] = min(1.0, adjusted_matrix[i, 4] + diff)
            
            elif adjustment_type == "Increase Engagement":
                # Move users toward watching/binge watching
                for i in range(4):
                    adjusted_matrix[i, 3] += 0.05
                    adjusted_matrix[i, 0] = max(0, adjusted_matrix[i, 0] - 0.03)
            
            elif adjustment_type == "Aggressive Conversion":
                # Optimize for subscriber conversion
                for i in range(4):
                    adjusted_matrix[i, 4] = min(1.0, adjusted_matrix[i, 4] * 1.5)
                    adjusted_matrix[i, 5] *= 0.5
                    total = adjusted_matrix[i].sum()
                    if total > 1.0:
                        adjusted_matrix[i] /= total
            
            # Normalize rows
            for i in range(6):
                row_sum = adjusted_matrix[i].sum()
                if row_sum > 0:
                    adjusted_matrix[i] /= row_sum
            
            try:
                test_chain = MarkovChainModel(adjusted_matrix)
                st.session_state.transition_matrix = adjusted_matrix
                st.session_state.markov_chain = test_chain
                st.success(f"✓ {adjustment_type} applied!")
            except ValueError as e:
                st.error(f"❌ Adjustment failed: {str(e)}")
        
        return n_users, n_steps, lambda_rate, use_arrivals


def render_metrics_section(metrics: dict):
    """Render key metrics in columns."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Users",
            f"{metrics['total_users']:,}",
            help="Total users in simulation"
        )
        st.metric(
            "Subscribers",
            f"{metrics['final_subscribers']:,}",
            help="Paid subscribers at end"
        )
    
    with col2:
        st.metric(
            "Conversion Rate",
            f"{metrics['subscriber_conversion_rate']:.2f}%",
            help="% of initial users who became subscribers"
        )
        st.metric(
            "Churn Rate",
            f"{metrics['churn_rate']:.2f}%",
            help="% of users who left the platform"
        )
    
    with col3:
        st.metric(
            "Active Users",
            f"{metrics['active_users']:,}",
            help="Users still active (not churned)"
        )
        st.metric(
            "Churn Count",
            f"{metrics['final_churned']:,}",
            help="Users who churned"
        )


def render_transition_matrix_viz():
    """Render transition matrix visualizations."""
    st.subheader("📊 Transition Matrix Analysis")
    
    visualizer = MarkovChainVisualizer(st.session_state.markov_chain)
    
    # Heatmap
    fig_heatmap = visualizer.plot_transition_matrix()
    st.pyplot(fig_heatmap)
    
    # Network graph
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("### Transition Network")
        threshold = st.slider(
            "Show edges with probability ≥",
            min_value=0.0,
            max_value=0.5,
            value=0.05,
            step=0.01
        )
        fig_network = visualizer.plot_transition_network(prob_threshold=threshold)
        st.pyplot(fig_network)
    
    with col2:
        st.write("### Steady-State Distribution")
        steady_state = st.session_state.markov_chain.compute_steady_state()
        
        fig_steady = visualizer.plot_steady_state_distribution()
        st.pyplot(fig_steady)
        
        # Display steady state table
        st.write("**Steady-State Values (π)**")
        steady_df = pd.DataFrame({
            'State': st.session_state.markov_chain.state_names,
            'Probability': steady_state,
            'Percentage': steady_state * 100
        })
        st.dataframe(steady_df, use_container_width=True)


def render_simulation_results(result):
    """Render simulation results and visualizations."""
    st.subheader("📈 Simulation Results")
    
    # Metrics
    metrics = result.get_metrics()
    render_metrics_section(metrics)
    
    # Time series visualization
    st.write("### User Distribution Over Time")
    
    viz = SimulationVisualizer(result.state_names)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("**Stacked Area Chart (Absolute)**")
        fig_area = viz.plot_state_distribution_over_time(result)
        st.pyplot(fig_area)
    
    with col2:
        st.write("**Stacked Area Chart (Proportions)**")
        fig_prop = viz.plot_state_proportions_over_time(result)
        st.pyplot(fig_prop)
    
    # Funnel and metrics
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("### Conversion Funnel")
        fig_funnel = viz.plot_funnel_chart(result)
        st.pyplot(fig_funnel)
    
    with col2:
        st.write("### Key Metrics Summary")
        fig_metrics = viz.plot_conversion_metrics(result)
        st.pyplot(fig_metrics)
    
    # Data table
    st.write("### State Distribution Data")
    df = result.get_dataframe()
    st.dataframe(df, use_container_width=True)
    
    # Proportions table
    st.write("### State Proportions (%)")
    prop_df = result.get_state_proportions() * 100
    st.dataframe(prop_df.round(2), use_container_width=True)


def render_ergodicity_analysis():
    """Render ergodicity analysis."""
    st.subheader("🔬 Markov Chain Properties")
    
    ergodicity_checks = st.session_state.markov_chain.check_ergodicity()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Ergodicity Checks:**")
        for check, result_val in ergodicity_checks.items():
            status = "✓" if result_val else "✗"
            st.write(f"{status} {check.replace('_', ' ').title()}: {result_val}")
    
    with col2:
        if ergodicity_checks["is_ergodic"]:
            st.success("✓ This chain is ERGODIC")
            st.info("""
            The chain has a unique, stable steady-state distribution 
            that is independent of the initial conditions. This is 
            important for our analysis!
            """)
        else:
            st.warning("⚠ This chain may not be ergodic")
            st.info("The steady-state may depend on initial conditions.")


def render_insights_section(result):
    """Generate and render business insights."""
    st.subheader("💡 Business Insights")
    
    metrics = result.get_metrics()
    
    # Identify key insights
    insights = []
    
    # Conversion insight
    if metrics['subscriber_conversion_rate'] > 30:
        insights.append("🎯 **Strong Conversion**: >30% of users convert to subscribers")
    elif metrics['subscriber_conversion_rate'] < 10:
        insights.append("⚠️ **Low Conversion**: <10% conversion rate - consider engagement improvements")
    else:
        insights.append("📊 **Moderate Conversion**: 10-30% conversion rate")
    
    # Churn insight
    if metrics['churn_rate'] > 50:
        insights.append("🔴 **High Churn**: >50% of users leave - urgent action needed")
    elif metrics['churn_rate'] < 20:
        insights.append("✓ **Healthy Churn**: <20% - good user retention")
    else:
        insights.append("⚠️ **Moderate Churn**: 20-50% - room for improvement")
    
    # Subscriber insight
    if metrics['final_subscribers'] > metrics['total_users'] * 0.2:
        insights.append("💰 **Strong Monetization**: >20% subscriber base")
    
    # Active users insight
    active_rate = (metrics['active_users'] / metrics['total_users']) * 100
    if active_rate > 50:
        insights.append("👥 **High Engagement**: >50% users still active")
    
    for insight in insights:
        st.write(f"• {insight}")
    
    # Recommendations
    st.write("### 📋 Recommendations:")
    
    recommendations = []
    
    if metrics['churn_rate'] > 30:
        recommendations.append("1. Implement retention strategies (personalization, recommendations)")
    
    if metrics['subscriber_conversion_rate'] < 20:
        recommendations.append("2. Enhance free trial experience to drive subscriptions")
        recommendations.append("3. Offer premium content earlier in user journey")
    
    if metrics['final_subscribers'] < metrics['total_users'] * 0.1:
        recommendations.append("4. Increase pricing experiments with high-engagement segments")
    
    if not recommendations:
        recommendations.append("✓ Current metrics are strong - focus on scale!")
    
    for rec in recommendations:
        st.write(f"• {rec}")


def main():
    """Main dashboard function."""
    initialize_session_state()
    
    # Header
    st.title("📺 Streaming Platform Engagement & Churn Simulator")
    st.markdown("""
        **Markov Chain-Based User Behavior Model**
        
        This dashboard simulates user behavior transitions across engagement states 
        using stochastic processes. Analyze conversion rates, churn patterns, and 
        optimize platform metrics.
    """)
    
    # Sidebar controls
    n_users, n_steps, lambda_rate, use_arrivals = render_sidebar()
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Run Simulation",
        "📊 Transition Analysis",
        "🔬 Theory & Properties",
        "📚 Documentation"
    ])
    
    # Tab 1: Run Simulation
    with tab1:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            run_button = st.button("🚀 Run Simulation", key="run_sim", use_container_width=True)
        
        with col2:
            st.write("")
            seed = st.number_input("Random Seed (for reproducibility)", value=42)
        
        with col3:
            st.write("")
            if st.button("🔄 Compare Scenarios", use_container_width=True):
                st.info("Run simulation multiple times with different settings to compare")
        
        if run_button:
            with st.spinner("Running simulation..."):
                if use_arrivals:
                    sim_engine = EnhancedSimulationEngine(st.session_state.markov_chain)
                    result, arrivals = sim_engine.run_simulation_with_arrivals(
                        lambda_rate=lambda_rate,
                        n_steps=n_steps,
                        seed=seed
                    )
                    st.session_state.simulation_result = result
                    
                    st.success("✓ Simulation with Poisson arrivals completed!")
                    
                    # Show arrivals
                    st.write("### New User Arrivals (Poisson Process)")
                    arrivals_df = pd.DataFrame({
                        'Time Step': range(len(arrivals)),
                        'New Arrivals': arrivals,
                        'Cumulative': np.cumsum(arrivals)
                    })
                    st.dataframe(arrivals_df, use_container_width=True)
                
                else:
                    sim_engine = SimulationEngine(st.session_state.markov_chain)
                    result = sim_engine.run_simulation(
                        n_users=n_users,
                        n_steps=n_steps,
                        seed=seed
                    )
                    st.session_state.simulation_result = result
                    st.success("✓ Simulation completed!")
        
        # Display results if available
        if st.session_state.simulation_result is not None:
            render_simulation_results(st.session_state.simulation_result)
            
            # Business insights
            render_insights_section(st.session_state.simulation_result)
    
    # Tab 2: Transition Analysis
    with tab2:
        render_transition_matrix_viz()
    
    # Tab 3: Theory & Properties
    with tab3:
        st.write("## 🎓 Markov Chain Theory")
        
        st.markdown("""
        ### What is a Markov Chain?
        
        A **Markov Chain** is a stochastic process where the future state depends 
        only on the current state (memoryless property).
        
        **Key Properties:**
        - **States**: User engagement states (Visitor, Browsing, etc.)
        - **Transition Matrix (P)**: Probabilities of moving between states
        - **State Evolution**: v(t+1) = v(t) × P
        
        ### Steady-State Distribution
        
        The **steady-state** (π) is a probability distribution where:
        - π = π × P (equilibrium condition)
        - Independent of initial state (if ergodic)
        - Represents long-run proportions of users in each state
        
        ### Ergodicity
        
        A Markov chain is **ergodic** if:
        1. **Irreducible**: All states communicate (reach each other)
        2. **Aperiodic**: No cycle patterns
        
        This ensures a unique steady-state that we can compute and rely on.
        """)
        
        # Ergodicity analysis
        render_ergodicity_analysis()
        
        st.write("---")
        st.write("## 📊 Mathematical Formulations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### State Evolution Equation")
            st.latex(r"v(t+1) = v(t) \cdot P")
            st.write("Where:")
            st.write("- v(t) = state probability vector at time t")
            st.write("- P = transition probability matrix")
        
        with col2:
            st.write("### Steady-State Condition")
            st.latex(r"\pi = \pi \cdot P")
            st.write("Where:")
            st.write("- π = steady-state distribution")
            st.write("- πP = π (equilibrium)")
    
    # Tab 4: Documentation
    with tab4:
        st.write("## 📚 Documentation & Guide")
        
        st.write("### How to Use This Dashboard")
        
        st.markdown("""
        **1. Configuration (Sidebar)**
        - Set number of users and simulation time steps
        - Enable Poisson arrivals for realistic user growth
        - Adjust transition probabilities using Quick Adjustments
        
        **2. Run Simulation**
        - Click "Run Simulation" to execute model
        - View results in charts and tables
        - Analyze business insights automatically generated
        
        **3. Analyze Transitions**
        - Visualize transition matrix as heatmap
        - View state transition network
        - Check steady-state distribution
        
        **4. Understand Theory**
        - Review Markov chain concepts
        - Check ergodicity properties
        - Understand mathematical formulations
        
        ### Key Metrics Explained
        
        - **Conversion Rate**: % of users who become paid subscribers
        - **Churn Rate**: % of users who leave the platform
        - **Active Users**: Users still engaged (not churned)
        - **Steady-State**: Long-run equilibrium distribution
        
        ### State Definitions
        
        - **Visitor**: Free trial or non-registered user
        - **Browsing**: Looking at content, not watching
        - **Watching**: Actively viewing content
        - **Binge Watching**: Extended viewing sessions
        - **Subscriber**: Paid subscriber
        - **Churn**: Left the platform (absorbing state)
        
        ### Tips for Best Results
        
        1. **Start with default matrix** to understand basic dynamics
        2. **Use Quick Adjustments** for scenario planning
        3. **Run multiple simulations** with different parameters
        4. **Analyze steady-state** for long-term insights
        5. **Compare scenarios** to find optimization strategies
        """)
        
        st.write("---")
        st.write("### Project Information")
        st.markdown("""
        **Subject**: Stochastic Processes and Applications  
        **Model**: Markov Chains + Optional Poisson Processes  
        **Technology Stack**: Python, Streamlit, NumPy, Pandas, Plotly  
        **GitHub**: [streaming-platform-simulator](https://github.com)
        """)


if __name__ == "__main__":
    main()
