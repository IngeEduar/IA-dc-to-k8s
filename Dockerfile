FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY nlp nlp

RUN python nlp/train_model.py

COPY . .

LABEL org.opencontainers.maintainer.name="Eduar Xavier Avendaño" \
    org.opencontainers.maintainer.email="xavieravendano9@gmail.com" \
    org.opencontainers.image.version="0.0.1" \
    org.opencontainers.image.authors="Kraken.net" \
    org.opencontainers.image.description="IA docker compose to k8s"

CMD ["python", "/app/main.py"]