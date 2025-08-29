FROM python:3.8-slim

LABEL authors="SHI"

WORKDIR /app

COPY . /app

RUN apt-get update

RUN apt-get install -y wget unzip libnss3 libgconf-2-4 libfontconfig1 libxss1 libzbar0

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get clean

ENTRYPOINT ["/bin/bash", "./run.sh"]