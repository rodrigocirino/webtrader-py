from market_signals import MarketSignals
from service.external.loggs import Loggs


class AdviceTrading:

    def __init__(self, bars):
        self.df = bars
        self.market = None
        self.advices_trading()

    def advices_trading(self):

        # ======= return in api ==============

        market_signals = MarketSignals()
        market_signals.add_signal("bullish", "medium", "novos dados altistas")
        market_signals.add_signal("bearish", "high", "novos dados baixistas")
        self.market = market_signals.get_signals()

        # ======= show in logs ==============

        # initialize logs service
        loggs = Loggs().logger

        last_row = self.df.iloc[-1]

        loggs.info(f"\n{'_' * 10} advices_trading {last_row.zone} {'_' * 50}")

        if last_row.close > last_row.open:
            loggs.info(f"Barra de alta")

        if last_row.close < last_row.open:
            loggs.info(f"Barra de baixa")

        if last_row.ema20:
            loggs.info(f"{last_row.ema20.upper().ljust(10)} - EMA20")

        if last_row.afs:
            loggs.info("AFASTAMENTO ALTO! - mais que 0.2% distante da EMA20 <---- EVITE ENTRADAS")

        if last_row.aroon:
            loggs.info(f"AROON {last_row.aroon.upper().ljust(10)}")
            print(f"... [posicionado] Cuidado com sobrecompras e sobrevendas!!, Se reverter saia rapidamente.")

        if last_row.stoch:
            loggs.info(f"Stochastic {last_row.stoch.upper().ljust(10)}.")

        if last_row.atrs:
            loggs.info("ATR Climax - Não entre a mercado.", "#ffff99")
            if last_row.close > last_row.open:
                loggs.info(f"\tBarra de Alta, NÃO VENDA CONTRA, olhe o gráfico! <------- COMPRE NÃO VENDA")
            else:
                loggs.info(f"\tBarra de Baixa, NÃO COMPRE CONTRA, olhe o gráfico! <------- VENDA NÃO COMPRE")
            print(f"... [entradas] Entradas em 50% da barra, Stop máximo no comprimento da barra")
