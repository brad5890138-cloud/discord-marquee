import time
import requests
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

# ==================== 請在此填入您的資料 ====================
WEBHOOK_URL = "https://discord.com/api/webhooks/1517792246374731857/mcJ-748jA7WdM4DD0KsKQg9URpD-BUOCw91-8ksZjOuz4b8-P0FCr7lJYK3cWMkCOKMq"
TEXT = " 歡迎來到🍀噬月陌姎~~！ " 
# ==========================================================

display_width = 15  
extended_text = TEXT + " " * display_width + TEXT

# 背景網頁伺服器（防止 Render 偵測到沒網頁而把主機關閉）
class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_server():
    server = HTTPServer(('0.0.0.0', 8080), KeepAliveHandler)
    server.serve_forever()

def create_and_run_marquee():
    print("🚀 正在您的頻道中發送全新跑馬燈訊息...")
    initial_payload = {
        "embeds": [{
            "title": "📢 系統跑馬燈公告",
            "description": "```\n[ 正在啟動中... ]\n```",
            "color": 16753920
        }]
    }
    
    post_res = requests.post(f"{WEBHOOK_URL}?wait=true", json=initial_payload)
    if post_res.status_code != 200:
        print(f"❌ 發送新訊息失敗，錯誤代碼: {post_res.status_code}")
        return
        
    new_message_id = post_res.json().get("id")
    print(f"✅ 成功創建新訊息！ID 為: {new_message_id}")
    message_url = f"{WEBHOOK_URL}/messages/{new_message_id}"
    
    while True:
        for i in range(len(TEXT) + display_width):
            marquee_frame = extended_text[i : i + display_width]
            payload = {
                "embeds": [{
                    "title": "📢 系統跑馬燈公告",
                    "description": f"```\n[ {marquee_frame} ]\n```",
                    "color": 16753920
                }]
            }
            try:
                res = requests.patch(message_url, json=payload)
                if res.status_code == 429:
                    retry_after = res.json().get("retry_after", 5)
                    time.sleep(retry_after)
            except Exception as e:
                print(f"💥 連線中斷: {e}")
                return
            time.sleep(2.5) 

if __name__ == "__main__":
    # 啟動背景伺服器
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    # 啟動跑馬燈
    create_and_run_marquee()
