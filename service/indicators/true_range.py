import numpy as np

from service.interface.command import Command


class TrueRange(Command):
    def __init__(self, bars):
        self.df = bars

    def execute(self):
        """Calculates the ATR (Average True Range) for the last n bars."""
        # Wilder quer calcular a amplitude maior, se a minima for mais distante que a maxima do fechamento anterior use esta, senao a outra
        #  ATR = MME(máx(H – L, H – Cp, Cp – L)) - Cp=previous close
        atrs = self.df.ta.atr(length=50, mamode="ma", col_names="atrs", append=False, percent=False)
        self.is_atr_over(atrs)
        # ATR APLICADO APENAS AO CORPO DA BARRA E NÃO AO TOTAL
        # df['mult_atr'] = (abs(df['open'] - df['close']) >= (atr_multiples * df['ATR']))

    def is_atr_over(self, true_range):
        mult = 1.50
        self.df["atrs"] = np.where(abs(self.df["open"] - self.df["close"]) > (true_range.shift() * mult), True, "")

    @staticmethod
    def analysis(row, signals):
        if row.atrs:
            if row.close > row.open:
                signals.add_signal("bullish", "high", ["Barra Clímax", "COMPRE NÃO VENDA"])
            else:
                signals.add_signal("bearish", "high", ["Barra Clímax", "VENDA NÃO COMPRE"])
