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

    def generate_quotes(self) -> tuple:
        temp1 = (1 / self.trader.risk_aversion) * np.log(1 + (self.trader.risk_aversion / self.kappa)) \
            + self.asset.market_impact / 2
        temp2 = (
            (-self.asset.drift / (self.trader.risk_aversion * np.power(self.asset.vol, 2))) + ((2 * self.trader.portfolio + 1) * 0.5)
        ) * np.exp(
            self.kappa * 0.25 * self.asset.market_impact
        ) * np.sqrt(
            (
                (np.power(self.asset.vol, 2) * self.trader.risk_aversion) / (2 * self.kappa * self.asset.liquidity)
            ) * np.power(
                1 + (self.trader.risk_aversion / self.kappa), 1 + (self.kappa / self.trader.risk_aversion)
            )
        )
        return temp1, temp2

    def make_markets(self) -> None:
        for n in range(1, self.N):
            quotes = self.generate_quotes()
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

            self.asset.S = self.S[n]
            self.trader.cash_account = self.X[n]
            self.trader.portfolio = self.Q[n]

    def show_inventory(self) -> None:
        plt.plot(
            np.linspace(0, self.T, self.N), 
            self.Q
        )
        plt.xlabel(r'$t$')
        plt.ylabel("inventory")
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
        plt.xlabel(r'$t$')
        plt.ylabel("S")
        plt.show()

    def show_pnl(self) -> None:
        plt.plot(
            np.linspace(0, self.T, self.N), 
            self.P
        )
        plt.xlabel(r'$t$')
        plt.ylabel("PnL")
        plt.show()

    def show_cash_account(self) -> None:
        plt.plot(
            np.linspace(0, self.T, self.N), 
            self.X
        )
        plt.xlabel(r'$t$')
        plt.ylabel("cash")
        plt.show()



if __name__ == "__main__":
    rng = default_rng()

    asset = Asset(
        100,
        2,
        0.0,
        0.01,
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
        5,
        rng.binomial
    )

    market_maker.make_markets()
    market_maker.show_inventory()
    market_maker.show_asset_price()
    market_maker.show_pnl()
    market_maker.show_cash_account()


    # sim_results = []
    # for i in range(1000):
    #     market_maker.make_markets()
    #     sim_results += [market_maker.P[-1]]

    # plt.hist(sim_results, bins=40)
    # plt.show()

    # print(np.std(sim_results))
    
