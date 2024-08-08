import pandas as pd


class ConsoleLog:
    def __init__(self, trade_analysis):
        self.show(trade_analysis)

    def show(self, trade_analysis):
        # print(f"{'*'*10}\tfull df\t{'*'*10}") print(self.df)

        df = trade_analysis.df
        df.drop(
            columns=["tick_volume", "spread", "real_volume"],  # "open", "high", "low"
            errors="ignore",
            inplace=True,
        )
        df = df.loc[:, ~df.columns.isin(["open", "high", "low"])]
        print(f"-- {trade_analysis.symbol} Período disponível: {df.index.min()} a {df.index.max()}")
        print(f"\n{'_' * 10} print_dataframe {'_' * 50}")
        # Imprime cada coluna com seu valor na última linha, alinhando com 50 caracteres de forma pythonica
        # print("\n".join(f"{col.ljust(20)}: {val}" for col, val in df.iloc[-1].items()))

        if trade_analysis.today:
            print(df[df.index >= pd.Timestamp.now(tz="UTC").normalize()].tail(150).to_string(index=True))
        else:
            print(df)
