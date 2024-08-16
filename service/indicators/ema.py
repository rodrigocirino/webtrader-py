import numpy as np
import pandas_ta as ta

from service.interface.command import Command
from service.interface.direction import Direction
from service.interface.levels import Level

"""
Confict with Sideways Alert: Se a EMA esta muito proxima, cruzando ou tem um alerta de mercado lateral
devemos operar contra a media movel, não a favor.
"""


class Ema(Command):
    def __init__(self, bars):
        self.df = bars

    def execute(self):
        self.ema()
        self.afastamento()

    def ema(self, s=20):
        ema = self.df["close"].ewm(span=s).mean()
        color_column = "ema" + str(s)
        self.df[color_column] = ""  # Default color
        self.df.loc[self.df["low"] > ema, color_column] = True  # up bullish
        self.df.loc[self.df["high"] < ema, color_column] = False  # down bearish

    def afastamento(self, period=20, atrs=5, limite=2):
        # EMA
        ema = self.df["close"].ewm(span=period).mean()

        # Afastamentos
        afast_high = (self.df["high"] - ema) / ema * 100
        afast_low = (ema - self.df["low"]) / ema * 100
        afast = np.where(self.df["close"] > ema, afast_high, afast_low)

        # ATR Dinâmico
        atr = ta.atr(self.df["high"], self.df["low"], self.df["close"], length=atrs)
        limite_dinamico = (atr / ema) * 100
        self.df["afs"] = abs(afast) / limite_dinamico

        # Verificação
        self.df["afs_activate"] = self.df["afs"] > limite

    @staticmethod
    def analysis(row, signals):
        if row.ema20:
            signals.add_signal(Direction.BULLISH, Level.EMPTY, ["EMA20 Bullish"])
        else:
            signals.add_signal(Direction.BEARISH, Level.EMPTY, ["EMA20 Bearish"])

        if row.close > row.open:
            signals.add_signal(Direction.BULLISH, Level.EMPTY, ["Barra de ALTA"])
        else:
            signals.add_signal(Direction.BEARISH, Level.EMPTY, ["Barra de BAIXA"])

        if row.afs_activate:
            if row.ema20 < row.close:
                direction = Direction.BULLISH
            else:
                direction = Direction.BEARISH
            signals.add_signal(
                direction,
                Level.EMERGENCY,
                [f"{'{:.2f}'.format(row.afs)}x Afastada da EMA ´pts máx`"],
            )
