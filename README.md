[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<p align="center">
  <a href="https://fastapi.tiangolo.com/pt/" target="blank"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" 
width="300" alt="FastApi Logo" /></a>
</p>

- This project use FastAPI Framework.
    - Docs: https://fastapi.tiangolo.com/pt/)
    - Flask is a lightweight WSGI web application framework.)

### Run

```bash
# Use this
python app.py
# or
uvicorn app:fast --host 0.0.0.0 --port 80

# test
curl http://localhost/trade?service=yf&symbol=NQ=F&today=True
```
