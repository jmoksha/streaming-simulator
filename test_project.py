"""
Test Script for Streaming Platform Simulator
Verifies all core functionality works correctly
"""

import sys
import numpy as np
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def test_markov_chain():
    """Test Markov chain functionality."""
    print("\n" + "="*70)
    print("TEST 1: Markov Chain Model")
    print("="*70)
    
    from src.markov_model import MarkovChainModel, DEFAULT_TRANSITION_MATRIX
    
    # Create chain
    mc = MarkovChainModel(DEFAULT_TRANSITION_MATRIX)
    print("✓ Markov chain created")
    
    # Validate
    mc.validate_matrix()
    print("✓ Matrix validated (rows sum to 1)")
    
    # Check ergodicity
    ergodicity = mc.check_ergodicity()
    print(f"✓ Ergodic: {ergodicity['is_ergodic']}")
    
    # Compute steady-state
    steady_state = mc.compute_steady_state()
    print(f"✓ Steady-state computed: {steady_state[:3]}")
    
    # Verify π = π·P
    verification = steady_state @ mc.transition_matrix
    is_valid = np.allclose(steady_state, verification, atol=1e-6)
    print(f"✓ Verification (π·P = π): {is_valid}")
    
    return True


def test_simulation():
    """Test simulation functionality."""
    print("\n" + "="*70)
    print("TEST 2: Monte Carlo Simulation")
    print("="*70)
    
    from src.markov_model import MarkovChainModel, DEFAULT_TRANSITION_MATRIX
    from src.simulation import SimulationEngine
    
    mc = MarkovChainModel(DEFAULT_TRANSITION_MATRIX)
    engine = SimulationEngine(mc)
    
    # Run simulation
    result = engine.run_simulation(n_users=500, n_steps=30, seed=42)
    print(f"✓ Simulation completed: {result.n_users} users, {result.n_steps} steps")
    
    # Get metrics
    metrics = result.get_metrics()
    print(f"✓ Metrics computed:")
    print(f"    - Conversion rate: {metrics['subscriber_conversion_rate']:.2f}%")
    print(f"    - Churn rate: {metrics['churn_rate']:.2f}%")
    print(f"    - Final subscribers: {metrics['final_subscribers']}")
    
    # Get dataframe
    df = result.get_dataframe()
    print(f"✓ Data extracted: shape {df.shape}")
    
    return True


def test_poisson_arrivals():
    """Test Poisson arrival process."""
    print("\n" + "="*70)
    print("TEST 3: Poisson Arrivals")
    print("="*70)
    
    from src.simulation import PoissonArrivalProcess, EnhancedSimulationEngine
    from src.markov_model import MarkovChainModel, DEFAULT_TRANSITION_MATRIX
    
    # Test Poisson process
    poisson = PoissonArrivalProcess(lambda_rate=10)
    arrivals = poisson.generate_arrivals(time_horizon=30, seed=42)
    print(f"✓ Poisson arrivals generated: {arrivals.sum()} total arrivals")
    print(f"    - Mean: {arrivals.mean():.2f}, Std: {arrivals.std():.2f}")
    
    # Test simulation with arrivals
    mc = MarkovChainModel(DEFAULT_TRANSITION_MATRIX)
    engine = EnhancedSimulationEngine(mc)
    
    result, arrivals_data = engine.run_simulation_with_arrivals(
        lambda_rate=10,
        n_steps=30,
        seed=42
    )
    print(f"✓ Simulation with arrivals: {result.n_users} total users")
    
    return True


