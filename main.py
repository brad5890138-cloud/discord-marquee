import time
import requests
import random

# ==================== 👑 至尊皇家自訂控制面板 ====================
WEBHOOK_URL = "https://discord.com/api/webhooks/1517854084257026238/f1wxy5XswdIxpwyZM1nZSfTThS3PAbGVaqNv5RZRo8rPrkcnc-M-rqAgX5hP5UEeXTAn"

# 【配備 1：更具動感的背景 GIF 網址】
GIF_URL = "https://cdn.discordapp.com/attachments/1191437102353744096/1518964924062109696/49780eceb55add4efc653ee4f86340fb938636700559fe7e2345026692c51369.gif?ex=6a3bd5d2&is=6a3a8452&hm=482b2f605fdeb7d96f7fabf50a5de6af336cb0e578a3c6e0164cf7ec5ac45cd5&"

# 【配備 2：客製化雙軌道台詞（前後加入閃爍星光粒子）】
TOP_TEXTS = [
    "  🍀 歡迎來到~~噬月陌姎 🪐  ",
    "  💬 文字聊天請至 ➔ 🔐幹話一堆《2026》  ",
    "  🔊 語音聊天請至下方房間  "
]

BOTTOM_TEXTS = [
    " ✨  一起交友聊天玩遊戲  ✨ ",
    " 🤪  這裡人超憨超胖 🤪  ",
    " 👋  歡迎加入!!!!   👋 "
]

STEP_SIZE = 3  # 每次前進字數
SPEED = 2.0  # 維持 2.0 秒極速極限，流暢且安全
# ==============================================================

# 至尊霓虹 RGB 顏色池
EMBED_NEON_COLORS = [16711680, 65280, 255, 16776960, 16711935, 65535, 16777215]
ANSI_COLORS = [
    "[1;31m", "[1;32m", "[1;33m", "[1;34m", "[1;35m", "[1;36m", "[1;37m"
]
color_end = "[0m"
display_width = 18  

def run_supreme_marquee():
    print("💎 正在發送【噬月陌姎】公告...")
    
    # 頂級奢華裝飾標題
    luxury_title = "🔱 ✨ 🌟【 歡迎加入噬月陌姎  】🌟 ✨ 🔱"
    
    # 1. 創立上層雙軌跑馬燈框
    marquee_payload = {
        "embeds": [{
            "title": luxury_title, 
            "description": "```ansi\n ⚡ 噬月陌姎系統正在全速加載 RGB 燈效...\n```", 
            "color": 16777215
        }]
    }
    res_marquee = requests.post(f"{WEBHOOK_URL}?wait=true", json=marquee_payload)
    if res_marquee.status_code != 200:
        print("❌ 跑馬燈建立失敗")
        return
    
    marquee_message_id = res_marquee.json().get("id")
    marquee_message_url = f"{WEBHOOK_URL}/messages/{marquee_message_id}"
    
    # 2. 創立底層獨立 GIF（維持不閃爍）
    gif_payload = {
        "embeds": [{
            "color": 16777215,
            "image": {"url": GIF_URL}
        }]
    }
    requests.post(WEBHOOK_URL, json=gif_payload)
    
    start_time = time.time()
    max_duration = 18000  # 5小時微軟接力限制
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
                
                # 隨時為每一條框線、每一行文字隨機抽籤色彩，達到斑斕霓虹效果
                c_border1 = random.choice(ANSI_COLORS)
                c_border2 = random.choice(ANSI_COLORS)
                c_text1 = random.choice(ANSI_COLORS)
                c_text2 = random.choice(ANSI_COLORS)
                current_embed_color = random.choice(EMBED_NEON_COLORS)
                
                # 擷取雙軌畫面
                top_frame = top_extended[i : i + display_width]
                
                bot_pos = (max_len - i) % len(bot_extended)
                bot_frame = bot_extended[bot_pos : bot_pos + display_width]
                if len(bot_frame) < display_width:
                    bot_frame = (bot_frame + " " * display_width)[:display_width]
                
                # 【優化重點：外框同步加入 ANSI 炫彩顏色，框線也會跟著變色！】
                description_content = (
                    f"```ansi\n"
                    f"{c_border1}▰▰▰▰▰▰ ✨ 星星所向  🌠  ▰▰▰▰▰▰{color_end}\n"
                    f"  {c_text1}{top_frame}{color_end}\n"
                    f"{c_border1}▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰{color_end}\n"
                    f"{c_border2}▰▰▰▰▰ 💫 星河皆是你  🌙  ▰▰▰▰▰{color_end}\n"
                    f"  {c_text2}{bot_frame}{color_end}\n"
                    f"{c_border2}▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰{color_end}\n"
                    f"```"
                )
                
                payload = {
                    "embeds": [{
                        "title": luxury_title,
                        "description": description_content,
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
                
                if i >= max_len and (i - STEP_SIZE) < (max_len - 1):
                    i = max_len - 1
                
    print("⏰ 5小時豪華交棒！")

if __name__ == "__main__":
    run_supreme_marquee()
