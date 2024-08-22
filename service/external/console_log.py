import pandas as pd

from service.external.loggs import Loggs

loggs = Loggs().logger


class ConsoleLog:
    def __init__(self, trade_analysis, reclog):
        self.show(trade_analysis, reclog)

    def show(self, trade_analysis, reclog):

        Loggs.disable_temporary_handlers(loggs, reclog)

        df = trade_analysis.df
        df.drop(
            columns=["tick_volume", "spread", "real_volume"],  # "open", "high", "low"
            errors="ignore",
            inplace=True,
        )
        df = df.loc[:, ~df.columns.isin(["open", "high", "low"])]
        loggs.info(f"-- {trade_analysis.symbol} Período disponível: {df.index.min()} a {df.index.max()}")
        loggs.info(f"\n{'_' * 10} print_dataframe {'_' * 50}")
        if trade_analysis.today:
            print(df)
        loggs.info(f"\n{'_' * 10} {trade_analysis.symbol} - TODAY {'_' * 50}")
        loggs.info(df[df.index >= pd.Timestamp.now(tz="UTC").normalize()].tail(150).to_string(index=True))

        # Imprime cada coluna com seu valor na última linha, alinhando com 50 caracteres de forma pythonica
        loggs.info(f"\n{'.' * 10}\t technical analysis \t{'.' * 50}")
        loggs.info("\n".join(f"{col.ljust(20)}: {val}" for col, val in trade_analysis.df.iloc[-2].items()))
