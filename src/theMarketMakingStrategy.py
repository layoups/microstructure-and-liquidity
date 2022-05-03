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
        simulator: Callable[[int, float], int]
    ) -> None:
        self.trader = trader
        self.asset = asset
        self.kappa = kappa
        self.dt = dt
        self.N = int(T / dt)
        self.T = self.N * self.dt
        self.M = M
        self.Q: List[int] = np.concatenate(([trader.portfolio], np.zeros(self.N - 1)), axis=0)
        self.X: List[float] = np.concatenate(([trader.cash_account], np.zeros(self.N - 1)), axis=0)
        self.P: List[float] = np.concatenate(([trader.cash_account + trader.portfolio * asset.S], np.zeros(self.N - 1)), axis=0)
        self.S: List[float] = np.concatenate(([asset.S], np.zeros(self.N - 1)), axis=0)
        self.dSa: List[float] = np.zeros(self.N)
        self.dSb: List[float] = np.zeros(self.N)
        self.Na: List[int] = np.zeros(self.N)
        self.Nb: List[int] = np.zeros(self.N)
        self.simulator = simulator

    def generate_quotes(self, n) -> tuple:
        temp1 = (1 / self.trader.risk_aversion) * np.log(1 + (self.trader.risk_aversion / self.kappa)) + self.asset.market_impact / 2
        temp2 = ((-self.asset.drift / (self.trader.risk_aversion * np.power(self.asset.vol, 2))) + ((2 * self.Q[n - 1] + 1) * 0.5)) \
            * np.exp(self.kappa * 0.25 * self.asset.market_impact) \
                * np.sqrt(
                    ((np.power(self.asset.vol, 2) * self.trader.risk_aversion) / (2 * self.kappa * self.asset.liquidity)) * np.power(
                        1 + (self.trader.risk_aversion / self.kappa), 1 + (self.kappa / self.trader.risk_aversion)
                    )
                )
        return temp1, temp2

    def make_markets(self) -> None:
        for n in range(1, self.N):
            quotes = self.generate_quotes(n)
            self.dSa[n-1] = quotes[0] + quotes[1]
            self.dSb[n-1] = quotes[0] - quotes[1]

            prob_a = self.asset.liquidity * np.exp(-self.kappa * self.dSa[n-1]) * self.dt
            Na = self.simulator(1, prob_a) if self.Q[n-1] > -self.M else 0
            self.Na[n] = self.Na[n-1] + Na

            prob_b = self.asset.liquidity * np.exp(-self.kappa * self.dSb[n-1]) * self.dt
            Nb = self.simulator(1, prob_b) if self.Q[n-1] < self.M else 0
            self.Nb[n] = self.Nb[n-1] + Nb

            self.S[n] = self.S[n-1] \
                + self.asset.drift * self.dt \
                    + self.asset.vol * np.sqrt(self.dt) * self.asset.process() \
                        + self.asset.market_impact * Na \
                            - self.asset.market_impact * Nb
            self.Q[n] = self.Nb[n] - self.Na[n]
            self.X[n] = self.X[n-1] \
                + (self.S[n] + self.dSa[n-1]) * Na \
                    - (self.S[n] - self.dSb[n-1]) * Nb
            self.P[n] = self.X[n] + self.Q[n] * self.S[n]

    def show_inventory(self) -> None:
        plt.plot(
            np.linspace(0, self.T, self.N), 
            self.Q
        )
        plt.show()

    def show_asset_price(self) -> None:
        plt.plot(
            np.linspace(0, self.T, self.N), 
            self.S
        )
        plt.plot(
            np.linspace(0, self.T, self.N), 
            self.dSa + self.S
        )
        plt.plot(
            np.linspace(0, self.T, self.N), 
            self.S - self.dSb
        )
        plt.show()

    def show_pnl(self) -> None:
        plt.plot(
            np.linspace(0, self.T, self.N), 
            self.P
        )
        plt.show()

    def show_cash_account(self) -> None:
        plt.plot(
            np.linspace(0, self.T, self.N), 
            self.X
        )
        plt.show()



if __name__ == "__main__":
    rng = default_rng()

    asset = Asset(
        100,
        0.2,
        0.0,
        0,
        140,
        rng.standard_normal
    )

    trader = Trader(1e-1, 0, 0)

    market_maker = MarketMaking(
        trader,
        asset,
        1.5,
        1,
        0.005,
        10,
        rng.binomial
    )

    market_maker.make_markets()
    print(market_maker.P[-1])


    market_maker.show_inventory()
    market_maker.show_asset_price()
    market_maker.show_pnl()
    market_maker.show_cash_account()
