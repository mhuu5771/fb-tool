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
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    driver = None
    final_results = []
    
    try:
        # TỰ ĐỘNG KIỂM TRA ĐƯỜNG DẪN CHROME
        render_chrome_path = "/usr/bin/google-chrome"
        render_driver_path = "/usr/bin/chromedriver"

        if os.path.exists(render_chrome_path):
            # CHẠY TRÊN RENDER
            chrome_options.binary_location = render_chrome_path
            service = Service(executable_path=render_driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            # CHẠY DƯỚI LOCAL (MÁY MẠNH)
            # Không cần set binary_location, webdriver-manager tự lo
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.set_page_load_timeout(60)
        driver.get(start_url)
        time.sleep(5) 
        
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
        results = get_deep_uids(data.get('url'), int(data.get('limit', 10)))
        return jsonify(results if results else [])
    except:
        return jsonify([])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)