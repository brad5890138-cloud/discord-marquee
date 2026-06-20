import time
import requests

# ==================== 🎛️ 跑馬燈自訂控制面板 ====================
WEBHOOK_URL = "https://discord.com/api/webhooks/1517792246374731857/mcJ-748jA7WdM4DD0KsKQg9URpD-BUOCw91-8ksZjOuz4b8-P0FCr7lJYK3cWMkCOKMq"

# 【功能：加入 GIF 動圖】請把你想放的 GIF 圖片網址，完整複製貼在兩個引號中間
GIF_URL = "https://cdn.discordapp.com/attachments/1191437102353744096/1517791192971214858/9154af24aeb650943a3c7e2ee38504b45ca51740d251f95bba16d093acebe5d7.gif?ex=6a3790b3&is=6a363f33&hm=5c294844fd02dcb5650436b5ed323e07ee1c690301c84246cb2a65109742d80c&"

TEXT_LIST = [
    " 🚨 這是第一句：伺服器重要公告測試中！ ",
    " 💎 這是第二句：歡迎大家加入，贊助永久開放！ ",
    " ➔ 這是第三句：請大家務必詳閱管理守則！ "
]

TEXT_COLOR = "黃色" 
SPEED = 2.3  
EMBED_COLOR = 16753920  # 橘色卡片外框
# ==============================================================

COLOR_CODES = {
    "紅色": "[1;31m", "綠色": "[1;32m", "黃色": "[1;33m",
    "藍色": "[1;34m", "粉色": "[1;35m", "青色": "[1;36m", "白色": "[1;37m"
}
color_start = COLOR_CODES.get(TEXT_COLOR, "[1;37m")
color_end = "[0m"
display_width = 15  

def run_gif_marquee():
    print("🚀 正在發送帶有 GIF 的升級版跑馬燈卡片...")
    initial_payload = {
        "embeds": [{
            "title": "📢 系統進階跑馬燈", 
            "description": "```ansi\n[ 正在換班初始化... ]\n```", 
            "color": EMBED_COLOR,
            "image": {"url": GIF_URL}  # 初始化加入 GIF
        }]
    }
    post_res = requests.post(f"{WEBHOOK_URL}?wait=true", json=initial_payload)
    if post_res.status_code != 200:
        print("❌ 發送失敗")
        return
        
    new_message_id = post_res.json().get("id")
    message_url = f"{WEBHOOK_URL}/messages/{new_message_id}"
    
    start_time = time.time()
    max_duration = 18000  # 5 小時換班限制
    
    while time.time() - start_time < max_duration:
        for current_text in TEXT_LIST:
            extended_text = current_text + " " * display_width + current_text
            
            for i in range(len(current_text) + display_width):
                if time.time() - start_time >= max_duration:
                    break
                    
                marquee_frame = extended_text[i : i + display_width]
                
                # ── 核心：每次 patch 都帶著 image 欄位，確保 GIF 持續顯示 ──
                payload = {
                    "embeds": [{
                        "title": "📢 系統進階跑馬燈",
                        "description": f"```ansi\n[ {color_start}{marquee_frame}{color_end} ]\n```",
                        "color": EMBED_COLOR,
                        "image": {"url": GIF_URL}  # 這裡維持 GIF 顯示
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

                time.sleep(SPEED) 
                
    print("⏰ 5小時安全交棒！")

if __name__ == "__main__":
    run_gif_marquee()
