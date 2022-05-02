from dataclasses import dataclass
import numpy as np
from numpy.random import default_rng
import matplotlib.pyplot as plt

rng = default_rng()

@dataclass
class Asset:
    S: float
    vol: float
    drift: float
    market_impact: float
    process: ...

@dataclass
class Trader:
    risk_aversion: float
    portfolio: int