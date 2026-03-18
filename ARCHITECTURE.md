# 🏗️ ARCHITECTURE & DESIGN DOCUMENTATION

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT DASHBOARD                           │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │  Sidebar    │  │  Main Tabs   │  │   Visualizations    │   │
│  │ Controls    │  │  - Run Sim   │  │   - Charts          │   │
│  │ - Users     │  │  - Analysis  │  │   - Heatmaps        │   │
│  │ - Steps     │  │  - Theory    │  │   - Networks        │   │
│  │ - Matrix    │  │  - Docs      │  │   - Metrics         │   │
│  └─────────────┘  └──────────────┘  └──────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │          USER INTERACTION LAYER                         │   │
│  │  - Parameter Input                                      │   │
│  │  - Real-time Updates                                    │   │
│  │  - Result Display                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
        ┌──────────────────────────────────────────────┐
        │     APPLICATION LAYER (Orchestration)        │
        │                                              │
        │  - Coordinate model and simulation           │
        │  - Process user input                        │
        │  - Generate insights                         │
        │  - Format outputs                            │
        └──────────────────────────────────────────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
    ┌───────────────────┐ ┌──────────────┐ ┌──────────────────┐
    │  MARKOV MODEL     │ │ SIMULATION   │ │ VISUALIZATION    │
    │                   │ │              │ │                  │
    │ • Chain creation  │ │ • MC Sim     │ │ • Plot charts    │
    │ • Validation      │ │ • Sensitivity│ │ • Interactive    │
    │ • Steady-state    │ │ • Poisson    │ │ • Export images  │
    │ • Ergodicity      │ │ • Results    │ │ • Dashboards     │
    │ • Trajectories    │ │   container  │ │                  │
    └───────────────────┘ └──────────────┘ └──────────────────┘
                │              │              │
                └──────────────┼──────────────┘
                               │
                               ▼
        ┌──────────────────────────────────────────────┐
        │      DATA LAYER                              │
        │                                              │
        │  • transition_matrix.csv (transition matrix) │
        │  • NumPy arrays (simulation data)            │
        │  • Pandas DataFrames (results)               │
        │  • Matplotlib/Plotly figures (outputs)       │
        └──────────────────────────────────────────────┘
```

---

## Module Dependency Graph

```
streamlit_dashboard.py (Entry point)
    ├── markov_model.py
    │   ├── numpy
    │   ├── pandas
    │   └── dataclasses
    │
    ├── simulation.py
    │   ├── markov_model.py
    │   ├── numpy
    │   ├── pandas
    │   └── dataclasses
    │
    └── visualization.py
        ├── markov_model.py
        ├── simulation.py
        ├── matplotlib
        ├── seaborn
        ├── plotly
        ├── pandas
        ├── numpy
        └── networkx

notebooks/analysis.ipynb
    ├── All modules above
    ├── jupyter
    └── ipython
```

---

## Class Hierarchy

```
MARKOV_MODEL.PY
│
└── MarkovChainModel
    ├── __init__(transition_matrix, state_names)
    ├── validate_matrix()
    ├── compute_next_state(current_state)
    ├── compute_steady_state(method='power')
    │   ├── _power_iteration()
    │   └── _eigenvalue_method()
    ├── check_ergodicity()
    │   ├── _is_irreducible()
    │   ├── _is_aperiodic()
    │   └── _has_unique_steady_state()
    ├── simulate_user_trajectory(n_steps, initial_state_idx)
    ├── get_transition_dataframe()
    ├── set_custom_matrix(matrix_dict)
    └── [Properties: steady_state, eigenvalues, eigenvectors]

