from datetime import datetime

import pandas as pd

from service.external.loggs import Loggs
from service.external.pandas_config import PandasConfig

# from service.external.scheduler import Scheduler
from service.external.server import Server
from service.indicators.aroon import Aroon
from service.indicators.ema import Ema
from service.indicators.interface.command import CommandController
from service.indicators.stochastic import Stochastic
from service.indicators.true_range import TrueRange

PandasConfig.apply_settings()

loggs = Loggs().logger


class TradeAnalysis:

    def __init__(self, servicemanager, symbols, today, timeframe=5):
        self.symbol = symbols
        self.df = pd.DataFrame()
        self.today = today
        self.servicemanager = servicemanager
        self.rates = Server(servicemanager, timeframe)
        # self.scheduler = Scheduler()

    def mining_dataframe(self, bars):
        self.df = pd.DataFrame(bars)
        if self.df.index.name != "time":  # Set 'time' as index if not already
            self.df.set_index("time", inplace=True)
        self.df.index = pd.to_datetime(self.df.index, unit="s", utc=True)
        # MT5 não traz a info de tz, qual timezone ele esta retornando, calcule manualmente o shift
        if self.servicemanager.startswith("mt5"):
            self.df["zone"] = self.df.index.tz_convert("Etc/GMT+5")
        else:
            self.df["zone"] = self.df.index.tz_convert("America/Sao_Paulo")
        self.df["zone"] = self.df["zone"].dt.strftime("%H:%M:%S")  # %Y/%m/%d %H:%M:%S
        # Etc/GMT+3, Brazil/East, America/Sao_Paulo

    def process_ticks(self):
        loggs.info(f"{'.,._' * 20}")
        df = self.rates.rates_from(self.symbol)
        if df is None:
            print(f"Não foi possível obter informações sobre o símbolo {self.symbol}")
        elif len(df) <= 20:
            print(
                f"{df} \nWarning: Simbolo tem somente {len(df)} registros,"
                f"menos de 20 necessários para análise com indicadores {self.symbol}\n\n"
            )
        else:
            loggs.info(f"-- Rates of {self.symbol} with {self.servicemanager} in {datetime.now()} --")
            self.mining_dataframe(df)

            self.analyze_indicators()

            self.print_dataframe()

            # self.one_last_dataframe()

            # AdviceTrading(self.df)  # self.df filtered

            # Update Scheduler
            # self.scheduler.renew(self.process_ticks, self.rates.server_time(self.symbol))
        return self.df

    def print_dataframe(self):
        self.df.drop(
            columns=["tick_volume", "spread", "real_volume"],  # "open", "high", "low"
            errors="ignore",
            inplace=True,
        )
        df = self.df.loc[:, ~self.df.columns.isin(["open", "high", "low"])]
        loggs.info(f"-- {self.symbol} Período disponível: {df.index.min()} a {df.index.max()}")
        loggs.info(f"\n{'_' * 10} print_dataframe {'_' * 50}")
        # Reorder columns
        df = df.reindex(columns=["zone", "close", "atrs", "afs", "ema20", "stoch", "aroon"])
        # If false return string vazia
        if self.today:
            loggs.info(df[self.df.index >= pd.Timestamp.now(tz="UTC").normalize()].tail(150).to_string(index=True))
        else:
            loggs.info(df)
        # print(df[["tick_volume"]].sort_values("tick_volume", ascending=False).tail(100))

    def one_last_dataframe(self):
        df = self.df.loc[:, ~self.df.columns.isin(["open", "high", "low"])]
        loggs.info(f"\n{'_' * 10} one_last_dataframe {'_' * 50}")
        # Imprime cada coluna com seu valor na última linha, alinhando com 50 caracteres de forma pythonica
        loggs.info("\n".join(f"{col.ljust(20)}: {val}" for col, val in df.iloc[-1].items()))

    def analyze_indicators(self):
        # Cria uma instância do controlador
        controller = CommandController()
        # Adiciona os comandos ao controlador
        controller.add_command(TrueRange(self.df))
        controller.add_command(Ema(self.df))
        controller.add_command(Aroon(self.df))
        controller.add_command(Stochastic(self.df))
        # Processa os comandos
        controller.process_command()

    # def run(self):
    #     try:
    #         if self.rates.initialize():
    #             self.scheduler.renew(self.process_ticks())
    #         else:
    #             print("Falha na inicialização do serviço.")
    #     except KeyboardInterrupt:
    #         print("Interrupção pelo usuário. Encerrando o programa...")
    #     finally:
    #         self.rates.finalize()
