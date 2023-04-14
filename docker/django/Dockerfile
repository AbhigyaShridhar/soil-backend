FROM python:3.9

USER root

ENV TERM linux
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y apt-utils
RUN apt-get install -y binutils && \
    apt-get install -y libproj-dev && \
    apt-get install -y gdal-bin && \
    apt-get install -y libgdal-dev && \
    apt-get install -y libsqlite3-mod-spatialite && \
    apt-get install -y libspatialite-dev

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
