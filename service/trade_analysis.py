from datetime import datetime

import pandas as pd

from service.external.loggs import Loggs
from service.external.pandas_config import PandasConfig
from service.external.server import Server
from service.indicators.aroon import Aroon
from service.indicators.ema import Ema
from service.indicators.stochastic import Stochastic
from service.indicators.true_range import TrueRange
from service.interface.command import CommandController

PandasConfig.apply_settings()

loggs = Loggs().logger


class TradeAnalysis:

    def __init__(self, servicemanager, symbols, today, timeframe):
        self.symbol = symbols
        self.df = pd.DataFrame()
        self.today = today
        self.servicemanager = servicemanager
        self.rates = Server(servicemanager, timeframe)

    def run(self):
        try:
            if self.rates.initialize():
                self.process_ticks()
            else:
                print("Falha na inicialização do serviço.")
        except KeyboardInterrupt:
            print("Interrupção pelo usuário. Encerrando o programa...")
        finally:
            self.rates.finalize()

    def process_ticks(self):
        loggs.info(f"{'.,._' * 20}")
        df = self.rates.rates_from(self.symbol)
        if df is None:
            print(f"\n{'*' * 20}\t{self.symbol} Ativo Não encontrado, verifique o nome do ticker.\t{'*' * 20}\n")
            return None
        elif len(df) <= 20:
            print(
                f"{df} \nWarning: Simbolo tem somente {len(df)} registros,"
                f"menos de 20 necessários para análise com indicadores {self.symbol}\n\n"
            )
        else:
            loggs.info(f"-- Rates of {self.symbol} with {self.servicemanager} in {datetime.now()} --")
            self.mining_dataframe(df)
            self.analyze_indicators()
            self.filter_bars(False)

    def filter_bars(self, filtered):
        if filtered:
            self.df = self.df[self.df.index <= "2024-08-15 23:15:00+00:00"]

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

    def analyze_indicators(self):
        # Cria uma instância do controlador
        controller = CommandController()
        # Adiciona os comandos ao controlador
        controller.add_command(Ema(self.df))
        controller.add_command(Aroon(self.df))
        controller.add_command(TrueRange(self.df))
        controller.add_command(Stochastic(self.df))
        # Processa os comandos
        controller.process_command()
