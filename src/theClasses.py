from dataclasses import dataclass
import numpy as np
from numpy.random import default_rng

rng = default_rng()

@dataclass
class Asset():
    S: float
    vol: float
    drift: float
    market_impact: float
    process: ...

@dataclass
class Trader():
    risk_aversion: float
    portfolio: int


asset = Asset(
    100,
    0.3,
    0.02,
    1.2,
    rng.standard_normal
)

print(asset)
print(asset.process())