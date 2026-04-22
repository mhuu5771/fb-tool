FROM python:3.9-slim

# Cài đặt các công cụ cần thiết và Google Chrome bản mới nhất
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update && apt-get install -y google-chrome-stable \
    && apt-get clean

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Timeout cao để quét Facebook không bị ngắt
CMD gunicorn --bind 0.0.0.0:$PORT --timeout 600 --workers 1 --threads 4 app:app