SIMULATION.PY
│
├── SimulationResult (dataclass)
│   ├── state_counts: np.ndarray
│   ├── user_trajectories: Dict
│   ├── user_final_states: np.ndarray
│   ├── get_dataframe()
│   ├── get_state_proportions()
│   └── get_metrics()
│
├── SimulationEngine
│   ├── __init__(markov_chain)
│   ├── run_simulation(n_users, n_steps, initial_state, seed)
│   └── run_sensitivity_analysis(...)
│
├── PoissonArrivalProcess
│   ├── __init__(lambda_rate)
│   ├── generate_arrivals(time_horizon, seed)
│   └── cumulative_arrivals(arrivals)
│
└── EnhancedSimulationEngine (extends SimulationEngine)
    ├── run_simulation_with_arrivals(lambda_rate, n_steps, seed)
    └── [Inherits from SimulationEngine]

VISUALIZATION.PY
│
├── MarkovChainVisualizer
│   ├── __init__(markov_chain)
│   ├── plot_transition_matrix(figsize, cmap)
│   ├── plot_transition_network(figsize, prob_threshold)
│   └── plot_steady_state_distribution(figsize)
│
├── SimulationVisualizer
│   ├── __init__(state_names)
│   ├── plot_state_distribution_over_time(result, figsize, stacked)
│   ├── plot_state_proportions_over_time(result, figsize)
│   ├── plot_funnel_chart(result, figsize)
│   └── plot_conversion_metrics(result, figsize)
│
└── [Functions]
    ├── create_interactive_dashboard(result) → go.Figure
    └── [Helper functions]
```

---

## Data Flow Diagrams

### Simulation Flow

```
User Input
    │
    ├─ n_users
    ├─ n_steps
    ├─ transition_matrix
    └─ seed
         │
         ▼
┌─────────────────────────────┐
│ SimulationEngine.run_simulation()
│                             │
│ 1. Initialize users         │
│    (all Visitor state)      │
│                             │
│ 2. For each time step:      │
│    │                        │
│    ├─ For each user:        │
│    │  ├─ Get current state  │
│    │  ├─ Sample next state  │
│    │  ├─ Update trajectory  │
│    │  └─ Count new state    │
│    │                        │
│    └─ Store state counts    │
│                             │
│ 3. Compute metrics          │
│    ├─ Conversion rate       │
│    ├─ Churn rate            │
│    ├─ Final distributions   │
│    └─ Active users          │
│                             │
└─────────────────────────────┘
         │
         ▼
   SimulationResult
    │
    ├─ state_counts[T, S]
    ├─ user_trajectories[U → [states]]
    └─ metrics{...}
```

### Steady-State Computation

```
Transition Matrix P
    │
    ├─ Method: "power"
    │    │
    │    ▼
    │  ┌────────────────────────────┐
    │  │ Power Iteration Method      │
    │  │                            │
    │  │ v_0 = [1/6, 1/6, ...]     │
    │  │ for t in 1..max_iter:      │
    │  │   v_t = v_{t-1} · P       │
    │  │   if ||v_t - v_{t-1}|| < ε:
    │  │     return v_t             │
    │  └────────────────────────────┘
    │         │
    │         ▼
    │    Steady-state π
    │
    └─ Method: "eigen"
         │
         ▼
       ┌────────────────────────────┐
       │ Eigenvalue Decomposition    │
       │                            │
       │ λ, v = eig(P.T)            │
       │ π = v[:, argmax(|λ - 1|)]  │
       │ π = π / sum(π)             │
       └────────────────────────────┘
             │
             ▼
        Steady-state π

Both methods produce same π (verified: π·P = π)
```

### Visualization Pipeline

```
SimulationResult
    │
    ├─ Method 1: Matplotlib (Static)
    │    │
    │    ├─ plot_state_distribution_over_time()
    │    ├─ plot_funnel_chart()
    │    ├─ plot_conversion_metrics()
    │    └─ plot_transition_network()
    │         │
    │         ▼
    │    figure.png (saveable)
    │
    ├─ Method 2: Plotly (Interactive)
    │    │
    │    ├─ Line charts (zoom, hover)
    │    ├─ Pie charts (click segments)
    │    ├─ Funnel (interactive)
    │    └─ 3D surface (rotate)
    │         │
    │         ▼
    │    go.Figure (web-ready)
    │
    └─ Method 3: Streamlit (Dashboard)
         │
         ├─ st.plotly_chart()
         ├─ st.pyplot()
         ├─ st.metric()
         └─ st.dataframe()
              │
              ▼
         Interactive Web App
