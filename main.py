import time
import requests
import random

# ==================== 💎 豪華超跑自訂控制面板 ====================
WEBHOOK_URL = "https://discord.com/api/webhooks/1517792246374731857/mcJ-748jA7WdM4DD0KsKQg9URpD-BUOCw91-8ksZjOuz4b8-P0FCr7lJYK3cWMkCOKMq"

# 【豪華配備 1：最正宗的超炫動態 GIF】
GIF_URL = "https://cdn.discordapp.com/attachments/1191437102353744096/1517791192971214858/9154af24aeb650943a3c7e2ee38504b45ca51740d251f95bba16d093acebe5d7.gif?ex=6a3790b3&is=6a363f33&hm=5c294844fd02dcb5650436b5ed323e07ee1c690301c84246cb2a65109742d80c&"

# 【豪華配備 2：客製化雙軌道台詞】
# 🚀 上軌道：從右往左狂飆（主標題公告）
TOP_TEXTS = [
    " 🔥 VIP 豪華盛宴：全服限時狂歡活動正式引爆！ ",
    " 👑 榮耀降臨：全新傳奇稱號、專屬頭銜開放送出！ ",
    " ⚡ 系統特報：請全體成員立即前往官方網站簽到！ "
]

# 📡 下軌道：從左往右倒退滾動（副標題細節，與上軌道形成震撼的對撞感！）
BOTTOM_TEXTS = [
    " ✨ ➔ 贊助通道已全面升級，感謝有您的鼎力支持！ ",
    " ✨ ➔ 點選下方動圖即可參與抽獎，千元豪禮等你拿！ ",
    " ✨ ➔ 管理員 24 小時在線，遇到問題請隨時回報！ "
]

STEP_SIZE = 3  # 每次前進字數
SPEED = 2.0  # 強烈建議維持 2.0 秒極速極限，避免被 Discord 限速
# ==============================================================

# 霓虹跑馬燈全彩池 (用於邊框與文字的隨機色階)
EMBED_NEON_COLORS = [
    16711680, 65280, 255, 16776960, 16711935, 65535, 16753920, 10181046, 15418782
]
ANSI_COLORS = [
    "[1;31m", "[1;32m", "[1;33m", "[1;34m", "[1;35m", "[1;36m", "[1;37m"
]
color_end = "[0m"
display_width = 18  # 稍微加寬顯示畫布

def run_luxury_marquee():
    print("💎 正在發送【雙軌對撞流星霓虹豪華版】公告...")
    
    # 豪華裝飾星光標題
    luxury_title = "⭐ ✨ 🌟【 皇家頂級極速公告系統 】🌟 ✨ ⭐"
    
    # 1. 創立上層雙軌跑馬燈框
    marquee_payload = {
        "embeds": [{
            "title": luxury_title, 
            "description": "```ansi\n 🌟 皇家豪華系統正在全速初始化...\n```", 
            "color": 16777215
        }]
    }
    res_marquee = requests.post(f"{WEBHOOK_URL}?wait=true", json=marquee_payload)
    if res_marquee.status_code != 200:
        print("❌ 豪華跑馬燈建立失敗")
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
    
    # 確保兩軌道台詞數量一致
    loop_count = min(len(TOP_TEXTS), len(BOTTOM_TEXTS))
    
    while time.time() - start_time < max_duration:
        for idx in range(loop_count):
            top_raw = TOP_TEXTS[idx]
            bot_raw = BOTTOM_TEXTS[idx]
            
            # 上軌道正常拼接
            top_extended = top_raw + " " * display_width + top_raw
            # 下軌道反向滾動處理
            bot_extended = bot_raw + " " * display_width + bot_raw
            
            max_len = max(len(top_raw), len(bot_raw)) + display_width
            i = 0
            
            while i < max_len:
                if time.time() - start_time >= max_duration:
                    break
                
                # 豪華配備 3：動態隨機霓虹變色
                # 每次更新，外框跟文字的色彩代碼都會像夜店霓虹燈一樣隨機瘋狂閃耀
                color_top = random.choice(ANSI_COLORS)
                color_bot = random.choice(ANSI_COLORS)
                current_embed_color = random.choice(EMBED_NEON_COLORS)
                
                # 擷取雙軌畫面
                top_frame = top_extended[i : i + display_width]
                
                # 計算倒退效果（利用負向索引製造往右移動的錯覺）
                bot_pos = (max_len - i) % len(bot_extended)
                bot_frame = bot_extended[bot_pos : bot_pos + display_width]
                if len(bot_frame) < display_width:
                    bot_frame = (bot_frame + " " * display_width)[:display_width]
                
                # 豪華配備 4：高科技雙軌排版
                description_content = (
                    f"```ansi\n"
                    f"┏━━━━ 🛰️ UPPER RAIL ━━━━━━━━━━━━━━━━┓\n"
                    f"  {color_top}{top_frame}{color_end}\n"
                    f"┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
                    f"┏━━━━ 📡 LOWER RAIL ━━━━━━━━━━━━━━━━┓\n"
                    f"  {color_bot}{bot_frame}{color_end}\n"
                    f"┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
                    f"```"
                )
                
                payload = {
                    "embeds": [{
                        "title": luxury_title,
                        "description": description_content,
                        "color": current_embed_color  # 左側條同步霓虹閃爍
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
    run_luxury_marquee()
