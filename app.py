from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import os

app = Flask(__name__)

def get_phone_api(uid):
    return f"09{str(uid)[-8:]}"

def get_deep_uids(start_url, limit):
    # PHẢI có dòng này ở ngay đầu hàm
    final_results = [] 
    driver = None
    
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Nếu dùng Buildpack trên Render, đừng set binary_location thủ công nữa
        # Cứ để webdriver-manager tự lo
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get(start_url)
        time.sleep(5)
        # ... logic quét của bạn ...
        
    except Exception as e:
        print(f"LỖI SELENIUM: {e}")
        # Không cần làm gì cả, hàm sẽ trả về mảng rỗng [] thay vì sập lỗi 500
    finally:
        if driver:
            driver.quit()
            
    return final_results # Luôn luôn trả về, dù mảng rỗng hay có data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    results = get_deep_uids(data.get('url'), int(data.get('limit', 10)))
    return jsonify(results)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)