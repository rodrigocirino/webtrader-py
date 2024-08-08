class MarketSignals:
    def __init__(self):
        self.signals = []

    def add_signal(self, trend, level, signals):
        self.signals.append({"market": [{"trend": trend, "level": level, "signals": signals}]})

    def get_signals(self):
        return self.signals

    def add_info(self, objson):
        self.signals.append(objson)

    def group_market(self, objson):
        grouped_data = {"info": [], "market": {}}

        for item in objson:
            if "info" in item:
                grouped_data["info"] = item["info"]
            elif "market" in item:
                for market in item["market"]:
                    trend = market["trend"]
                    level = market["level"]
                    if trend not in grouped_data["market"]:
                        grouped_data["market"][trend] = {}
                    if level not in grouped_data["market"][trend]:
                        grouped_data["market"][trend][level] = []
                    grouped_data["market"][trend][level].extend(market["signals"])

        return grouped_data
