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
        self.dSa: List[float] = []
        self.dSb: List[float] = []
        self.Na: List[int] = [0]
        self.Nb: List[int] = [0]
        self.simulator = simulator

    def generate_quotes(self) -> tuple:
        temp1 = (1 / self.trader.risk_aversion) * np.log(1 + (self.trader.risk_aversion / self.kappa)) + self.asset.market_impact / 2
        temp2 = ((-self.asset.drift / (self.trader.risk_aversion * np.power(self.asset.vol, 2))) + ((2 * self.Q[-1] + 1) * 0.5)) \
            * np.exp(self.kappa * 0.25 * self.asset.market_impact) \
                * np.sqrt(
                    ((np.power(self.asset.vol, 2) * self.trader.risk_aversion) / (2 * self.kappa * self.asset.liquidity)) * np.power(
                        1 + (self.trader.risk_aversion / self.kappa), 1 + (self.kappa / self.trader.risk_aversion)
                    )
                )
        return temp1, temp2

    def make_markets(self) -> None:
        for n in range(1, self.N + 1):
            quotes = self.generate_quotes()
            self.dSa[n-1] = quotes[0] + quotes[1]
            self.dSb[n-1] = quotes[0] - quotes[1]

            prob_a = self.asset.liquidity * np.exp(-self.kappa * self.dSa[n-1]) * self.dt
            self.Na[n] = self.simulator(prob_a) if self.Q[n-1] > -self.M else 0

            prob_b = self.asset.liquidity * np.exp(-self.kappa * self.dSb[n-1]) * self.dt
            self.Nb[n] = self.simulator(prob_b) if self.Q[n-1] < self.M else 0

            self.S[n] = self.asset.drift * self.dt \
                + self.asset.vol * np.sqrt(self.dt) * self.asset.process() \
                    + self.asset.market_impact * self.Na[n-1] \
                        - self.asset.market_impact * self.Nb[n-1]
            self.Q[n] = self.Nb[n] - self.Na[n]
            self.X[n] = self.X[n-1] \
                + (self.S[n] + self.dSa[n-1]) * self.Na[n] \
                    - (self.S[n] - self.dSb[n-1]) * self.Nb[n]
            self.P[n] = self.X[n] + self.Q[n] * self.S[n]








if __name__ == "__main__":
    rng = default_rng()
    print(rng.binomial(1, 0.5))