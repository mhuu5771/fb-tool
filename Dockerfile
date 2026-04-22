# Sử dụng Image chuẩn đã cài sẵn Python và Chrome
FROM joyzoursky/python-selenium:3.9-chrome

WORKDIR /app

# Copy và cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào máy chủ
COPY . .

# Tăng timeout lên 300 giây (5 phút) để tránh lỗi WORKER TIMEOUT
# Chạy 1 worker để tiết kiệm RAM trên Render Free tier
CMD gunicorn --bind 0.0.0.0:$PORT --timeout 300 --workers 1 --threads 4 app:app