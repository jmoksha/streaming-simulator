"""
Simulation Module for Streaming Platform User Behavior
Author: Data Scientist
Date: 2024

Implements Monte Carlo simulations and Poisson arrival processes for modeling
multiple users and generating realistic behavioral data.
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, List
from dataclasses import dataclass
from .markov_model import MarkovChainModel


@dataclass
class SimulationResult:
    """Container for simulation results."""
    
    state_counts: np.ndarray  # Shape: (n_steps, n_states)
    user_trajectories: Dict[int, np.ndarray]  # User trajectories
    user_final_states: np.ndarray  # Final state for each user
    n_users: int
    n_steps: int
    state_names: List[str]
    timestamps: np.ndarray  # Time array
    
    def get_dataframe(self) -> pd.DataFrame:
        """Convert state counts to DataFrame."""
        df = pd.DataFrame(
            self.state_counts,
            columns=self.state_names,
            index=self.timestamps
        )
        return df
    
    def get_state_proportions(self) -> pd.DataFrame:
        """Get state proportions over time."""
        total_users = self.state_counts.sum(axis=1, keepdims=True)
        proportions = self.state_counts / total_users
        
        df = pd.DataFrame(
            proportions,
            columns=self.state_names,
            index=self.timestamps
        )
        return df
    
    def get_metrics(self) -> Dict:
        """Compute key metrics from simulation."""
        total_users = self.n_users
        final_step_counts = self.state_counts[-1]
        
        metrics = {
            "total_users": total_users,
            "final_visitors": int(final_step_counts[0]),
            "final_browsing": int(final_step_counts[1]),
            "final_watching": int(final_step_counts[2]),
            "final_binge_watching": int(final_step_counts[3]),
            "final_subscribers": int(final_step_counts[4]),
            "final_churned": int(final_step_counts[5]),
            "subscriber_conversion_rate": (final_step_counts[4] / total_users) * 100,
            "churn_rate": (final_step_counts[5] / total_users) * 100,
            "active_users": int(final_step_counts[:5].sum()),
        }
        
        return metrics


class SimulationEngine:
    """
    Engine for running Monte Carlo simulations of user behavior.
    """
    
    def __init__(self, markov_chain: MarkovChainModel):
        """
        Initialize simulation engine.
        
        Parameters:
        -----------
        markov_chain : MarkovChainModel
            Markov chain model to use for simulations
        """
        self.markov_chain = markov_chain
        self.state_names = markov_chain.state_names
        self.n_states = markov_chain.n_states
    
    def run_simulation(self, n_users: int, n_steps: int,
                      initial_state: np.ndarray = None,
                      seed: int = None) -> SimulationResult:
        """
        Run Monte Carlo simulation of multiple users.
        
        Parameters:
        -----------
        n_users : int
            Number of users to simulate
        n_steps : int
            Number of time steps to simulate
        initial_state : np.ndarray, optional
            Initial state distribution. If None, all users start as Visitors.
        seed : int, optional
            Random seed for reproducibility
        
        Returns:
        --------
        SimulationResult : Simulation results containing state evolution
        """
        if seed is not None:
            np.random.seed(seed)
        
        if initial_state is None:
            # All users start as Visitors (state 0)
            initial_state = np.zeros(self.n_states)
            initial_state[0] = 1.0
        
        # Initialize state tracking
        state_counts = np.zeros((n_steps, self.n_states))
        user_trajectories = {}
        
        # Count initial distribution
        n_in_each_state = (initial_state * n_users).astype(int)
        # Adjust for rounding errors
        n_in_each_state[0] += n_users - n_in_each_state.sum()
        
        state_counts[0] = n_in_each_state
        
        # Initialize user trajectories
        user_id = 0
        for state_idx in range(self.n_states):
            for _ in range(n_in_each_state[state_idx]):
                user_trajectories[user_id] = np.array([state_idx])
                user_id += 1
        
        # Simulate state transitions
        for step in range(1, n_steps):
            new_counts = np.zeros(self.n_states)
            
            # For each user, simulate transition
            for uid in range(n_users):
                current_state = user_trajectories[uid][-1]
                
                # Get transition probabilities from current state
                transition_probs = self.markov_chain.transition_matrix[current_state]
                
                # Sample next state
                next_state = np.random.choice(
                    self.n_states,
                    p=transition_probs
                )
                
                user_trajectories[uid] = np.append(
                    user_trajectories[uid], next_state
                )
                new_counts[next_state] += 1
            
            state_counts[step] = new_counts
        
        # Get final states
        user_final_states = np.array([
            user_trajectories[uid][-1] for uid in range(n_users)
        ])
        
        # Create time array
        timestamps = np.arange(n_steps)
        
        return SimulationResult(
            state_counts=state_counts,
            user_trajectories=user_trajectories,
            user_final_states=user_final_states,
            n_users=n_users,
            n_steps=n_steps,
            state_names=self.state_names,
            timestamps=timestamps
        )
    
    def run_sensitivity_analysis(self, n_users: int, n_steps: int,
                                 parameter: str, 
                                 param_values: List[float],
                                 from_state: str, to_state: str,
                                 n_simulations: int = 5) -> Dict:
        """
        Run sensitivity analysis by varying a specific transition probability.
        
        Parameters:
        -----------
        n_users : int
            Number of users per simulation
        n_steps : int
            Number of steps per simulation
        parameter : str
            Description of what parameter varies
        param_values : List[float]
            Values to test
        from_state : str
            Source state
        to_state : str
            Target state
        n_simulations : int
            Number of repetitions per parameter value
        
        Returns:
        --------
        Dict : Results keyed by parameter value
        """
        results = {}
        original_matrix = self.markov_chain.transition_matrix.copy()
        
        from_idx = self.state_names.index(from_state)
        to_idx = self.state_names.index(to_state)
        
        for param_value in param_values:
            # Adjust transition probability
            self.markov_chain.transition_matrix = original_matrix.copy()
            
            # Scale the target transition
            diff = param_value - original_matrix[from_idx, to_idx]
            
            # Adjust other transitions from the same state proportionally
            other_indices = [i for i in range(self.n_states) if i != to_idx]
            other_sum = self.markov_chain.transition_matrix[from_idx, other_indices].sum()
            
            if other_sum > 0:
                adjustment_ratio = diff / other_sum
                self.markov_chain.transition_matrix[from_idx, other_indices] *= (
                    1 - adjustment_ratio
                )
            
            self.markov_chain.transition_matrix[from_idx, to_idx] = param_value
            self.markov_chain.validate_matrix()
            
            # Run simulations
            sim_results = []
            for _ in range(n_simulations):
                result = self.run_simulation(n_users, n_steps)
                metrics = result.get_metrics()
                sim_results.append(metrics)
            
            # Average results
            avg_metrics = {}
            for key in sim_results[0].keys():
                values = [m[key] for m in sim_results]
                avg_metrics[key] = np.mean(values)
                avg_metrics[f"{key}_std"] = np.std(values)
            
            results[param_value] = avg_metrics
        
        # Restore original matrix
        self.markov_chain.transition_matrix = original_matrix
        
        return results


class PoissonArrivalProcess:
    """
    Poisson process for simulating new user arrivals.
    """
    
    def __init__(self, lambda_rate: float):
        """
        Initialize Poisson arrival process.
        
        Parameters:
        -----------
        lambda_rate : float
            Arrival rate (users per time unit)
        """
        self.lambda_rate = lambda_rate
    
    def generate_arrivals(self, time_horizon: int,
                         seed: int = None) -> np.ndarray:
        """
        Generate arrival times using Poisson process.
        
        Parameters:
        -----------
        time_horizon : int
            Total time duration
        seed : int, optional
            Random seed
        
        Returns:
        --------
        np.ndarray : Array of arrival counts at each time step
        """
        if seed is not None:
            np.random.seed(seed)
        
        # Generate number of arrivals at each time step
        arrivals = np.random.poisson(self.lambda_rate, time_horizon)
        
        return arrivals
    
    def cumulative_arrivals(self, arrivals: np.ndarray) -> np.ndarray:
        """
        Compute cumulative arrivals over time.
        
        Parameters:
        -----------
        arrivals : np.ndarray
            Array of arrival counts per time step
        
        Returns:
        --------
        np.ndarray : Cumulative arrivals
        """
        return np.cumsum(arrivals)


class EnhancedSimulationEngine(SimulationEngine):
    """
    Enhanced simulation engine with Poisson arrivals and departure analysis.
    """
    
    def run_simulation_with_arrivals(self, lambda_rate: float, 
                                     n_steps: int,
                                     seed: int = None) -> Tuple[SimulationResult, 
                                                                np.ndarray]:
        """
        Run simulation with Poisson arrivals.
        
        Parameters:
        -----------
        lambda_rate : float
            User arrival rate (new users per time step)
        n_steps : int
            Number of time steps
        seed : int, optional
            Random seed
        
        Returns:
        --------
        Tuple[SimulationResult, np.ndarray] : Simulation results and arrivals
        """
        if seed is not None:
            np.random.seed(seed)
        
        poisson_process = PoissonArrivalProcess(lambda_rate)
        arrivals = poisson_process.generate_arrivals(n_steps, seed)
        
        # Initialize with first batch of arrivals
        initial_state = np.zeros(self.n_states)
        initial_state[0] = 1.0  # All arrivals start as Visitors
        
        n_users_initial = arrivals[0]
        
        # Track all users (including those arriving later)
        all_user_trajectories = {}
        state_counts = np.zeros((n_steps, self.n_states))
        
        # Initialize first batch
        user_id = 0
        for _ in range(n_users_initial):
            all_user_trajectories[user_id] = [0]  # Start as Visitor
            user_id += 1
        
        state_counts[0, 0] = n_users_initial
        
        # Simulate time steps
        for step in range(1, n_steps):
            # Add new arrivals
            n_new = arrivals[step]
            for _ in range(n_new):
                all_user_trajectories[user_id] = [0]  # New users start as Visitors
                user_id += 1
            
            # Transition existing users
            new_counts = np.zeros(self.n_states)
            
            for uid in range(user_id):
                if len(all_user_trajectories[uid]) <= step - 1:
                    continue  # User hasn't arrived yet
                
                current_state = all_user_trajectories[uid][-1]
                
                # Get transition probabilities
                transition_probs = self.markov_chain.transition_matrix[current_state]
                
                # Sample next state
                next_state = np.random.choice(
                    self.n_states,
                    p=transition_probs
                )
                
                all_user_trajectories[uid].append(next_state)
                new_counts[next_state] += 1
            
            state_counts[step] = new_counts
        
        # Convert trajectories to numpy arrays
        for uid in all_user_trajectories:
            all_user_trajectories[uid] = np.array(all_user_trajectories[uid])
        
        total_users = len(all_user_trajectories)
        user_final_states = np.array([
            all_user_trajectories[uid][-1] for uid in range(total_users)
        ])
        
        result = SimulationResult(
            state_counts=state_counts,
            user_trajectories=all_user_trajectories,
            user_final_states=user_final_states,
            n_users=total_users,
            n_steps=n_steps,
            state_names=self.state_names,
            timestamps=np.arange(n_steps)
        )
        
        return result, arrivals
