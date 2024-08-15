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

    def afastamento(self, period=20, atrs=5):
        # ema
        ema = self.df["close"].ewm(span=period).mean()
        afs_ema = (self.df["close"] - ema) / ema * 100
        # atr
        atr = ta.atr(self.df["high"], self.df["low"], self.df["close"], length=atrs)
        limite_dinamico = (atr / ema) * 100
        # Baseado no ATR amplitude das barras, quantas vezes o fechamento esta afastado da média,
        # Alta volatilidade e/ou barras muito grandes tendem a fechar mais longe, com mais variacao no afastamento
        self.df["afs"] = abs(afs_ema) / limite_dinamico

    @staticmethod
    def analysis(row, signals):
        if row.ema20:
            signals.add_signal(Direction.BULLISH, Level.INFO, ["EMA20 Bullish"])
        else:
            signals.add_signal(Direction.BEARISH, Level.INFO, ["EMA20 Bearish"])

        if row.close > row.open:
            signals.add_signal(Direction.BULLISH, Level.INFO, ["Barra de alta 'close > open'"])
        else:
            signals.add_signal(Direction.BEARISH, Level.INFO, ["Barra de baixa 'close < open'"])

        if row.afs > 2:
            if row.ema20:
                direction = Direction.BULLISH
            else:
                direction = Direction.BEARISH
            signals.add_signal(
                direction,
                Level.TRACE,
                [f"{'{:.2f}'.format(row.afs)}x Afastamento da EMA20 sobre ATR5"],
            )
