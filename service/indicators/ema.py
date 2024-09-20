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

    def afastamento(self, period=20, atrs=5):
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
        self.df["afs_p"] = afast


    @staticmethod
    def analysis(row, signals, limite=2):
        if row.ema20:
            signals.add_signal(Direction.BULLISH, Level.EMPTY, ["EMA20 Altista"])
        else:
            signals.add_signal(Direction.BEARISH, Level.EMPTY, ["EMA20 Baixista"])

        if row.close > row.open:
            signals.add_signal(Direction.BULLISH, Level.EMPTY, ["Barra de ALTA"])
        else:
            signals.add_signal(Direction.BEARISH, Level.EMPTY, ["Barra de BAIXA"])

        # Verificação
        afs_activate = row.afs > limite
        if afs_activate:
            if row.ema20 > row.close:
                direction = Direction.BULLISH
                signals.add_signal(
                    direction,
                    Level.NOTICE,
                    ["Tendência forte, NÃO VENDA! Compras são facilitadas pela tendência."],
                )
            else:
                direction = Direction.BEARISH
                signals.add_signal(
                    direction,
                    Level.NOTICE,
                    ["Tendência forte, NÃO COMPRE! Vendas são facilitadas pela tendência."],
                )
            signals.add_signal(
                direction,
                Level.EMERGENCY,
                [
                    f"{'{:.2f}%'.format(row.afs_p)} {'{:.1f}x'.format(row.afs)} Afastada da EMA20.", 
                    "BT forte, possível entrada no fechamento, stop na mínima da barra.",
                    "BT a próxima deve superar sua máxima, e não reverter, indicando continuidade",
                    "Entrada a 50% da BT demonstra fraqueza da tendência, se prepare para stopar."
                
                ],
            )
