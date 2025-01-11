[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

- This project use FastAPI Framework. Docs: https://fastapi.tiangolo.com/pt/)

#### Server up

```bash
# Use this
python app.py
# or
uvicorn app:fast --host 0.0.0.0 --port 80
```

#### Test

```bash
# Test with 🤩 wsl or linux terminal
curl http://localhost/trade?service=mt5&symbol=MinDolSep24 | jq .
curl http://localhost/trade?service=mt5&symbol=QQQ.US&today=True
curl http://localhost/trade?service=mt5&symbol=Bra50&today=True&log=False

# 🤬 powershell json returns
(curl 'http://localhost/trade?service=yf&symbol=^SPX' -UseBasicParsing).Content | ConvertFrom-Json | 
ConvertTo-Json -Depth 10
```
