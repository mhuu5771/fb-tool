FROM joyzoursky/python-selenium:3.9-chrome

WORKDIR /app

# Cài đặt thư viện cần thiết
RUN pip install flask gunicorn selenium==4.9.0 webdriver-manager

COPY . .

# Timeout 600 để tránh worker bị chết giữa chừng
CMD gunicorn --bind 0.0.0.0:$PORT --timeout 600 --workers 1 --threads 4 app:app