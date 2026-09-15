"""Delegation-proof market design research package."""

from .mechanisms import AuctionResult, run_auction
from .simulation import SimulationConfig, simulate

__all__ = ["AuctionResult", "SimulationConfig", "run_auction", "simulate"]