```

---

## State Machine Diagram

```
                    ┌─────────────────┐
                    │    VISITOR      │  (Free Trial)
                    │  Entry State    │
                    └────────┬────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
         50%               10%               10%
           │                 │                 │
           ▼                 ▼                 ▼
    ┌─────────────┐   ┌──────────────┐   ┌─────────┐
    │  BROWSING   │   │  WATCHING    │   │  CHURN  │ ◄─── Absorbing
    │             │   │              │   │         │
    └──────┬──────┘   └────┬────┬────┘   └─────────┘
           │               │    │
        40%│               │    └─ 10%
           │         30% ┌─┴──┐
           └────────────►│    │
                    15%  │    │
                    ┌────┘    │
                    │         │
                    │    45%  │
                    ▼         │
            ┌──────────────────┴──┐
            │  BINGE WATCHING     │
            │                     │
            └──────┬──────┬───────┘
                 3%│      │30%
                   │      │
                   │      ▼
                   │   ┌──────────────┐
                   │   │  SUBSCRIBER  │ ◄─ Strong Retention
                   │   │              │     75% stay
                   │   └────┬────┬────┘
                   │     5% │    │ 5%
                   │        │    │
                   └────────┤    ├──► CHURN (Absorbing)
                            │    │
                            ▼    │
                         CHURN ◄─┘
```

---

## Algorithm Complexity Analysis

### Steady-State Computation
```
Power Iteration:
  - Time: O(k × n²) where k = iterations, n = states
  - Space: O(n²) for transition matrix
  - Convergence: Linear (exponential in practice)
  - Typical: <100 iterations for n=6

Eigenvalue Method:
  - Time: O(n³) for decomposition
  - Space: O(n²) for matrices
  - Robust for any size
  - Best for n < 100
```

### Monte Carlo Simulation
```
Single User Trajectory:
  - Time: O(n_steps × log(n_states))
  - Space: O(n_steps)

Multi-User Simulation:
  - Time: O(n_users × n_steps × log(n_states))
  - Space: O(n_users × n_states + n_steps × n_states)
  
Practical (1000 users, 50 steps):
  - Time: ~1-2 seconds
  - Memory: ~50 MB
```

### Sensitivity Analysis
```
Parameters × Simulations × (users × steps)
  = n_params × n_sims × (U × T)
  
Example (6 values, 3 sims, 1000 users, 50 steps):
  = 6 × 3 × (1000 × 50 × log(6))
  ≈ 18 × 50,000 ≈ 900,000 operations
  ≈ 10 seconds runtime
```

---

## Design Patterns Used

### 1. **Factory Pattern**
```python
# SimulationResult acts as data container
result = engine.run_simulation(...)
# Result provides factory methods
df = result.get_dataframe()
metrics = result.get_metrics()
```

### 2. **Strategy Pattern**
```python
# Different steady-state computation strategies
markov_chain.compute_steady_state(method='power')
markov_chain.compute_steady_state(method='eigen')
```

### 3. **Observer Pattern (Streamlit)**
```python
# Streamlit reactively updates on input changes
if st.button("Run Simulation"):
    # Recomputes everything
    result = engine.run_simulation(...)
    # Displays results
```

### 4. **Decorator Pattern**
```python
# Visualization methods decorate raw data
result.get_dataframe()
sim_visualizer.plot_state_distribution_over_time(result)
```

### 5. **Inheritance**
```python
# EnhancedSimulationEngine extends SimulationEngine
class EnhancedSimulationEngine(SimulationEngine):
    def run_simulation_with_arrivals(self, ...):
        # Uses parent run_simulation method
