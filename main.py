import time
import requests
import random

# ==================== 👑 至尊皇家自訂控制面板 ====================
WEBHOOK_URL = "https://discord.com/api/webhooks/1517792246374731857/mcJ-748jA7WdM4DD0KsKQg9URpD-BUOCw91-8ksZjOuz4b8-P0FCr7lJYK3cWMkCOKMq"

GIF_URL = "https://cdn.discordapp.com/attachments/1191437102353744096/1517791192971214858/9154af24aeb650943a3c7e2ee38504b45ca51740d251f95bba16d093acebe5d7.gif?ex=6a3790b3&is=6a363f33&hm=5c294844fd02dcb5650436b5ed323e07ee1c690301c84246cb2a65109742d80c&"

# 🌟 完美的對稱星光大標題
luxury_title = "⭐ ✨ 🌟【 噬月陌姎 🪐 皇家公告系統 】🌟 ✨ ⭐"

# ⭕ 原原本本、完全沒有更動的文字訊息（TOP）
TOP_TEXTS = [
    " 🍀 歡迎來到~~噬月陌姎 ",
    " 💬 文字聊天交請至🔐幹話一堆《2026》 ",
    " 🔊 語音聊天請至下方房間 "
]

# ⭕ 原原本本、完全沒有更動的文字訊息（BOTTOM）
BOTTOM_TEXTS = [
    " ✨ 一起交友聊天玩遊戲 ",
    " 🤪 這裡人超憨超胖 ",
    " 👋 歡迎加入!!!! "
]

STEP_SIZE = 3  
SPEED = 2.0  
# ==============================================================

EMBED_NEON_COLORS = [
    15548997, 5763719, 3447003, 10181046, 15418782, 16776960, 16753920
]
ANSI_COLORS = ["[1;31m", "[1;32m", "[1;33m", "[1;34m", "[1;35m", "[1;36m", "[1;37m"]
color_end = "[0m"
display_width = 18  

def run_original_text_combined_marquee():
    print("💎 正在發送【原汁原味文案 + GIF 完美一體化版】公告...")
    
    marquee_payload = {
        "embeds": [{
            "title": luxury_title, 
            "description": "```ansi\n ⚡ 皇家系統正在為專屬公告載入動態特效...\n```", 
            "color": 16777215,
            "image": {"url": GIF_URL}
        }]
    }
    res_marquee = requests.post(f"{WEBHOOK_URL}?wait=true", json=marquee_payload)
    if res_marquee.status_code != 200:
        print("❌ 跑馬燈建立失敗")
        return
    
    marquee_message_id = res_marquee.json().get("id")
    marquee_message_url = f"{WEBHOOK_URL}/messages/{marquee_message_id}"
    
    start_time = time.time()
    max_duration = 18000  
    loop_count = min(len(TOP_TEXTS), len(BOTTOM_TEXTS))
    
    while time.time() - start_time < max_duration:
        for idx in range(loop_count):
            top_raw = TOP_TEXTS[idx]
            bot_raw = BOTTOM_TEXTS[idx]
            
            top_extended = top_raw + " " * display_width + top_raw
            bot_extended = bot_raw + " " * display_width + bot_raw
            
            max_len = max(len(top_raw), len(bot_raw)) + display_width
            i = 0
            
            while i < max_len:
                if time.time() - start_time >= max_duration:
                    break
                
                c_border1 = random.choice(ANSI_COLORS)
                c_border2 = random.choice(ANSI_COLORS)
                c_text1 = random.choice(ANSI_COLORS)
                c_text2 = random.choice(ANSI_COLORS)
                current_embed_color = random.choice(EMBED_NEON_COLORS)
                
                top_frame = top_extended[i : i + display_width]
                bot_pos = (max_len - i) % len(bot_extended)
                bot_frame = bot_extended[bot_pos : bot_pos + display_width]
                if len(bot_frame) < display_width:
                    bot_frame = (bot_frame + " " * display_width)[:display_width]
                
                # 🪐 您的專屬浪漫邊框：「星星所向」與「星河皆是你」
                description_content = (
                    f"```ansi\n"
                    f"{c_border1}◤━━━━ ✨ 星星所向 (✨) ━━━━◥{color_end}\n"
                    f"  {c_text1}{top_frame}{color_end}\n"
                    f"{c_border1}◣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━◢{color_end}\n"
                    f"{c_border2}◤━━━━ ✨ 星河皆是你 (🪐) ━━━◥{color_end}\n"
                    f"  {c_text2}{bot_frame}{color_end}\n"
                    f"{c_border2}◣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━◢{color_end}\n"
                    f"```"
                )
                
                # 🚀 完美的將跑馬燈和 GIF 綁在同一個框框中
                payload = {
                    "embeds": [{
                        "title": luxury_title,
                        "description": description_content,
                        "color": current_embed_color,
                        "image": {"url": GIF_URL}
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
                
                if i >= max_len and (i - STEP_SIZE) < (max_len - 1):
                    i = max_len - 1
                
    print("⏰ 5小時豪華交棒！")

if __name__ == "__main__":
    run_original_text_combined_marquee()
