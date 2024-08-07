import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from service.indicators.advice_trading import AdviceTrading
from trade_analysis import TradeAnalysis

app = FastAPI()


class TradeData:
    def __init__(self, service, symbols, today):
        self.service = service
        self.symbol = symbols
        self.today = today

    def process(self):
        tick_receiver = TradeAnalysis(self.service, self.symbol, self.today)
        bars = tick_receiver.process_ticks()
        return AdviceTrading(bars)


# http://localhost/trade?service=yf&symbol=NQ=F&today=True
@app.get("/trade", response_class=JSONResponse)
def read_user_item(service: str, symbol: str | None = None, today: bool = False):
    td = TradeData(service, symbol, today).process()
    return td.market


@app.get("/")
def ping():
    return True


if __name__ == "__main__":
    # uvicorn app:fast --host 0.0.0.0 --port 80
    uvicorn.run("__main__:app", host="0.0.0.0", port=80, reload=True, workers=2)
