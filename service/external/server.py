from datetime import datetime

import MetaTrader5 as mt5
import yfinance as yf


class Server:

    def __init__(self, service, timeframe):
        self.service = service
        self.timeframe = timeframe  # in minutes
        self.servertime = ""
        self.mt5 = mt5 if (service == "mt5" or service == "mt5_ticks") else None

    def rates_from(self, symbol, num_bars=250):
        # MetaTrader 5 stores tick and bar open time in "Etc/UTC" zone (without the shift)
        if self.service == "mt5":
            return mt5.copy_rates_from_pos(symbol, self.timeframe, 0, num_bars)
        if self.service == "mt5_ticks":
            return mt5.symbol_info(symbol)
        if self.service == "yf":
            return self.online_yf_intraday([symbol])

    def server_time(self, symbol):
        # display symbol properties
        if self.service.startswith("mt5"):
            symbol_info = mt5.symbol_info(symbol)
            return datetime.fromtimestamp(symbol_info.time)
        else:
            return datetime.now()

    def online_yf_intraday(self, stocks):
        # timeframe = interval valid 1m,2m,5m,15m,30m,60m,90m,1h
        # stocks = [stock + ".SA" if not stock.endswith(".SA") and "^" not in stock else stock for stock in stocks]
        # period = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
        df = yf.download(stocks, period="5d", interval=f"{self.timeframe }m")
        df.drop(["Close", "Volume"], axis=1, inplace=True)
        df.index.names = ["time"]  # rename index
        df.rename(columns={"Open": "open", "High": "high", "Low": "low", "Adj Close": "close"}, inplace=True)
        return df

    def initialize(self):
        if self.mt5 is not None:
            if not self.mt5.initialize():
                print(
                    "Failed to initialize MetaTrader 5, error code =",
                    self.mt5.last_error(),
                )
                self.mt5.shutdown()
                return False
            else:
                print("\n\n+ MetaTrader 5 initialized")
                return True
        elif self.service == "yf":
            print("\n\nYfinance initializing.....")
            return True
        else:
            print("Service not supported")
            return False

    def finalize(self):
        if self.service == "mt5":
            print("- MetaTrader 5 shutdown")
            mt5.shutdown()
