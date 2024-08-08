from service.market_signals import MarketSignals


class AdviceTrading:

    def __init__(self, trade_analysis):
        self.symbol = trade_analysis.symbol
        self.df = trade_analysis.df
        self.servicemanager = trade_analysis.servicemanager
        self.market = None
        self.advices_trading()

    def advices_trading(self):

        # Only last record
        row = self.df.iloc[-1]

        # Load market signals
        signals = MarketSignals()

        bull_bar = row.close > row.open

        if bull_bar:
            signals.add_signal("bullish", "low", ["Barra de alta 'close > open'"])
        else:
            signals.add_signal("bearish", "low", ["Barra de baixa 'close < open'"])

        if row.ema20:
            signals.add_signal("bullish", "low", ["EMA20 Bullish"])
        else:
            signals.add_signal("bearish", "low", ["EMA20 Bearish"])

        if row.afs:
            if row.ema20:
                signals.add_signal("bullish", "high", ["Afastamento Alto!", "EVITE ENTRADAS"])
            else:
                signals.add_signal("bearish", "high", ["Afastamento Alto!", "EVITE ENTRADAS"])

        if row.aroon == "up":
            signals.add_signal("bullish", "high", ["Aroon Altista"])
        if row.aroon == "down":
            signals.add_signal("bearish", "high", ["Aroon Baixista"])
        if row.aroon == "mid":
            signals.add_signal("both", "high", ["Aroon Transicao"])

        if row.stoch == "up":
            signals.add_signal("bullish", "high", ["Stochastic Altista"])
        if row.stoch == "down":
            signals.add_signal("bearish", "high", ["Stochastic Baixista"])

        if row.atrs:
            if bull_bar:
                signals.add_signal("bullish", "high", ["Barra Clímax", "COMPRE NÃO VENDA"])
            else:
                signals.add_signal("bearish", "high", ["Barra Clímax", "VENDA NÃO COMPRE"])

        objson = {"info": [{"symbol": self.symbol, "service": self.servicemanager, "zone": row.zone, "date": row.name}]}
        signals.add_info(objson)

        self.market = signals.get_signals()
        print(self.market)
