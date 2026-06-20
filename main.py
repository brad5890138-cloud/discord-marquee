import time
import requests

# ==================== 🎛️ 跑馬燈控制面板 ====================
WEBHOOK_URL = "https://discord.com/api/webhooks/1517792246374731857/mcJ-748jA7WdM4DD0KsKQg9URpD-BUOCw91-8ksZjOuz4b8-P0FCr7lJYK3cWMkCOKMq"

GIF_URL = "https://cdn.discordapp.com/attachments/1191437102353744096/1517791192971214858/9154af24aeb650943a3c7e2ee38504b45ca51740d251f95bba16d093acebe5d7.gif?ex=6a3790b3&is=6a363f33&hm=5c294844fd02dcb5650436b5ed323e07ee1c690301c84246cb2a65109742d80c&"

TEXT_LIST = [
    " 🚨 這是第一句：伺服器重要公告測試中！ ",
    " 💎 這是第二句：歡迎大家加入，贊助永久開放！ ",
    " ➔ 這是第三句：請大家務必詳閱管理守則！ "
]

TEXT_COLOR = "黃色" 
STEP_SIZE = 3  
SPEED = 2.0  
EMBED_COLOR = 16753920  
# ==============================================================

COLOR_CODES = {
    "紅色": "[1;31m", "綠色": "[1;32m", "黃色": "[1;33m",
    "藍色": "[1;34m", "粉色": "[1;35m", "青色": "[1;36m", "白色": "[1;37m"
}
color_start = COLOR_CODES.get(TEXT_COLOR, "[1;37m")
color_end = "[0m"
display_width = 15  

def run_no_flicker_marquee():
    print("🚀 正在發送【雙層絕不閃爍版】公告...")
    
    # 1. 發送第一則訊息：純文字跑馬燈框
    marquee_payload = {
        "embeds": [{
            "title": "📢 系統進階跑馬燈", 
            "description": "```ansi\n[ 正在換班初始化... ]\n```", 
            "color": EMBED_COLOR
        }]
    }
    res_marquee = requests.post(f"{WEBHOOK_URL}?wait=true", json=marquee_payload)
    if res_marquee.status_code != 200:
        print("❌ 跑馬燈建立失敗")
        return
    
    marquee_message_id = res_marquee.json().get("id")
    marquee_message_url = f"{WEBHOOK_URL}/messages/{marquee_message_id}"
    
    # 2. 發送第二則訊息：固定放底部的 GIF，此後永遠不去 PATCH 編輯它，保證絕不閃爍！
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
                
                # ── 核心修正：payload 不再夾帶任何 image，只更新文字 ──
                payload = {
                    "embeds": [{
                        "title": "📢 系統進階跑馬燈",
                        "description": f"```ansi\n[ {color_start}{marquee_frame}{color_end} ]\n```",
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
    run_no_flicker_marquee()
