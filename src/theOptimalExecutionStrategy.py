from theSetup import *

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
            self.trader.portfolio * np.sinh(alpha * (self.T - n * self.dt)) / np.sinh(alpha * self.T)
            for n in range(self.N + 1)
        ]
        self.trader.portfolio = self.liquidation_process[-1]

    def show_strategy(self) -> None:
        plt.plot(
            np.linspace(0, self.T, self.N + 1), 
            self.liquidation_process,
            label=r'$ \gamma =$ {}'.format(self.trader.risk_aversion)
        )
        # plt.show

if __name__ == "__main__":
    rng = default_rng()

    asset = Asset(
        45,
        0.6,
        0,
        0,
        0,
        rng.standard_normal
    )

    trader = Trader(1e-5, 200000, 0)

    opt_exec_1 = OptimalExecution(
        asset,
        trader,
        1,
        0.005,
        4e6,
        0.1
    )
    opt_exec_2 = OptimalExecution(
        asset,
        Trader(1e-6, 200000, 0),
        1,
        0.005,
        4e6,
        0.1
    )
    opt_exec_3 = OptimalExecution(
        asset,
        Trader(5e-6, 200000, 0),
        1,
        0.005,
        4e6,
        0.1
    )

    opt_exec_1.optimal_trading_curve()
    opt_exec_1.show_strategy()
    opt_exec_2.optimal_trading_curve()
    opt_exec_2.show_strategy()
    opt_exec_3.optimal_trading_curve()
    opt_exec_3.show_strategy()

    plt.legend(bbox_to_anchor=(1, 1), loc=1, borderaxespad=0.)
    plt.xlabel(r'$t$')
    plt.ylabel("portfolio")
    plt.title('Optimal Trading Curve: \n' + r'$q_0 = 200000,\ T = 1,\ S_0 = 45,\ \sigma = 0.6,\ V = 4 \cdot 10^6,\ \eta = 0.1$')
    plt.show()