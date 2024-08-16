import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from service.advice_trading import AdviceTrading
from service.external.console_log import ConsoleLog
from service.trade_analysis import TradeAnalysis

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],  # important for cors
)


class TradeData:
    def __init__(self, service, symbols, today, log):
        self.service = service
        self.symbol = symbols
        self.today = today
        self.reclog = log

    def process(self):
        trade_analysis = TradeAnalysis(self.service, self.symbol, self.today)
        trade_analysis.run()
        # show in logs
        ConsoleLog(trade_analysis, self.reclog)
        # get market json
        json_trade = AdviceTrading(trade_analysis)
        return json_trade.market


@app.get("/trade", response_class=JSONResponse)
def read_user_item(service: str, symbol: str | None = None, today: bool = False, log: bool = True):
    return TradeData(service, symbol, today, log).process()


if __name__ == "__main__":
    # uvicorn app:fast --host 0.0.0.0 --port 80
    uvicorn.run("__main__:app", host="0.0.0.0", port=80, reload=True, workers=2)
    # uvicorn.run(app, port=80)
