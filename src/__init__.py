"""
Streaming Platform Engagement Simulator
Main package for Markov chain user behavior modeling
"""

__version__ = "1.0.0"
__author__ = "Data Scientist"
__description__ = "Markov Chain-based User Behavior Simulator for Streaming Platforms"

from src.markov_model import MarkovChainModel
from src.simulation import SimulationEngine, EnhancedSimulationEngine
from src.visualization import MarkovChainVisualizer, SimulationVisualizer

__all__ = [
    'MarkovChainModel',
    'SimulationEngine',
    'EnhancedSimulationEngine',
    'MarkovChainVisualizer',
    'SimulationVisualizer'
]
