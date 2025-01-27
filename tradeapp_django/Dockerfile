FROM python:3.11-slim as builder

ENV PYTHONUNBUFFERED=1
ENV PIPENV_VENV_IN_PROJECT=1

RUN pip install --upgrade pip
RUN pip install pipenv

COPY Pipfile Pipfile.lock  ./

RUN pipenv install --system --deploy


FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends gcc \
    && apt-get install -y netcat-openbsd

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

COPY entrypoint.sh .
RUN chmod a+x ./entrypoint.sh

WORKDIR app/

COPY . .

ENTRYPOINT ["sh",  "entrypoint.sh"]