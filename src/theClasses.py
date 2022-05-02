from dataclasses import dataclass, field
import numpy as np
from numpy.random import default_rng

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


@dataclass
class OptimalExecution:
    asset: Asset
    trader: Trader
    T: int
    dt: float
    N: int = field(init=False)
    V: int
    execution_cost: float

    def __post_init__(self):
        self.N = int(self.T / self.dt)
        self.T = self.N * self.dt


    def optimal_trading_curve(self) -> list:
        alpha = self.asset.vol * np.sqrt(
            self.trader.risk_aversion * self.V /\
                (2 * self.execution_cost)
        )
        return [
            self.trader.portfolio * np.sinh(alpha * (self.T - n*self.dt)) / np.sinh(alpha * self.T)
            for n in range(self.N + 1)
        ]


# asset = Asset(
#     100,
#     0.3,
#     0.02,
#     1.2,
#     rng.standard_normal
# )

# print(asset)
# print(asset.process())