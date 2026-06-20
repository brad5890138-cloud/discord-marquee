import time
import requests

# ==================== 🎛️ 跑馬燈控制面板 ====================
WEBHOOK_URL = "https://discord.com/api/webhooks/1517792246374731857/mcJ-748jA7WdM4DD0KsKQg9URpD-BUOCw91-8ksZjOuz4b8-P0FCr7lJYK3cWMkCOKMq"

GIF_URL = "https://cdn.discordapp.com/attachments/1191437102353744096/1517791192971214858/9154af24aeb650943a3c7e2ee38504b45ca51740d251f95bba16d093acebe5d7.gif?ex=6a3790b3&is=6a363f33&hm=5c294844fd02dcb5650436b5ed323e07ee1c690301c84246cb2a65109742d80c&"

NEW_TITLE = "✨ 🍀歡迎來到噬月陌姎 ✨"

TEXT_LIST = [
    " 歡迎 ",
    " 來到 ",
    " 噬月陌姎 "
]

# ── 🟢 核心修改 1：滾動文字設定為綠色 ──
TEXT_COLOR = "綠色" 

# ── 🟢 核心修改 2：卡片左側邊框同步設定為綠色數字 ──
EMBED_COLOR = 5763719  

STEP_SIZE = 3  
SPEED = 2.0  
# ==============================================================

COLOR_CODES = {
    "紅色": "[1;31m", "綠色": "[1;32m", "黃色": "[1;33m",
    "藍色": "[1;34m", "粉色": "[1;35m", "青色": "[1;36m", "白色": "[1;37m"
}
color_start = COLOR_CODES.get(TEXT_COLOR, "[1;37m")
color_end = "[0m"
display_width = 15  

def run_green_marquee():
    print("🚀 正在發送【全綠色高亮版】公告...")
    
    # 1. 發送第一則訊息：跑馬燈框
    marquee_payload = {
        "embeds": [{
            "title": NEW_TITLE, 
            "description": "```ansi\n 正在換班初始化...\n```", 
            "color": EMBED_COLOR
        }]
    }
    res_marquee = requests.post(f"{WEBHOOK_URL}?wait=true", json=marquee_payload)
    if res_marquee.status_code != 200:
        print("❌ 跑馬燈建立失敗")
        return
    
    marquee_message_id = res_marquee.json().get("id")
    marquee_message_url = f"{WEBHOOK_URL}/messages/{marquee_message_id}"
    
    # 2. 發送第二則訊息：固定底部的 GIF
    gif_payload = {
        "embeds": [{
            "color": EMBED_COLOR,
            "image": {"url": GIF_URL}
        }]
    }
    requests.post(WEBHOOK_URL, json=gif_payload)
    
    start_time = time.time()
    max_duration = 18000  
    
    while time.time() - start_time < max_duration:
        for current_text in TEXT_LIST:
            extended_text = current_text + " " * display_width + current_text
            total_len = len(current_text) + display_width
            
            i = 0
            while i < total_len:
                if time.time() - start_time >= max_duration:
                    break
                    
                marquee_frame = extended_text[i : i + display_width]
                
                payload = {
                    "embeds": [{
                        "title": "NEW_TITLE",
                        "description": f"```ansi\n{color_start}{marquee_frame}{color_end}\n```",
                        "color": EMBED_COLOR
                    }]
                }

                try:
                    res = requests.patch(marquee_message_url, json=payload)
                    if res.status_code == 429:
                        retry_after = res.json().get("retry_after", 5)
                        time.sleep(retry_after)
                        continue
                except Exception as e:
                    print(f"💥 連線中斷: {e}")
                    return

                time.sleep(SPEED) 
                i += STEP_SIZE  
                
    print("⏰ 5小時安全交棒！")

if __name__ == "__main__":
    run_green_marquee()
