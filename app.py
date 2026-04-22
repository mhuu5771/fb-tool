from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# Thêm thư viện này để tự động tải driver nếu chạy local
from webdriver_manager.chrome import ChromeDriverManager 
import time
import re
import os

app = Flask(__name__)

def get_phone_api(uid):
    return f"09{str(uid)[-8:]}"

def get_deep_uids(start_url, limit):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    driver = None
    final_results = []
    
    try:
        # KIỂM TRA MÔI TRƯỜNG:
        if os.path.exists("/usr/bin/chromedriver"):
            # Nếu chạy trên RENDER (Docker)
            service = Service(executable_path="/usr/bin/chromedriver")
            chrome_options.binary_location = "/usr/bin/google-chrome"
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            # Nếu chạy dưới LOCAL (Máy của Mạnh)
            # Nó sẽ tự tải driver tương thích với Chrome trên máy bạn
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        driver.set_page_load_timeout(60)
        driver.get(start_url)
        time.sleep(3)
        
        # ... (Giữ nguyên logic quét của Mạnh) ...
        page_source = driver.page_source
        uids_found = re.findall(r'(?:"id":"|id=)([0-9]{13,15})', page_source)
        for uid in uids_found:
            final_results.append({"uid": uid, "phone": get_phone_api(uid)})
            if len(final_results) >= limit: break
                    
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
    try:
        data = request.json
        url = data.get('url')
        limit = int(data.get('limit', 20))
        results = get_deep_uids(url, limit)
        return jsonify(results if results else [])
    except Exception:
        return jsonify([])

if __name__ == '__main__':
    # Render sẽ tự cấp PORT qua biến môi trường
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)