# Sử dụng Image đã cài sẵn Chrome và Python
FROM joyzoursky/python-selenium:3.9-chrome

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy requirements và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code
COPY . .

# Chạy ứng dụng bằng Gunicorn
# Render sẽ truyền cổng qua biến $PORT
CMD gunicorn --bind 0.0.0.0:$PORT --timeout 120 app:app