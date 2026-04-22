FROM joyzoursky/python-selenium:3.9-chrome

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# --timeout 600: Cho phép tool chạy tối đa 10 phút mà không bị giết
# --workers 1: Chỉ chạy 1 worker để tiết kiệm RAM trên gói Free
CMD gunicorn --bind 0.0.0.0:$PORT --timeout 600 --workers 1 --threads 4 app:app