```

---

## Error Handling Strategy

```
User Input
    │
    ├─ Streamlit sidebar validation
    │    └─ Type checking, range validation
    │
    ▼
Markov Chain Creation
    │
    ├─ Matrix shape validation
    ├─ Stochasticity check (rows sum to 1)
    ├─ Probability bounds check (0 ≤ p ≤ 1)
    └─ Exception handling with clear messages
    │
    ▼
Simulation Execution
    │
    ├─ User count validation
    ├─ Step count validation
    ├─ Seed validation
    └─ Try-catch for edge cases
    │
    ▼
Visualization
    │
    ├─ Check data availability
    ├─ Handle edge cases (empty data)
    └─ Graceful degradation
```

---

## Testing Architecture

```
test_project.py
│
├── Test 1: Markov Chain Model
│   ├─ Creation
│   ├─ Validation
│   ├─ Ergodicity
│   ├─ Steady-state
│   └─ Verification (π·P = π)
│
├── Test 2: Simulation
│   ├─ Run with small dataset
│   ├─ Check metrics computation
│   ├─ Verify data shapes
│   └─ Validate percentages
│
├── Test 3: Poisson Arrivals
│   ├─ Generation
│   ├─ Statistics
│   ├─ Simulation integration
│   └─ User count growth
│
├── Test 4: Visualization
│   ├─ Heatmap creation
│   ├─ Network graph
│   ├─ Time series
│   ├─ Funnel
│   └─ Metrics plots
│
├── Test 5: Sensitivity Analysis
│   ├─ Parameter variation
│   ├─ Results aggregation
│   └─ Trend analysis
│
└── Test 6: Data Loading
    ├─ CSV parsing
    ├─ Matrix shape
    └─ State names
```

---

## Performance Optimization

### Current Optimizations
✓ Vectorized NumPy operations (avoid loops)  
✓ Efficient Poisson sampling (np.random.poisson)  
✓ Lazy computation (steady-state only when needed)  
✓ Caching (streamlit @st.cache_resource)  

### Potential Optimizations
- GPU acceleration for large simulations
- Parallel user trajectory computation
- Batch processing for sensitivity
- C extensions for tight loops

---

## Extensibility Points

```python
# 1. Add new states
markov_chain.state_names.append("NewState")

# 2. Custom transition process
class CustomSimulationEngine(SimulationEngine):
    def run_simulation(self, ...):
        # Custom logic
        pass

# 3. New metrics
class ExtendedSimulationResult(SimulationResult):
    def get_revenue_metrics(self):
        # Custom calculations
        pass

# 4. Advanced visualization
class AdvancedVisualizer(SimulationVisualizer):
    def plot_custom_metric(self, result):
        # Custom plots
        pass

# 5. Multi-class users
markov_chains = {
    'free_users': MarkovChainModel(...),
    'premium_users': MarkovChainModel(...)
}
```

---

## Configuration Management

```
.streamlit/
├── config.toml (appearance, theme)

.env (future use)
├── DB_URL (database)
├── API_KEY (external services)
└── LOGGING_LEVEL

data/
├── transition_matrix.csv (customizable)
└── [future] historical_data.csv

src/
└── config.py (future)
    ├── DEFAULT_MATRIX
    ├── STATE_NAMES
    └── VISUALIZATION_COLORS
```

---

## Security Considerations

✓ Input validation on all user inputs  
✓ Matrix bounds checking (0-1)  
✓ Safe NumPy operations (no arbitrary code execution)  
✓ No database/network calls (local only)  
✓ Secure random seed handling  

---

## Monitoring & Logging (Future)

```python
# Could add:
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Usage:
logger.info(f"Simulation started: {n_users} users")
logger.debug(f"Steady-state: {steady_state}")
logger.warning(f"Non-ergodic chain detected")
```

---

**Architecture Documentation Complete** ✅  
All design patterns, data flows, and dependencies documented.
