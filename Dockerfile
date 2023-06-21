## Stage 1: Build Stage
#FROM python:3.11-slim AS build
#
#ENV PYTHONUNBUFFERED 1
#
#RUN apt-get update && apt-get install -y netcat-openbsd
#COPY Pipfile Pipfile.lock /
#RUN pip install --upgrade pip
#RUN pip install pipenv
#RUN pipenv install --system
#
#COPY ./.env /
#COPY ./tradeapp_django /app
#
## Set execute permission for entrypoint.sh
#RUN chmod +x /app/entrypoint.sh
#
## Stage 2: Final Stage
#FROM python:3.11-alpine
#
#RUN apk --no-cache add netcat-openbsd
#COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
#COPY --from=build /app /app
#
#WORKDIR /app
#
#ENTRYPOINT ["sh", "/app/entrypoint.sh"]




FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat-openbsd
COPY Pipfile Pipfile.lock /
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system

COPY ./.env /
COPY ./entrypoint.sh /
RUN chmod +x entrypoint.sh
COPY ./tradeapp_django /app

ENTRYPOINT ["sh", "/entrypoint.sh"]
