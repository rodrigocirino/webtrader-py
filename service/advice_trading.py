from service.market_signals import MarketSignals


class AdviceTrading:

    def __init__(self, trade_analysis):
        self.trade_analysis = trade_analysis
        self.market = None
        self.advices_trading()

    def put_info(self, signals, row):
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

        # Only last record
        row = self.trade_analysis.df.iloc[-2]

        # Load market signals
        signals = MarketSignals()
        self.put_info(signals, row)

        bull_bar = row.close > row.open

        if bull_bar:
            signals.add_signal("bullish", "low", ["Barra de alta 'close > open'"])
        else:
            signals.add_signal("bearish", "low", ["Barra de baixa 'close < open'"])

        if row.ema20:
            signals.add_signal("bullish", "low", ["EMA20 Bullish"])
        else:
            signals.add_signal("bearish", "low", ["EMA20 Bearish"])

        if row.afs > 2:
            signals.add_signal(
                "both",
                "high",
                [f"{'{:.2f}'.format(row.afs)}x Afastamento da EMA20 sobre ATR5"],
            )

        if row.aroon == "up":
            signals.add_signal("bullish", "high", ["Aroon Altista"])
        if row.aroon == "down":
            signals.add_signal("bearish", "high", ["Aroon Baixista"])
        if row.aroon == "mid":
            signals.add_signal("both", "medium", ["Aroon Transicao"])

        if row.stoch == "up":
            signals.add_signal("bullish", "high", ["Stochastic Altista"])
        if row.stoch == "down":
            signals.add_signal("bearish", "high", ["Stochastic Baixista"])

        if row.atrs:
            if bull_bar:
                signals.add_signal("bullish", "high", ["Barra Clímax", "COMPRE NÃO VENDA"])
            else:
                signals.add_signal("bearish", "high", ["Barra Clímax", "VENDA NÃO COMPRE"])

        self.market = signals.get_signals()
        print(self.market)
        self.market = signals.group_market(self.market)
        print(self.market)
