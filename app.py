from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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
    
    # Chỉ định chính xác vị trí Chrome trong Image joyzoursky
    chrome_options.binary_location = "/usr/bin/google-chrome"

    driver = None
    final_results = []
    
    try:
        # TRONG IMAGE NÀY, CHROMEDRIVER LUÔN NẰM Ở ĐÂY:
        service = Service(executable_path="/usr/bin/chromedriver")
        
        # Khởi tạo driver với service và options đã fix cứng path
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get(start_url)
        # Tăng thời gian chờ lên một chút vì Render Free hơi chậm
        time.sleep(6) 
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        page_source = driver.page_source
        uids_found = re.findall(r'(?:"id":"|id=)([0-9]{13,15})', page_source)
        
        seen_uids = set()
        for uid in uids_found:
            if uid not in seen_uids:
                seen_uids.add(uid)
                final_results.append({"uid": uid, "phone": get_phone_api(uid)})
                if len(final_results) >= limit: break
                    
    except Exception as e:
        print(f"LỖI THỰC TẾ: {str(e)}")
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
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)