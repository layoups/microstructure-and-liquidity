from dataclasses import dataclass, field
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

class OptimalExecution:

    def __init__(
        self,
        asset: Asset,
        trader: Trader,
        T: int,
        dt: float, 
        V: int,
        execution_cost: float
    ) -> None:
        self.asset = asset
        self.trader = trader
        self.dt = dt
        self.N = int(T / dt)
        self.T = self.N * self.dt
        self.V = V
        self.execution_cost = execution_cost
        self.liquidation_process = []


    def optimal_trading_curve(self) -> None:
        alpha = self.asset.vol * np.sqrt(
            self.trader.risk_aversion * self.V /\
                (2 * self.execution_cost)
        )
        self.liquidation_process = [
            self.trader.portfolio * np.sinh(alpha * (self.T - n*self.dt)) / np.sinh(alpha * self.T)
            for n in range(self.N + 1)
        ]

    def show(self) -> None:
        plt.plot(
            np.linspace(0, self.T, self.N + 1), 
            self.liquidation_process
        )
        plt.show()

class MarketMaking:
    pass

if __name__ == "__main__":

    asset = Asset(
        45,
        0.6,
        0,
        0,
        rng.standard_normal
    )

    trader = Trader(
        1e-5,
        200000
    )

    opt_exec = OptimalExecution(
        asset,
        trader,
        1,
        0.005,
        4e6,
        0.1
    )

    opt_exec.optimal_trading_curve()
    opt_exec.show()
