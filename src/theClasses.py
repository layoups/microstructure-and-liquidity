from dataclasses import dataclass
import numpy as np
from numpy.random import default_rng

@dataclass
class Asset():
    S: float
    vol: float
    drift: float
    market_impact: float


asset = Asset(
    100,
    0.3,
    0.02,
    1.2
)

print(asset)