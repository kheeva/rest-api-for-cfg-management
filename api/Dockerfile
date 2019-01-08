FROM python:3.5.6
MAINTAINER Oleg <oleg.ivliev1@gmail.com>
WORKDIR /workdir
COPY requirements.txt /workdir
RUN pip install -r requirements.txt
ENTRYPOINT ["gunicorn", "main:app", "-k aiohttp.worker.GunicornWebWorker", "-b localhost:8081"]
