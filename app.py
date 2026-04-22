from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import os

app = Flask(__name__)

def get_phone_api(uid):
    # Logic tạo số điện thoại giả lập từ UID
    return f"09{str(uid)[-8:]}"

def get_deep_uids(start_url, limit):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    # Với Image joyzoursky, ta không cần set binary_location thủ công
    driver = None
    final_results = []
    seen_uids = set()
    queue = [start_url]
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        while len(final_results) < limit and queue:
            current_target = queue.pop(0)
            try:
                driver.get(current_target)
                time.sleep(3) # Đợi Facebook load
                
                # Cuộn trang để kích hoạt load thêm dữ liệu
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)

                page_source = driver.page_source
                # Regex quét UID Facebook (13-15 chữ số)
                uids_found = re.findall(r'(?:"id":"|id=)([0-9]{13,15})', page_source)
                
                for uid in uids_found:
                    if uid not in seen_uids:
                        seen_uids.add(uid)
                        final_results.append({
                            "uid": uid,
                            "phone": get_phone_api(uid)
                        })
                        # Nếu cần quét sâu thêm, đưa các UID mới vào hàng đợi
                        if len(queue) < limit:
                            queue.append(f"https://www.facebook.com/{uid}")
                        if len(final_results) >= limit: break
            except Exception:
                continue
    except Exception as e:
        print(f"LỖI SELENIUM: {str(e)}")
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