[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[//]: # (![Flask logo]&#40;https://flask-ptbr.readthedocs.io/en/latest/_images/logo-full.png&#41;)

#### This project use FastAPI Framework.

[//]: # ()

[//]: # (- Docs: https://flask-ptbr.readthedocs.io/en/latest/)

[//]: # (- Advanced Patterns of Flask: https://flask.palletsprojects.com/en/3.0.x/patterns/)

[//]: # (- Flask is a lightweight WSGI web application framework.)

[//]: # (- Flask depends on the Werkzeug WSGI toolkit, the Jinja template engine, and the Click CLI toolkit.)

### Run

```bash
# Use this
python app.py
# or
uvicorn app:fast --host 0.0.0.0 --port 80

# test
curl http://localhost/trade?service=yf&symbol=NQ=F&today=True
```
