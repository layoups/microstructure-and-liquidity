from dataclasses import dataclass
import numpy as np
from numpy.random import default_rng
import matplotlib.pyplot as plt
from typing import List
from collections.abc import Callable

@dataclass
class Asset:
    S: float
    vol: float
    drift: float
    market_impact: float
    process: Callable[[], float]

@dataclass
class Trader:
    risk_aversion: float
    portfolio: float