FROM python:3.12.8-slim

WORKDIR /app

COPY ./app.py ./app.py
COPY ./requirements.txt ./requirements.txt
COPY ./utils ./utils
COPY ./assets ./assets

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN pip install --no-cache-dir -r requirements.txt gunicorn vizro

EXPOSE 80/tcp

ENTRYPOINT ["gunicorn", "app:server", "run", "--bind", "0.0.0.0:80"]