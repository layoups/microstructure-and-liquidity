from theSetup import *

class MarketMaking:
    def __init__(
        self,
        trader: Trader,
        asset: Asset,
        kappa: float,
        T: float,
        dt: float,
        M: int,
        simulator: Callable[[float], int]
    ) -> None:
        self.trader = trader
        self.asset = asset
        self.kappa = kappa
        self.dt = dt
        self.N = int(T / dt)
        self.T = self.N * self.dt
        self.M = M
        self.Q: List[int] = [trader.portfolio]
        self.X: List[float] = [trader.cash_account]
        self.P: List[float] = [trader.cash_account + trader.portfolio * asset.S]
        self.S: List[float] = [asset.S]
        self.dSa: List[float]
        self.dSb: List[float]
        self.Na: List[int]
        self.Nb: List[int]
        self.simulator = simulator







if __name__ == "__main__":
    rng = default_rng()
    print(rng.binomial(1, 0.5))
    pass