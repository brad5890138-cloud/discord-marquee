import time
import requests

# ==================== 🎛️ 三色輪播自訂面板 ====================
WEBHOOK_URL = "https://discord.com/api/webhooks/1517792246374731857/mcJ-748jA7WdM4DD0KsKQg9URpD-BUOCw91-8ksZjOuz4b8-P0FCr7lJYK3cWMkCOKMq"

GIF_URL = "https://cdn.discordapp.com/attachments/1191437102353744096/1517791192971214858/9154af24aeb650943a3c7e2ee38504b45ca51740d251f95bba16d093acebe5d7.gif?ex=6a3790b3&is=6a363f33&hm=5c294844fd02dcb5650436b5ed323e07ee1c690301c84246cb2a65109742d80c&"

NEW_TITLE = "✨ 🍀噬月陌姎 ✨"

# 【黃色句子】
TEXT_YELLOW = "新朋友歡迎加入 "

# 【綠色句子】
TEXT_GREEN = " 噬月陌姎 "

# 【粉紅句子】
TEXT_PINK = " 一起聊天玩樂 "

STEP_SIZE = 3  
SPEED = 2.0  
# ==============================================================

# 定義三組顏色對應的 (ANSI文字顏色, EMBED卡片邊框顏色)
COLOR_CONFIGS = [
    {"text": "[1;33m", "embed": 16776960}, # 黃色 (卡片邊框同步變黃)
    {"text": "[1;32m", "embed": 5763719},  # 綠色 (卡片邊框同步變綠)
    {"text": "[1;35m", "embed": 15418782}  # 粉紅 (卡片邊框同步變粉)
]
color_end = "[0m"
display_width = 15  

def run_multicolor_marquee():
    print("🚀 正在發送【三色霓虹輪播版】公告...")
    
    # 1. 發送第一則訊息：跑馬燈框（初始黃色邊框）
    marquee_payload = {
        "embeds": [{
            "title": NEW_TITLE, 
            "description": "```ansi\n 正在換班三色初始化...\n```", 
            "color": COLOR_CONFIGS[0]["embed"]
        }]
    }
    res_marquee = requests.post(f"{WEBHOOK_URL}?wait=true", json=marquee_payload)
    if res_marquee.status_code != 200:
        print("❌ 跑馬燈建立失敗")
        return
    
    marquee_message_id = res_marquee.json().get("id")
    marquee_message_url = f"{WEBHOOK_URL}/messages/{marquee_message_id}"
    
    # 2. 發送第二則訊息：固定底部的 GIF (維持最初綠色邊框)
    gif_payload = {
        "embeds": [{
            "color": COLOR_CONFIGS[1]["embed"],
            "image": {"url": GIF_URL}
        }]
    }
    requests.post(WEBHOOK_URL, json=gif_payload)
    
    start_time = time.time()
    max_duration = 18000  
    
    # 將三句話與三個顏色綁定在一起
    task_list = [
        {"text": TEXT_YELLOW, "color": COLOR_CONFIGS[0]},
        {"text": TEXT_GREEN, "color": COLOR_CONFIGS[1]},
        {"text": TEXT_PINK, "color": COLOR_CONFIGS[2]}
    ]
    
    while time.time() - start_time < max_duration:
        for task in task_list:
            current_text = task["text"]
            color_start = task["color"]["text"]
            current_embed_color = task["color"]["embed"]
            
            extended_text = current_text + " " * display_width + current_text
            total_len = len(current_text) + display_width
            
            i = 0
            while i < total_len:
                if time.time() - start_time >= max_duration:
                    break
                    
                marquee_frame = extended_text[i : i + display_width]
                
                # 每次 PATCH 不僅變更文字，連 Embed 邊框顏色也同步切換！
                payload = {
                    "embeds": [{
                        "title": NEW_TITLE,
                        "description": f"```ansi\n{color_start}{marquee_frame}{color_end}\n```",
                        "color": current_embed_color
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
    run_multicolor_marquee()
