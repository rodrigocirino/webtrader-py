import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from service.advice_trading import AdviceTrading
from service.trade_analysis import TradeAnalysis

app = FastAPI()


class TradeData:
    def __init__(self, service, symbols, today):
        self.service = service
        self.symbol = symbols
        self.today = today

    def process(self):
        tick_receiver = TradeAnalysis(self.service, self.symbol, self.today)
        bars = tick_receiver.process_ticks()
        return AdviceTrading(self.symbol, bars)


@app.get("/trade", response_class=JSONResponse)
def read_user_item(service: str, symbol: str | None = None, today: bool = False):
    td = TradeData(service, symbol, today).process()
    return td.market


if __name__ == "__main__":
    # uvicorn app:fast --host 0.0.0.0 --port 80
    uvicorn.run("__main__:app", host="0.0.0.0", port=80, reload=True, workers=2)
