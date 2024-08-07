class Bearish:
    def __init__(self, level, msg):
        self.level = level
        self.msg = msg

    def to_dict(self):
        return {self.level: self.msg}


class Bullish:
    def __init__(self, level, msg):
        self.level = level
        self.msg = msg

    def to_dict(self):
        return {self.level: self.msg}


class MarketSignals:
    def __init__(self):
        self.bullish_data = []
        self.bearish_data = []

    def add_signal(self, category, level, msg):
        if category == "bullish":
            self.bullish_data.append((level, msg))
        elif category == "bearish":
            self.bearish_data.append((level, msg))

    def get_signals(self):
        bullish_instances = [Bullish(level, msg) for level, msg in self.bullish_data]
        bearish_instances = [Bearish(level, msg) for level, msg in self.bearish_data]

        bullish_dict = {}
        for instance in bullish_instances:
            if instance.level not in bullish_dict:
                bullish_dict[instance.level] = []
            bullish_dict[instance.level].append(instance.msg)

        bearish_dict = {}
        for instance in bearish_instances:
            if instance.level not in bearish_dict:
                bearish_dict[instance.level] = []
            bearish_dict[instance.level].append(instance.msg)

        # dictish = {"bullish": bullish_dict, "bearish": bearish_dict}
        # return json.dumps(dictish, indent=4)
        return {"bullish": bullish_dict, "bearish": bearish_dict}


def run_example():
    market_signals = MarketSignals()

    initial_bullish_data = [
        ("high", "afastamento alto, maior que 2%"),
        ("high", "aroon em sobrepreco, se reverter saia imediatamente"),
        ("medium", "stochastic em transicao"),
        ("low", "ema altista"),
        ("low", "vwap altista"),
    ]

    initial_bearish_data = [("low", "ema em transicao")]

    for level, msg in initial_bullish_data:
        market_signals.add_signal("bullish", level, msg)

    for level, msg in initial_bearish_data:
        market_signals.add_signal("bearish", level, msg)

    # Adicionando novos sinais
    market_signals.add_signal("bullish", "medium", "novos dados altistas")
    market_signals.add_signal("bearish", "high", "novos dados baixistas")

    result = market_signals.get_signals()
    print(result)


if __name__ == "__main__":
    run_example()
