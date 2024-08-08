import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from service.advice_trading import AdviceTrading
from service.external.console_log import ConsoleLog
from service.trade_analysis import TradeAnalysis

app = FastAPI()


class TradeData:
    def __init__(self, service, symbols, today):
        self.service = service
        self.symbol = symbols
        self.today = today

    def process(self):
        trade_analysis = TradeAnalysis(self.service, self.symbol, self.today)
        trade_analysis.run()
        # show in logs
        ConsoleLog(trade_analysis)
        # get market json
        json_trade = AdviceTrading(trade_analysis)
        return json_trade.market


@app.get("/trade", response_class=JSONResponse)
def read_user_item(service: str, symbol: str | None = None, today: bool = False):
    return TradeData(service, symbol, today).process()


if __name__ == "__main__":
    # uvicorn app:fast --host 0.0.0.0 --port 80
    # uvicorn.run("__main__:app", host="0.0.0.0", port=80, reload=True, workers=2)
    uvicorn.run(app, port=80)
