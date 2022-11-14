"""
Tools for analysing the Wikipedia Requests for Adminship network
https://snap.stanford.edu/data/wiki-RfA.html
"""

__version__ = "0.0.0"

from .WikiData import *
from .NetworkAnalyzer import NetworkAnalyzer
from .votes_per_year import plot_votes_per_year
from .cumulative_degree_distribution import plot_degree_distribution
