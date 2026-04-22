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
    
    # KHÔNG CẦN set binary_location vì Image đã có sẵn đường dẫn chuẩn

    driver = None
    final_results = []
    seen_uids = set()
    queue = [start_url]
    
    try:
        # Trong Image này, chromedriver đã nằm sẵn trong PATH
        driver = webdriver.Chrome(options=chrome_options)
        
        while len(final_results) < limit and queue:
            current_target = queue.pop(0)
            try:
                driver.get(current_target)
                time.sleep(5)
                page_source = driver.page_source
                uids_found = re.findall(r'(?:"id":"|id=)([0-9]{13,15})', page_source)
                for uid in uids_found:
                    if uid not in seen_uids:
                        seen_uids.add(uid)
                        final_results.append({"uid": uid, "phone": get_phone_api(uid)})
                        if len(queue) < limit:
                            queue.append(f"https://www.facebook.com/{uid}")
                        if len(final_results) >= limit: break
            except: continue
    except Exception as e:
        print(f"LỖI THỰC TẾ: {str(e)}")
    finally:
        if driver: driver.quit()
    return final_results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    try:
        data = request.json
        results = get_deep_uids(data.get('url'), int(data.get('limit', 20)))
        return jsonify(results if results else [])
    except: return jsonify([])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)