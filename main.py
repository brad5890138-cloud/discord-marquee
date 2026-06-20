import time
import requests

# ==================== 請在此填入您的資料 ====================
WEBHOOK_URL = "https://discord.com/api/webhooks/1517792246374731857/mcJ-748jA7WdM4DD0KsKQg9URpD-BUOCw91-8ksZjOuz4b8-P0FCr7lJYK3cWMkCOKMq"
TEXT = " 歡迎來到🍀噬月陌姎~~！ " 
# ==========================================================

display_width = 15  
extended_text = TEXT + " " * display_width + TEXT

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
        print(f"❌ 發送新訊息失敗")
        return
        
    new_message_id = post_res.json().get("id")
    print(f"✅ 成功創建新訊息！ID 為: {new_message_id}")
    message_url = f"{WEBHOOK_URL}/messages/{new_message_id}"
    
    # ─── 關鍵修改：只讓它執行 18000 秒 (5 個小時) ───
    start_time = time.time()
    max_duration = 18000  # 5 小時

    while time.time() - start_time < max_duration:
        for i in range(len(TEXT) + display_width):
            # 隨時檢查是否超時，超時就跳出
            if time.time() - start_time >= max_duration:
                break
                
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
            
    print("⏰ 5小時任務時間到，安全交棒給下一輪 GitHub Actions！")

if __name__ == "__main__":
    create_and_run_marquee()
