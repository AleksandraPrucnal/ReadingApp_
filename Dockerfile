FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    swig \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN apt-get remove -y build-essential swig && apt-get autoremove -y

RUN mkdir /app
COPY ./src /app/src

COPY ./src/data.sql /app/src/data.sql

RUN useradd -m user
USER user

WORKDIR /app

#CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]