FROM python:3.9-slim


WORKDIR /rodeo_server

# Instalar las dependencias necesarias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

    
COPY code/Server /rodeo_server/

RUN pip install -r /rodeo_server/requirements.txt


EXPOSE 5000

#CMD ["gunicorn", "--certfile=cert.pem", "--keyfile=key.pem", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-b", "0.0.0.0:5000", "server:app"]
CMD ["gunicorn", "--certfile=fullchain.pem", "--keyfile=privkey.pem", "-k", "eventlet", "-b", "0.0.0.0:5000", "server:app"]
#CMD ["gunicorn", "-k", "eventlet", "-b", "0.0.0.0:5000", "server:app"]
