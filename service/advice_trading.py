from service.indicators.aroon import Aroon
from service.indicators.ema import Ema
from service.indicators.stochastic import Stochastic
from service.indicators.true_range import TrueRange
from service.market_signals import MarketSignals


class AdviceTrading:

    def __init__(self, trade_analysis):
        self.trade_analysis = trade_analysis
        self.market = None
        self.advices_trading()

    def put_info(self, row, signals):
        objson = {
            "info": [{
                "symbol": self.trade_analysis.symbol,
                "service": self.trade_analysis.servicemanager,
                "zone": row.zone,
                "date": row.name,
                "ajuste": None,
            }]
        }
        signals.add_info(objson)

    def advices_trading(self):

        # Level.X: empty, trace, debug, info, warning, notice, caution, error, critical, emergency

        # Only last record
        row = self.trade_analysis.df.iloc[-2]

        # Load market signals
        signals = MarketSignals()
        self.put_info(row, signals)

        # EMA Advices
        Ema.analysis(row, signals)

        TrueRange.analysis(row, signals)

        Aroon.analysis(row, signals)

        Stochastic.analysis(row, signals)

        self.market = signals.get_signals()
        self.market = signals.group_market(self.market)
        # self.market = signals.fake_json()
