FROM python:3.12 AS base

ARG PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=500

RUN apt-get update && apt-get install -y gcc
RUN python -m pip install --upgrade pip
    
WORKDIR /src

COPY ./lecture_2 ./lecture_2
COPY ./lecture_3/hw3/requirements.txt ./

RUN pip install -r requirements.txt

FROM base AS dev

CMD ["bash", "-c", "while true; do sleep 1; done"]

FROM base AS local

CMD ["uvicorn", "lecture_2.online_shop.main:app", "--host", "0.0.0.0", "--port", "8080"]