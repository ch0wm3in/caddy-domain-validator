FROM python:slim
LABEL authors="ch0wm3in"
LABEL repo="https://github.com/ch0wm3in/caddy-domain-validator"

RUN useradd --system --create-home --home-dir /home/application --shell /bin/bash \
      --gid root --uid 1000 application

USER application

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app/ ./app

CMD python ./app
