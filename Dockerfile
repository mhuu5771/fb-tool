# Sử dụng Python bản nhẹ
FROM python:3.10-slim

# Cài đặt Google Chrome và các thư viện hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update && apt-get install -y google-chrome-stable \
    && apt-get clean

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy file thư viện và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
COPY . .

# Chạy ứng dụng bằng Gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT --timeout 120 app:app