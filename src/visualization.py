"""
Visualization Module for Streaming Platform Analysis
Author: Data Scientist
Date: 2024

Provides professional visualizations for Markov chain analysis, simulations,
and streaming platform metrics.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple
import networkx as nx
from .markov_model import MarkovChainModel
from .simulation import SimulationResult


# Set default style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10


class MarkovChainVisualizer:
    """Visualization utilities for Markov chain analysis."""
    
    def __init__(self, markov_chain: MarkovChainModel):
        """
        Initialize visualizer.
        
        Parameters:
        -----------
        markov_chain : MarkovChainModel
            Markov chain model to visualize
        """
        self.markov_chain = markov_chain
        self.state_names = markov_chain.state_names
        self.n_states = markov_chain.n_states
    
    def plot_transition_matrix(self, figsize: Tuple = (10, 8),
                              cmap: str = 'YlOrRd') -> plt.Figure:
        """
        Visualize transition matrix as heatmap.
        
        Parameters:
        -----------
        figsize : Tuple
            Figure size
        cmap : str
            Colormap name
        
        Returns:
        --------
        plt.Figure : Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create heatmap
        im = ax.imshow(
            self.markov_chain.transition_matrix,
            cmap=cmap,
            aspect='auto',
            vmin=0,
            vmax=1
        )
        
        # Set ticks and labels
        ax.set_xticks(np.arange(self.n_states))
        ax.set_yticks(np.arange(self.n_states))
        ax.set_xticklabels(self.state_names, rotation=45, ha='right')
        ax.set_yticklabels(self.state_names)
        
        # Add text annotations
        for i in range(self.n_states):
            for j in range(self.n_states):
                prob = self.markov_chain.transition_matrix[i, j]
                text = ax.text(
                    j, i, f'{prob:.2f}',
                    ha="center", va="center",
                    color="black" if prob < 0.5 else "white",
                    fontweight='bold'
                )
        
        ax.set_xlabel('To State', fontsize=12, fontweight='bold')
        ax.set_ylabel('From State', fontsize=12, fontweight='bold')
        ax.set_title('Transition Probability Matrix', fontsize=14, fontweight='bold')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Probability', rotation=270, labelpad=20)
        
        plt.tight_layout()
        return fig
    
    def plot_transition_network(self, figsize: Tuple = (12, 10),
                               prob_threshold: float = 0.05) -> plt.Figure:
        """
        Visualize transition matrix as network graph.
        
        Parameters:
        -----------
        figsize : Tuple
            Figure size
        prob_threshold : float
            Only draw edges with probability >= threshold
        
        Returns:
        --------
        plt.Figure : Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create directed graph
        G = nx.DiGraph()
        
        # Add nodes
        for state in self.state_names:
            G.add_node(state)
        
        # Add edges with probabilities as weights
        for i, from_state in enumerate(self.state_names):
            for j, to_state in enumerate(self.state_names):
                prob = self.markov_chain.transition_matrix[i, j]
                if prob >= prob_threshold:
                    G.add_edge(from_state, to_state, weight=prob)
        
        # Layout
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
        
        # Draw nodes
        node_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', 
                      '#FFA07A', '#98D8C8', '#C7CEEA']
        nx.draw_networkx_nodes(
            G, pos,
            node_color=node_colors,
            node_size=3000,
            ax=ax,
            edgecolors='black',
            linewidths=2
        )
        
        # Draw edges with varying width based on probability
        edges = G.edges()
        weights = [G[u][v]['weight'] for u, v in edges]
        
        nx.draw_networkx_edges(
            G, pos,
            width=[w * 5 for w in weights],
            edge_color='gray',
            alpha=0.6,
            ax=ax,
            arrowsize=20,
            arrowstyle='-|>',
            connectionstyle='arc3,rad=0.1'
        )
        
        # Draw labels
        nx.draw_networkx_labels(
            G, pos,
            font_size=10,
            font_weight='bold',
            ax=ax
        )
        
        # Add edge labels (probabilities)
        edge_labels = {
            (u, v): f"{G[u][v]['weight']:.2f}" 
            for u, v in G.edges()
        }
        nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels,
            font_size=8,
            ax=ax
        )
        
        ax.set_title('State Transition Network', fontsize=14, fontweight='bold')
        ax.axis('off')
        
        plt.tight_layout()
        return fig
    
    def plot_steady_state_distribution(self, figsize: Tuple = (12, 6)) -> plt.Figure:
        """
        Visualize steady-state distribution.
        
        Parameters:
        -----------
        figsize : Tuple
            Figure size
        
        Returns:
        --------
        plt.Figure : Matplotlib figure object
        """
        if self.markov_chain.steady_state is None:
            self.markov_chain.compute_steady_state()
        
        fig, ax = plt.subplots(figsize=figsize)
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#C7CEEA']
        bars = ax.bar(
            range(self.n_states),
            self.markov_chain.steady_state,
            color=colors,
            edgecolor='black',
            linewidth=2,
            alpha=0.8
        )
        
        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, self.markov_chain.steady_state)):
            ax.text(
                bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.01,
                f'{value:.3f}\n({value*100:.1f}%)',
                ha='center', va='bottom',
                fontweight='bold',
                fontsize=10
            )
        
        ax.set_xticks(range(self.n_states))
        ax.set_xticklabels(self.state_names, rotation=45, ha='right')
        ax.set_ylabel('Probability', fontsize=12, fontweight='bold')
        ax.set_title('Steady-State Distribution (π = π·P)', 
                    fontsize=14, fontweight='bold')
        ax.set_ylim([0, max(self.markov_chain.steady_state) * 1.15])
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        return fig


class SimulationVisualizer:
    """Visualization utilities for simulation results."""
    
    def __init__(self, state_names: List[str] = None):
        """
        Initialize visualizer.
        
        Parameters:
        -----------
        state_names : List[str], optional
            Names of states
        """
        self.state_names = state_names or [
            "Visitor", "Browsing", "Watching", 
            "Binge Watching", "Subscriber", "Churn"
        ]
        self.colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#C7CEEA']
    
    def plot_state_distribution_over_time(self, 
                                         result: SimulationResult,
                                         figsize: Tuple = (14, 7),
                                         stacked: bool = True) -> plt.Figure:
        """
        Plot state distribution evolution over time.
        
        Parameters:
        -----------
        result : SimulationResult
            Simulation results
        figsize : Tuple
            Figure size
        stacked : bool
            Whether to use stacked area plot
        
        Returns:
        --------
        plt.Figure : Matplotlib figure object
        """
        df = result.get_dataframe()
        
        fig, ax = plt.subplots(figsize=figsize)
        
        if stacked:
            ax.stackplot(
                df.index,
                [df[col].values for col in self.state_names],
                labels=self.state_names,
                colors=self.colors,
                alpha=0.8
            )
        else:
            for i, state in enumerate(self.state_names):
                ax.plot(
                    df.index,
                    df[state],
                    marker='o',
                    label=state,
                    linewidth=2.5,
                    color=self.colors[i],
                    markersize=4
                )
        
        ax.set_xlabel('Time Step', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Users', fontsize=12, fontweight='bold')
        ax.set_title('User Distribution Across States Over Time', 
                    fontsize=14, fontweight='bold')
        ax.legend(loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_state_proportions_over_time(self,
                                        result: SimulationResult,
                                        figsize: Tuple = (14, 7)) -> plt.Figure:
        """
        Plot state proportions (normalized) over time.
        
        Parameters:
        -----------
        result : SimulationResult
            Simulation results
        figsize : Tuple
            Figure size
        
        Returns:
        --------
        plt.Figure : Matplotlib figure object
        """
        proportions_df = result.get_state_proportions()
        
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.stackplot(
            proportions_df.index,
            [proportions_df[col].values for col in self.state_names],
            labels=self.state_names,
            colors=self.colors,
            alpha=0.8
        )
        
        ax.set_xlabel('Time Step', fontsize=12, fontweight='bold')
        ax.set_ylabel('Proportion of Users', fontsize=12, fontweight='bold')
        ax.set_title('Proportion of Users in Each State (100% Stacked)', 
                    fontsize=14, fontweight='bold')
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), framealpha=0.9)
        ax.set_ylim([0, 1])
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig
    
    def plot_funnel_chart(self, result: SimulationResult,
                         figsize: Tuple = (10, 8)) -> plt.Figure:
        """
        Create funnel chart showing Visitor → Subscriber progression.
        
        Parameters:
        -----------
        result : SimulationResult
            Simulation results
        figsize : Tuple
            Figure size
        
        Returns:
        --------
        plt.Figure : Matplotlib figure object
        """
        initial_visitors = result.state_counts[0, 0]
        final_counts = result.state_counts[-1]
        
        funnel_states = ["Visitor", "Browsing", "Watching", "Binge Watching", "Subscriber"]
        funnel_counts = [
            result.state_counts[0, 0],  # Initial visitors
            final_counts[1],  # Final browsing
            final_counts[2],  # Final watching
            final_counts[3],  # Final binge watching
            final_counts[4]   # Final subscribers
        ]
        
        # Ensure we have progressive flow for funnel visualization
        cumulative = []
        for i, count in enumerate(funnel_counts):
            if i == 0:
                cumulative.append(count)
            else:
                cumulative.append(min(cumulative[-1], count) if count > 0 else 0)
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create funnel using barh
        y_pos = np.arange(len(funnel_states))
        colors_funnel = self.colors[:len(funnel_states)]
        
        bars = ax.barh(
            y_pos,
            cumulative,
            color=colors_funnel,
            edgecolor='black',
            linewidth=2,
            alpha=0.8
        )
        
        # Add value and percentage labels
        for i, (bar, count, original) in enumerate(zip(bars, cumulative, funnel_counts)):
            percentage = (count / initial_visitors) * 100
            ax.text(
                bar.get_width() + 5,
                bar.get_y() + bar.get_height()/2,
                f'{original:.0f} ({percentage:.1f}%)',
                va='center',
                fontweight='bold',
                fontsize=11
            )
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(funnel_states)
        ax.set_xlabel('Number of Users', fontsize=12, fontweight='bold')
        ax.set_title('User Funnel: Visitor to Subscriber Conversion', 
                    fontsize=14, fontweight='bold')
        ax.invert_yaxis()
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_conversion_metrics(self, result: SimulationResult,
                               figsize: Tuple = (14, 6)) -> plt.Figure:
        """
        Plot key conversion and churn metrics.
        
        Parameters:
        -----------
        result : SimulationResult
            Simulation results
        figsize : Tuple
            Figure size
        
        Returns:
        --------
        plt.Figure : Matplotlib figure object
        """
        metrics = result.get_metrics()
        
        fig, axes = plt.subplots(1, 3, figsize=figsize)
        
        # Pie chart: Final state distribution
        final_state_counts = result.state_counts[-1]
        colors_pie = self.colors
        
        axes[0].pie(
            final_state_counts,
            labels=self.state_names,
            autopct='%1.1f%%',
            colors=colors_pie,
            startangle=90
        )
        axes[0].set_title('Final User Distribution', fontsize=12, fontweight='bold')
        
        # Bar chart: Conversion metrics
        conversion_data = {
            'Subscribers': metrics['final_subscribers'],
            'Active Users': metrics['active_users'],
            'Churned': metrics['final_churned']
        }
        axes[1].bar(
            conversion_data.keys(),
            conversion_data.values(),
            color=['#98D8C8', '#4ECDC4', '#C7CEEA'],
            edgecolor='black',
            linewidth=2
        )
        axes[1].set_ylabel('Number of Users', fontsize=11, fontweight='bold')
        axes[1].set_title('Key Metrics', fontsize=12, fontweight='bold')
        axes[1].grid(axis='y', alpha=0.3)
        
        for i, (k, v) in enumerate(conversion_data.items()):
            axes[1].text(i, v + 5, f'{v:.0f}', ha='center', fontweight='bold')
        
        # Rates
        rate_data = {
            'Conversion Rate': metrics['subscriber_conversion_rate'],
            'Churn Rate': metrics['churn_rate']
        }
        axes[2].bar(
            rate_data.keys(),
            rate_data.values(),
            color=['#98D8C8', '#FF6B6B'],
            edgecolor='black',
            linewidth=2
        )
        axes[2].set_ylabel('Percentage (%)', fontsize=11, fontweight='bold')
        axes[2].set_title('Conversion & Churn Rates', fontsize=12, fontweight='bold')
        axes[2].grid(axis='y', alpha=0.3)
        axes[2].set_ylim([0, 100])
        
        for i, (k, v) in enumerate(rate_data.items()):
            axes[2].text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')
        
        plt.tight_layout()
        return fig


def create_interactive_dashboard(result: SimulationResult) -> go.Figure:
    """
    Create interactive Plotly dashboard.
    
    Parameters:
    -----------
    result : SimulationResult
        Simulation results
    
    Returns:
    --------
    go.Figure : Plotly figure
    """
    df = result.get_dataframe()
    metrics = result.get_metrics()
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'User Distribution Over Time',
            'Final State Distribution',
            'Conversion Funnel',
            'Key Metrics'
        ),
        specs=[
            [{"secondary_y": False}, {"secondary_y": False}],
            [{"secondary_y": False}, {"secondary_y": False}]
        ]
    )
    
    # Time series
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#C7CEEA']
    for i, state in enumerate(result.state_names):
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[state],
                name=state,
                mode='lines',
                line=dict(color=colors[i], width=2),
                stackgroup='one'
            ),
            row=1, col=1
        )
    
    # Pie chart
    final_counts = result.state_counts[-1]
    fig.add_trace(
        go.Pie(
            labels=result.state_names,
            values=final_counts,
            marker=dict(colors=colors),
            name='Final Distribution'
        ),
        row=1, col=2
    )
    
    # Funnel
    funnel_states = ["Visitor", "Browsing", "Watching", "Binge Watching", "Subscriber"]
    funnel_values = [
        result.state_counts[0, 0],
        result.state_counts[-1, 1],
        result.state_counts[-1, 2],
        result.state_counts[-1, 3],
        result.state_counts[-1, 4]
    ]
    
    fig.add_trace(
        go.Funnel(
            x=funnel_values,
            y=funnel_states,
            name='Conversion Funnel'
        ),
        row=2, col=1
    )
    
    # Metrics table
    metrics_text = f"""
    <b>Key Metrics</b><br>
    Total Users: {metrics['total_users']}<br>
    Subscribers: {metrics['final_subscribers']}<br>
    Churned: {metrics['final_churned']}<br>
    <b>Conversion Rate: {metrics['subscriber_conversion_rate']:.2f}%</b><br>
    <b>Churn Rate: {metrics['churn_rate']:.2f}%</b>
    """
    
    fig.add_trace(
        go.Scatter(
            x=[0], y=[0],
            mode='text',
            text=[metrics_text],
            textposition='middle center',
            showlegend=False,
            hoverinfo='none'
        ),
        row=2, col=2
    )
    
    # Update layout
    fig.update_xaxes(title_text="Time Step", row=1, col=1)
    fig.update_yaxes(title_text="Users", row=1, col=1)
    fig.update_xaxes(visible=False, row=2, col=2)
    fig.update_yaxes(visible=False, row=2, col=2)
    
    fig.update_layout(
        height=900,
        title_text="Streaming Platform Engagement Dashboard",
        showlegend=True,
        font=dict(size=12)
    )
    
    return fig