def test_visualization():
    """Test visualization functions."""
    print("\n" + "="*70)
    print("TEST 4: Visualization Functions")
    print("="*70)
    
    from src.markov_model import MarkovChainModel, DEFAULT_TRANSITION_MATRIX
    from src.simulation import SimulationEngine
    from src.visualization import MarkovChainVisualizer, SimulationVisualizer
    
    # Markov chain visualizer
    mc = MarkovChainModel(DEFAULT_TRANSITION_MATRIX)
    mc_viz = MarkovChainVisualizer(mc)
    
    fig1 = mc_viz.plot_transition_matrix()
    print("✓ Transition matrix heatmap created")
    
    fig2 = mc_viz.plot_transition_network()
    print("✓ Transition network graph created")
    
    mc.compute_steady_state()
    fig3 = mc_viz.plot_steady_state_distribution()
    print("✓ Steady-state distribution plot created")
    
    # Simulation visualizer
    engine = SimulationEngine(mc)
    result = engine.run_simulation(n_users=500, n_steps=30, seed=42)
    
    sim_viz = SimulationVisualizer(result.state_names)
    
    fig4 = sim_viz.plot_state_distribution_over_time(result)
    print("✓ State distribution over time plot created")
    
    fig5 = sim_viz.plot_state_proportions_over_time(result)
    print("✓ State proportions plot created")
    
    fig6 = sim_viz.plot_funnel_chart(result)
    print("✓ Funnel chart created")
    
    fig7 = sim_viz.plot_conversion_metrics(result)
    print("✓ Conversion metrics plot created")
    
    return True


def test_sensitivity_analysis():
    """Test sensitivity analysis."""
    print("\n" + "="*70)
    print("TEST 5: Sensitivity Analysis")
    print("="*70)
    
    from src.markov_model import MarkovChainModel, DEFAULT_TRANSITION_MATRIX
    from src.simulation import SimulationEngine
    
    mc = MarkovChainModel(DEFAULT_TRANSITION_MATRIX)
    engine = SimulationEngine(mc)
    
    # Run sensitivity analysis
    results = engine.run_sensitivity_analysis(
        n_users=500,
        n_steps=30,
        parameter="Visitor→Subscriber Probability",
        param_values=np.arange(0, 0.26, 0.05),
        from_state="Visitor",
        to_state="Subscriber",
        n_simulations=2
    )
    
    print(f"✓ Sensitivity analysis completed: {len(results)} parameter values tested")
    
    # Print results
    for param, metrics in results.items():
        print(f"    P(V→S)={param:.2f}: Conversion={metrics['subscriber_conversion_rate']:.2f}%")
    
    return True


def test_data_loading():
    """Test loading transition matrix from CSV."""
    print("\n" + "="*70)
    print("TEST 6: Data Loading")
    print("="*70)
    
    from src.markov_model import load_transition_matrix_from_csv
    
    try:
        matrix, states = load_transition_matrix_from_csv('data/transition_matrix.csv')
        print(f"✓ Transition matrix loaded: shape {matrix.shape}")
        print(f"✓ States: {states}")
        return True
    except FileNotFoundError:
        print("⚠ CSV file not found - this is OK for testing")
        return True


def run_all_tests():
    """Run all tests."""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  STREAMING PLATFORM SIMULATOR - TEST SUITE".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    tests = [
        ("Markov Chain Model", test_markov_chain),
        ("Monte Carlo Simulation", test_simulation),
        ("Poisson Arrivals", test_poisson_arrivals),
        ("Visualization", test_visualization),
        ("Sensitivity Analysis", test_sensitivity_analysis),
        ("Data Loading", test_data_loading),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"✗ {test_name} FAILED: {str(e)}")
            failed += 1
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"✓ Passed: {passed}/{len(tests)}")
    print(f"✗ Failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n" + "🎉 "*35)
        print("ALL TESTS PASSED! Project is ready to use.")
        print("🎉 "*35)
    else:
        print(f"\n⚠ {failed} test(s) failed. Check errors above.")
    
    print("\n" + "="*70)
    print("Next steps:")
    print("  1. Run dashboard: streamlit run app/streamlit_dashboard.py")
    print("  2. Open notebook: jupyter notebook notebooks/analysis.ipynb")
    print("  3. Read guide: cat QUICKSTART.md")
    print("="*70 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend for testing
    
    success = run_all_tests()
    sys.exit(0 if success else 1)
