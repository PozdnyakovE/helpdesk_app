FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y netcat-openbsd && \
    apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


CMD ["python", "main.py"]

# COPY startapp.sh /startapp.sh
# RUN chmod +x /startapp.sh
# ENTRYPOINT ["/startapp.sh"]