import time
import requests
import random

# ==================== 👑 四軌四圖至尊自訂面板 ====================
WEBHOOK_URL = "https://discord.com/api/webhooks/1517792246374731857/mcJ-748jA7WdM4DD0KsKQg9URpD-BUOCw91-8ksZjOuz4b8-P0FCr7lJYK3cWMkCOKMq"

# 🌟 完美的對稱星光大標題
luxury_title = "⭐ ✨ 🌟【 噬月陌姎 🪐 皇家公告系統 】🌟 ✨ ⭐"

# 【📊 核心亮點：4 組文字與 4 張 GIF 一對一完美配對】
# 您可以自由更換這 4 個 GIF_URL 裡面的網址！
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
        "top": " ✨ 🪐 點擊下方動圖有驚喜 🪐 ✨ ",  # 👈 第 4 句新增主公告
        "bottom": " 🎉 🪐 天天都要玩得開心 🪐 🎉 ", # 👈 第 4 句新增副公告
        "gif": "https://cdn.discordapp.com/attachments/1191437102353744096/1517843597746245712/e4c10bc2bf59f55a17dfb839c36c39a276b1ed8cbe6a00e78c7dc219ea5bb7aa.gif?ex=6a37c181&is=6a367001&hm=5d5c317da00fa8dddc2f21ebb3969b4e48f12819a2c6c2a5e362cc9332ded7f2&"
    }
]

STEP_SIZE = 3  
SPEED = 2.0  
# ==============================================================

EMBED_NEON_COLORS = [
    16753920, 5763719, 15418782, 3447003, 10181046, 15548997, 16776960
]
ANSI_COLORS = ["[1;31m", "[1;32m", "[1;33m", "[1;34m", "[1;35m", "[1;36m", "[1;37m"]
color_end = "[0m"
display_width = 18  

def run_four_gif_marquee():
    print("💎 正在發送【四圖四軌霓虹輪播版】公告...")
    
    # 建立最初始訊息
    marquee_payload = {
        "embeds": [{
            "title": luxury_title, 
            "description": "```ansi\n ⚡ 皇家系統正在載入四圖四軌全自動化特效...\n```", 
            "color": 16777215,
            "image": {"url": CAMPAIGNS[0]["gif"]}
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
    
    # 重新配置顏色 config（保持與上一版相同的高穩定度邊框）
    COLOR_CONFIGS = [
        {"text": "[1;33m", "embed": 16776960}, # 第一句：黃色
        {"text": "[1;32m", "embed": 5763719},  # 第二句：綠色
        {"text": "[1;35m", "embed": 15418782}, # 第三句：粉紅
        {"text": "[1;36m", "embed": 3447003}   # 第四句：青藍色
    ]
    
    while time.time() - start_time < max_duration:
        # 輪流執行 4 個 Campaign
        for idx, camp in enumerate(CAMPAIGNS):
            top_raw = camp["top"]
            bot_raw = camp["bottom"]
            current_gif = camp["gif"]
            
            # 對應當前輪次的顏色
            color_idx = idx % len(COLOR_CONFIGS)
            color_start = COLOR_CONFIGS[color_idx]["text"]
            current_embed_color = COLOR_CONFIGS[color_idx]["embed"]
            
            top_extended = top_raw + " " * display_width + top_raw
            bot_extended = bot_raw + " " * display_width + bot_raw
            
            max_len = max(len(top_raw), len(bot_raw)) + display_width
            i = 0
            
            while i < max_len:
                if time.time() - start_time >= max_duration:
                    break
                
                # 邊框隨機閃爍增加豪華感
                c_border1 = random.choice(ANSI_COLORS)
                c_border2 = random.choice(ANSI_COLORS)
                
                top_frame = top_extended[i : i + display_width]
                bot_pos = (max_len - i) % len(bot_extended)
                bot_frame = bot_extended[bot_pos : bot_pos + display_width]
                if len(bot_frame) < display_width:
                    bot_frame = (bot_frame + " " * display_width)[:display_width]
                
                # 📐 採用上一版完美的古典對稱邊框
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
                
                # 🚀 連同最新的 GIF 圖片一起更新發送
                payload = {
                    "embeds": [{
                        "title": luxury_title,
                        "description": description_content,
                        "color": current_embed_color,
                        "image": {"url": current_gif} # 👈 自動換成目前句子對應的 GIF！
                    }]
                }

                try:
                    res = requests.patch(marquee_message_url, json=payload)
                    if res.status_code == 429:
                        retry_after = res.json().get("retry_after", 5)
                        time.sleep(retry_after)
                        continue
                except:
                    return

                time.sleep(SPEED)
                i += STEP_SIZE
                
                if i >= max_len and (i - STEP_SIZE) < (max_len - 1):
                    i = max_len - 1
                
    print("⏰ 5小時豪華交棒！")

if __name__ == "__main__":
    run_four_gif_marquee()
