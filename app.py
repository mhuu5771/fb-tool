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
    final_results = []
    driver = None
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    # Ép đường dẫn binary nếu chạy trên Linux (Render)
    # Đường dẫn chuẩn sau khi cài google-chrome-stable là /usr/bin/google-chrome
    if os.path.exists("/usr/bin/google-chrome"):
        chrome_options.binary_location = "/usr/bin/google-chrome"
    elif os.path.exists("/usr/bin/google-chrome-stable"):
        chrome_options.binary_location = "/usr/bin/google-chrome-stable"

    try:
        # Sử dụng webdriver-manager để tự khớp Driver với bản Chrome đã cài ở Dockerfile
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.set_page_load_timeout(60)
        driver.get(start_url)
        # ... logic quét UID giữ nguyên ...
        
    except Exception as e:
        print(f"LỖI SELENIUM THỰC TẾ: {str(e)}")
    finally:
        if driver:
            driver.quit()
    return final_results

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