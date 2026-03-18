"""
Markov Chain Model for Streaming Platform Engagement & Churn Analysis
Author: Data Scientist
Date: 2024

This module implements core Markov chain functionality for modeling user
behavior transitions across engagement states in a streaming platform.
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict, List
import warnings


class MarkovChainModel:
    """
    A comprehensive Markov Chain model for streaming platform user behavior.
    
    States:
    - Visitor: Free trial or non-registered user
    - Browsing: User browsing content but not watching
    - Watching: User actively watching content
    - Binge_Watching: User engaged in extended viewing sessions
    - Subscriber: Paid subscriber
    - Churn: User has left the platform
    """
    
    def __init__(self, transition_matrix: np.ndarray = None, 
                 state_names: List[str] = None):
        """
        Initialize the Markov Chain model.
        
        Parameters:
        -----------
        transition_matrix : np.ndarray, optional
            6x6 transition probability matrix. Rows sum to 1.
        state_names : List[str], optional
            Names of states corresponding to matrix indices
        """
        self.state_names = state_names or [
            "Visitor", "Browsing", "Watching", 
            "Binge Watching", "Subscriber", "Churn"
        ]
        self.n_states = len(self.state_names)
        
        if transition_matrix is not None:
            self.transition_matrix = transition_matrix
            self.validate_matrix()
        else:
            self.transition_matrix = np.eye(self.n_states)
        
        self.steady_state = None
        self.eigenvalues = None
        self.eigenvectors = None
    
    def validate_matrix(self) -> bool:
        """
        Validate that the transition matrix is stochastic (rows sum to 1).
        
        Returns:
        --------
        bool : True if valid, raises ValueError otherwise
        """
        if self.transition_matrix.shape != (self.n_states, self.n_states):
            raise ValueError(
                f"Matrix shape {self.transition_matrix.shape} does not match "
                f"expected shape ({self.n_states}, {self.n_states})"
            )
        
        row_sums = self.transition_matrix.sum(axis=1)
        
        if not np.allclose(row_sums, 1.0, atol=1e-10):
            raise ValueError(
                f"Transition matrix rows do not sum to 1. "
                f"Row sums: {row_sums}"
            )
        
        if np.any(self.transition_matrix < 0) or np.any(self.transition_matrix > 1):
            raise ValueError(
                "All transition probabilities must be between 0 and 1"
            )
        
        print("✓ Transition matrix validation passed!")
        return True
    
    def compute_next_state(self, current_state: np.ndarray) -> np.ndarray:
        """
        Compute the next state distribution given current state.
        
        Mathematical operation: v(t+1) = v(t) * P
        
        Parameters:
        -----------
        current_state : np.ndarray
            Current state distribution (probability vector, shape: (n_states,))
        
        Returns:
        --------
        np.ndarray : Next state distribution (shape: (n_states,))
        """
        if current_state.shape != (self.n_states,):
            raise ValueError(
                f"State vector shape {current_state.shape} does not match "
                f"expected shape ({self.n_states},)"
            )
        
        next_state = current_state @ self.transition_matrix
        return next_state / next_state.sum()  # Normalize
    
    def compute_steady_state(self, method: str = "power", 
                            max_iterations: int = 10000,
                            tolerance: float = 1e-10) -> np.ndarray:
        """
        Compute the steady-state distribution (stationary distribution).
        
        A steady-state π satisfies: π = π * P
        This represents the long-run proportion of users in each state.
        
        Parameters:
        -----------
        method : str, default="power"
            Method to compute steady state:
            - "power": Power iteration method (faster for large matrices)
            - "eigen": Eigenvalue decomposition (more robust)
        max_iterations : int
            Maximum iterations for power method
        tolerance : float
            Convergence tolerance
        
        Returns:
        --------
        np.ndarray : Steady-state distribution (shape: (n_states,))
        """
        if method == "power":
            self.steady_state = self._power_iteration(max_iterations, tolerance)
        elif method == "eigen":
            self.steady_state = self._eigenvalue_method()
        else:
            raise ValueError(f"Unknown method: {method}")
        
        return self.steady_state
    
    def _power_iteration(self, max_iterations: int, 
                        tolerance: float) -> np.ndarray:
        """
        Compute steady state using power iteration method.
        
        This method iteratively applies the transition matrix to an initial
        distribution until convergence.
        """
        # Start with uniform distribution
        state = np.ones(self.n_states) / self.n_states
        
        for iteration in range(max_iterations):
            next_state = self.compute_next_state(state)
            
            # Check convergence
            if np.allclose(state, next_state, atol=tolerance):
                print(f"✓ Power iteration converged in {iteration} iterations")
                return next_state
            
            state = next_state
        
        warnings.warn(
            f"Power iteration did not converge after {max_iterations} iterations"
        )
        return state
    
    def _eigenvalue_method(self) -> np.ndarray:
        """
        Compute steady state using eigenvalue decomposition.
        
        The steady state is the left eigenvector of P corresponding to
        eigenvalue 1.
        """
        # Compute eigenvalues and eigenvectors of transpose
        eigenvalues, eigenvectors = np.linalg.eig(
            self.transition_matrix.T
        )
        
        self.eigenvalues = eigenvalues
        self.eigenvectors = eigenvectors
        
        # Find eigenvector corresponding to eigenvalue 1
        idx = np.argmax(np.abs(eigenvalues - 1.0) < 1e-10)
        
        steady_state = np.real(eigenvectors[:, idx])
        steady_state = steady_state / steady_state.sum()
        
        print("✓ Steady state computed using eigenvalue decomposition")
        return steady_state
    
    def check_ergodicity(self) -> Dict[str, bool]:
        """
        Check if the Markov chain is ergodic (aperiodic and irreducible).
        
        An ergodic chain has a unique steady-state distribution regardless
        of initial conditions, which is important for our analysis.
        
        Returns:
        --------
        Dict[str, bool] : Dictionary with ergodicity checks
        """
        checks = {
            "is_irreducible": self._is_irreducible(),
            "is_aperiodic": self._is_aperiodic(),
            "has_unique_steady_state": self._has_unique_steady_state()
        }
        
        checks["is_ergodic"] = all(checks.values())
        
        return checks
    
    def _is_irreducible(self) -> bool:
        """
        Check if all states communicate with each other (irreducibility).
        Uses accessibility matrix method.
        """
        # Compute powers of transition matrix to check accessibility
        P_power = self.transition_matrix.copy()
        accessibility = (P_power > 0).astype(int)
        
        for _ in range(self.n_states - 1):
            P_power = P_power @ self.transition_matrix
            accessibility = accessibility + (P_power > 0).astype(int)
        
        # Chain is irreducible if every state can reach every other state
        return np.all(accessibility > 0)
    
    def _is_aperiodic(self) -> bool:
        """
        Check if the chain is aperiodic (no cycle pattern).
        A sufficient condition: presence of self-loop (diagonal entry > 0).
        """
        return np.any(np.diag(self.transition_matrix) > 0)
    
    def _has_unique_steady_state(self) -> bool:
        """
        Check if unique steady state exists by verifying eigenvalue 1 has
        multiplicity 1 and all other eigenvalues have absolute value < 1.
        """
        if self.eigenvalues is None:
            self._eigenvalue_method()
        
        # Count eigenvalues equal to 1 (within tolerance)
        count_one = np.sum(np.abs(self.eigenvalues - 1.0) < 1e-10)
        
        # Check all other eigenvalues have magnitude < 1
        other_eigenvalues = self.eigenvalues[np.abs(self.eigenvalues - 1.0) >= 1e-10]
        all_less_than_one = np.all(np.abs(other_eigenvalues) < 1.0 - 1e-10)
        
        return count_one == 1 and all_less_than_one
    
    def simulate_user_trajectory(self, n_steps: int, 
                                initial_state_idx: int = 0) -> np.ndarray:
        """
        Simulate a single user's trajectory through states.
        
        Parameters:
        -----------
        n_steps : int
            Number of time steps to simulate
        initial_state_idx : int
            Starting state index (default: 0 = Visitor)
        
        Returns:
        --------
        np.ndarray : Array of state indices visited (shape: (n_steps,))
        """
        trajectory = np.zeros(n_steps, dtype=int)
        trajectory[0] = initial_state_idx
        
        # Use row-wise stochastic sampling
        current_state = initial_state_idx
        
        for t in range(1, n_steps):
            # Get transition probabilities from current state
            transition_probs = self.transition_matrix[current_state]
            
            # Sample next state
            next_state = np.random.choice(
                self.n_states, 
                p=transition_probs
            )
            trajectory[t] = next_state
            current_state = next_state
        
        return trajectory
    
    def get_transition_dataframe(self) -> pd.DataFrame:
        """
        Get transition matrix as a formatted DataFrame.
        
        Returns:
        --------
        pd.DataFrame : Transition matrix with state names as indices/columns
        """
        return pd.DataFrame(
            self.transition_matrix,
            index=self.state_names,
            columns=[f"to_{s.lower().replace(' ', '_')}" for s in self.state_names]
        )
    
    def set_custom_matrix(self, matrix_dict: Dict) -> None:
        """
        Set custom transition probabilities from a dictionary.
        
        Parameters:
        -----------
        matrix_dict : Dict
            Dictionary mapping (from_state, to_state) tuples to probabilities
        """
        custom_matrix = np.zeros((self.n_states, self.n_states))
        
        for (from_state, to_state), prob in matrix_dict.items():
            from_idx = self.state_names.index(from_state)
            to_idx = self.state_names.index(to_state)
            custom_matrix[from_idx, to_idx] = prob
        
        self.transition_matrix = custom_matrix
        self.validate_matrix()


def load_transition_matrix_from_csv(filepath: str) -> Tuple[np.ndarray, List[str]]:
    """
    Load transition matrix from CSV file.
    
    Parameters:
    -----------
    filepath : str
        Path to CSV file with transition matrix
    
    Returns:
    --------
    Tuple[np.ndarray, List[str]] : Transition matrix and state names
    """
    df = pd.read_csv(filepath, index_col=0)
    state_names = df.index.tolist()
    matrix = df.values
    
    return matrix, state_names


# Default transition matrix as backup
DEFAULT_TRANSITION_MATRIX = np.array([
    [0.3,  0.5,  0.1,  0.0,  0.0,  0.1],   # Visitor
    [0.1,  0.4,  0.3,  0.1,  0.0,  0.1],   # Browsing
    [0.05, 0.15, 0.3,  0.25, 0.15, 0.1],   # Watching
    [0.02, 0.03, 0.1,  0.45, 0.3,  0.1],   # Binge Watching
    [0.0,  0.0,  0.05, 0.15, 0.75, 0.05],  # Subscriber
    [0.0,  0.0,  0.0,  0.0,  0.0,  1.0]    # Churn (absorbing state)
])
