FROM python:3.9-slim


WORKDIR /rodeo_engine

ENV PYTHONHTTPSVERIFY=0

# Instalar las dependencias necesarias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY code/Engine /rodeo_engine/

RUN pip install -r /rodeo_engine/requirements.txt


CMD ["python", "engine.py"]
