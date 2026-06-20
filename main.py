import time
import requests
import random

# ==================== 👑 至尊皇家自訂控制面板 ====================
WEBHOOK_URL = "https://discord.com/api/webhooks/1517792246374731857/mcJ-748jA7WdM4DD0KsKQg9URpD-BUOCw91-8ksZjOuz4b8-P0FCr7lJYK3cWMkCOKMq"

# 🌟 完美的對稱星光大標題
luxury_title = "⭐ ✨ 🌟【 噬月陌姎 🪐 皇家公告系統 】🌟 ✨ ⭐"

# ⭕ 【您的原汁原味文字訊息與 4 張專屬 GIF】一字不差，完美配對！
CAMPAIGNS = [
    {
        "top": " 🍀 歡迎來到~~噬月陌姎 ",
        "bottom": " ✨ 一起交友聊天 ",
        "gif": "https://cdn.discordapp.com/attachments/1191437102353744096/1517843596714311822/9154af24aeb650943a3c7e2ee38504b45ca51740d251f95bba16d093acebe5d7.gif?ex=6a37c181&is=6a367001&hm=90ab184a60650d7c6532a64e9ad67d0b34d88fe5e992257857908330a0031e44&"
    },
    {
        "top": " 💬 文字聊天交請至🔐幹話一堆《2026》 ",
        "bottom": " 🤪 這裡人超憨超胖 ",
        "gif": "https://cdn.discordapp.com/attachments/1191437102353744096/1517843596995461120/914721b1ffca10f9b1db81af635774d2fbf15e962e928e9f2579165932febfb2.gif?ex=6a37c181&is=6a367001&hm=4f60687b362dfe0bd64500927af4e902fec35b87e8f07158fc34a707984d42d1&"
    },
    {
        "top": " 🔊 語音聊天請至下方房間 ",
        "bottom": " 👋 歡迎加入 ",
        "gif": "https://cdn.discordapp.com/attachments/1191437102353744096/1517843597427343471/e0fd6e9a768f22ee78382a1306cec42aa193a76a5dd3c7c959fdf816741fad90.gif?ex=6a37c181&is=6a367001&hm=f5dd615cce3602be58f3bef89fe52894e748482138e61941694ba458988f9b45&"
    },
    {
        "top": " 🍀 歡迎來到~~噬月陌姎 ",  
        "bottom": " ✨ 一起交友聊天 ", 
        "gif": "https://cdn.discordapp.com/attachments/1191437102353744096/1517843597746245712/e4c10bc2bf59f55a17dfb839c36c39a276b1ed8cbe6a00e78c7dc219ea5bb7aa.gif?ex=6a37c181&is=6a367001&hm=5d5c317da00fa8dddc2f21ebb3969b4e48f12819a2c6c2a5e362cc9332ded7f2&"
    }
]

STEP_SIZE = 3  
SPEED = 2.0  

# ⚡ 【⏱️ 豪華旗艦核心優化：極速強制限時機制】
# 限制每一張 GIF 與句子「只准在畫面上更新 3 次（約 6 秒）」，時間一到立刻斬斷，強制換下一張圖！
MAX_UPDATES_PER_CAMPAIGN = 3  
# ==============================================================

ANSI_COLORS = ["[1;31m", "[1;32m", "[1;33m", "[1;34m", "[1;35m", "[1;36m", "[1;37m"]
color_end = "[0m"
display_width = 18  

COLOR_CONFIGS = [
    {"text": "[1;33m", "embed": 16776960}, # 黃
    {"text": "[1;32m", "embed": 5763719},  # 綠
    {"text": "[1;35m", "embed": 15418782}, # 粉
    {"text": "[1;36m", "embed": 3447003}   # 藍
]

def run_fast_unlimited_marquee_rotation():
    print("💎 正在發送【6秒極速換圖 + 神龍擺尾版】公告...")
    start_time = time.time()
    max_duration = 18000  
    
    while time.time() - start_time < max_duration:
        for idx, camp in enumerate(CAMPAIGNS):
            top_raw = camp["top"]
            bot_raw = camp["bottom"]
            current_gif = camp["gif"]
            
            color_idx = idx % len(COLOR_CONFIGS)
            color_start = COLOR_CONFIGS[color_idx]["text"]
            current_embed_color = COLOR_CONFIGS[color_idx]["embed"]
            
            # POST 全新畫布與專屬 GIF
            initial_payload = {
                "embeds": [{
                    "title": luxury_title, 
                    "description": "```ansi\n ⚡ 皇家系統正在為專屬公告載入特效與新 GIF...\n```", 
                    "color": current_embed_color,
                    "image": {"url": current_gif}
                }]
            }
            res_post = requests.post(f"{WEBHOOK_URL}?wait=true", json=initial_payload)
            if res_post.status_code != 200:
                continue
                
            current_msg_id = res_post.json().get("id")
            message_url = f"{WEBHOOK_URL}/messages/{current_msg_id}"
            
            top_extended = top_raw + " " * display_width + top_raw
            bot_extended = bot_raw + " " * display_width + bot_raw
            max_len = max(len(top_raw), len(bot_raw)) + display_width
            
            i = 0
            update_count = 0  # 紀錄目前這張圖更新了幾次
            
            # 📐 當字串還沒滾完，且更新次數還沒滿 3 次時，持續滾動文字
            while i < max_len and update_count < MAX_UPDATES_PER_CAMPAIGN:
                if time.time() - start_time >= max_duration:
                    break
                
                c_border1 = random.choice(ANSI_COLORS)
                c_border2 = random.choice(ANSI_COLORS)
                top_frame = top_extended[i : i + display_width]
                bot_pos = (max_len - i) % len(bot_extended)
                bot_frame = bot_extended[bot_pos : bot_pos + display_width]
                if len(bot_frame) < display_width:
                    bot_frame = (bot_frame + " " * display_width)[:display_width]
                
                description_content = (
                    f"```ansi\n"
                    f"{c_border1}▰▰▰▰▰▰ ✨ 星星所向 (✨) ▰▰▰▰▰▰{color_end}\n"
                    f"  {color_start}{top_frame}{color_end}\n"
                    f"{c_border1}▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰{color_end}\n"
                    f"{c_border2}▰▰▰▰▰ ✨ 星河皆是你 (✨) ▰▰▰▰▰{color_end}\n"
                    f"  {color_start}{bot_frame}{color_end}\n"
                    f"{c_border2}▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰{color_end}\n"
                    f"```"
                )
                
                payload = {
                    "embeds": [{
                        "title": luxury_title,
                        "description": description_content,
                        "color": current_embed_color,
                        "image": {"url": current_gif}
                    }]
                }

                try:
                    res = requests.patch(message_url, json=payload)
                    if res.status_code == 429:
                        retry_after = res.json().get("retry_after", 5)
                        time.sleep(retry_after)
                        continue
                except:
                    return

                time.sleep(SPEED)
                i += STEP_SIZE
                update_count += 1 # 累加更新次數
                
                if i >= max_len and (i - STEP_SIZE) < (max_len - 1):
                    i = max_len - 1
            
            # ── 📐 核心重寫 2：滿 6 秒了，強制把這則訊息 DELETE 刪除，光速換下一張圖！ ──
            try:
                requests.delete(message_url)
            except:
                pass
                
    print("⏰ 5小時豪華交棒！")

if __name__ == "__main__":
    run_fast_unlimited_marquee_rotation()
