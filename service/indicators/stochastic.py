import pandas_ta as ta

from service.interface.command import Command

"""Indicator: Stochastic Oscillator (STOCH)"""


class Stochastic(Command):

    def __init__(self, bars):
        self.df = bars

    def execute(self):
        """
        # Using default params
        k (int): The Fast %K period. Default: 14
        d (int): The Slow %K period. Default: 3
        smooth_k (int): The Slow %D period. Default: 3
        mamode (str): See ```help(ta.ma)```. Default: 'sma'
        """
        stoch = ta.stoch(self.df.high, self.df.low, self.df.close, 14, 6, 4)
        if stoch is not None:
            # Renomeando as colunas para nomes mais simples
            k_name, d_name = stoch.columns
            stoch.rename(columns={k_name: "stoch_k", d_name: "stoch_d"}, inplace=True)
            # self.df["stoch_k"] = stoch["stoch_k"].apply(lambda x: round(x, 2))
            # self.df["stoch_d"] = stoch["stoch_d"].round(2)

            self.df["stoch"] = stoch.apply(
                lambda row: self.define_strength(row["stoch_k"], row["stoch_d"]),
                axis=1,
            )

    def define_strength(self, k, d):
        if k > 80 and d > 80:
            return "up"
        elif k < 20 and d < 20:
            return "down"
        else:
            return None

    @staticmethod
    def analysis(row, signals):
        if row.stoch == "up":
            signals.add_signal("bullish", "high", ["Stochastic Altista"])
        if row.stoch == "down":
            signals.add_signal("bearish", "high", ["Stochastic Baixista"])
