FROM python:3.6.5-alpine

MAINTAINER DevNet Cloudy Team

# for alpine base image only.
# RUN apk update \
#    && apk add --no-cache --virtual .build-deps gcc musl-dev openssl-dev libffi-dev build-base linux-headers ca-certificates

RUN apk update \
    && apk add --no-cache --virtual .build-deps build-base python3-dev libffi-dev


LABEL Description="DevNet ppe-backend microservice image"

RUN mkdir -p /opt/ppe-backend
WORKDIR /opt/ppe-backend

RUN pip install --upgrade pip

COPY requirements.txt         /opt/ppe-backend/
RUN pip install --no-cache-dir -r requirements.txt

RUN apk del libressl-dev .build-deps

COPY wait-for.sh        /usr/bin/wait-for.sh
COPY wait-for.sh        /scripts/wait-for.sh
COPY *.json        /opt/ppe-backend/
COPY *.py          /opt/ppe-backend/
ADD  common        /opt/ppe-backend/common/
ADD  db            /opt/ppe-backend/db/
ADD  mockups       /opt/ppe-backend/mockups
ADD  endpoints     /opt/ppe-backend/endpoints/
ADD  middleware    /opt/ppe-backend/middleware/
ADD  models        /opt/ppe-backend/models/
ADD  services      /opt/ppe-backend/services/
ADD  public        /opt/ppe-backend/public/

EXPOSE 7030

ENTRYPOINT  ["python", "main.py"]
