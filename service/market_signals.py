class MarketSignals:
    def __init__(self):
        self.signals = []

    def add_signal(self, trend, level, signals):
        self.signals.append({"signals": [{"trend": trend, "level": level, "signals": signals}]})

    def get_signals(self):
        return self.signals

    def add_info(self, objson):
        self.signals.append(objson)

    @classmethod
    def stub_fakes(cls):
        market_signals = MarketSignals()

        initial_data = [
            (
                "bullish",
                "high",
                ["afastamento alto, maior que 2%", "aroon em sobrepreço, se reverter saia imediatamente"],
            ),
            ("bullish", "medium", ["stochastic em transição", "novos dados altistas"]),
            ("bullish", "low", ["ema altista", "vwap altista"]),
            ("bearish", "high", ["novos dados baixistas"]),
            ("bearish", "low", ["ema em transição"]),
        ]

        for trend, level, signals in initial_data:
            market_signals.add_signal(trend, level, signals)

        # Adicionando novos sinais
        market_signals.add_signal("bullish", "medium", ["novos dados altistas"])
        market_signals.add_signal("bearish", "high", ["novos dados baixistas"])

        objson = {"info": [{"symbol": "cls.symbol", "zone": "12:00:00", "date": "2024-08-01 13:30:00+00:00"}]}
        market_signals.add_info(objson)

        return market_signals.get_signals()


if __name__ == "__main__":
    print(MarketSignals.stub_fakes())
