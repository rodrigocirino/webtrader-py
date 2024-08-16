import pandas as pd
import pandas_ta as ta

from service.interface.command import Command
from service.interface.direction import Direction
from service.interface.levels import Level

"""
Objetivo: Indicar pontos de entrada numa tendência muito forte.
Cenário: A tendência esta muito forte, demonstrando em indicadores estocásticos que esta sobrecomprado ou sobrevendido, 
são dias de always in long/short desde a abertura e queremos entrar mas estamos com medo de entrar no final da  festa. 
Este indicador pode ajudar a demonstrar que há folego para mais algumas barras, ignorando demais osciladores estocásticos.
"""


class Aroon(Command):
    def __init__(self, bars):
        self.df = bars

    def execute(self):
        # Calcular o Aroon (Aroon Up e Aroon Down) para medir a força da tendência
        aroon = ta.aroon(self.df["high"], self.df["low"], length=14)
        data = pd.DataFrame()
        data["Aroon_Up"] = aroon["AROONU_14"]
        data["Aroon_Down"] = aroon["AROOND_14"]
        # Aplicar a função define_trend_strength para cada par de valores Aroon Up e Aroon Down e criar uma nova coluna
        self.df["aroon"] = data.apply(
            lambda row: self.define_trend_strength(row["Aroon_Up"], row["Aroon_Down"]),
            axis=1,
        )

    def define_trend_strength(self, aroon_up, aroon_down):
        if aroon_up > 80 and aroon_down < 20:
            return "up"
        elif aroon_down > 80 and aroon_up < 20:
            return "down"
        elif 80 >= aroon_up >= 50 > aroon_down:
            return "up_mid"
        elif 80 >= aroon_down >= 50 > aroon_up:
            return "down_mid"
        else:
            return None

    @staticmethod
    def analysis(row, signals):
        if row.aroon == "up":
            signals.add_signal(Direction.BULLISH, Level.WARNING, ["Aroon Altista"])
        if row.aroon == "down":
            signals.add_signal(Direction.BEARISH, Level.WARNING, ["Aroon Baixista"])
        if row.aroon == "up_mid":
            signals.add_signal(Direction.BULLISH, Level.DEBUG, ["Aroon Transicao"])
        if row.aroon == "down_mid":
            signals.add_signal(Direction.BEARISH, Level.DEBUG, ["Aroon Transicao"])
