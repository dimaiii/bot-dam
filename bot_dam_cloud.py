import requests
from datetime import date

print("Đang tổng hợp dữ liệu buổi sáng...")

# 1. Thời tiết Thái Bình
thoi_tiet = requests.get("https://wttr.in/Thai_Binh?format=3&M").text.strip()

# 2. Đếm ngược tới Tết
ngay_hom_nay = date.today()
ngay_tet = date(2027, 2, 6)
so_ngay_con_lai = (ngay_tet - ngay_hom_nay).days

# 3. Lấy 1 câu quote 
try:
    quote_res = requests.get("https://api.quotable.io/random", timeout=5).json()
    quote_text = f'"{quote_res["content"]}" — *{quote_res["author"]}*'
except:
    quote_text = "Chúc dimai một ngày mới tốt lành và làm việc hiệu quả!"

# 4. Đóng gói tin nhắn
tin_nhan = f"""🌅 **BÁO CÁO BUỔI SÁNG (08:00 AM)** 🌅

☁️ **Thời tiết Thái Bình:** {thoi_tiet}
⏳ **Đếm ngược Tết:** Còn đúng **{so_ngay_con_lai}** ngày nữa!
💡 **Trích dẫn hôm nay:** 
> {quote_text}

---
*Chúc dimai một ngày mới tràn đầy năng lượng!*"""

# 5. Bắn lên Discord
webhook_url = "https://discord.com/api/webhooks/1564287862290255957/gl6LrI_5SU3Obvs4qkKv8kbchzgUqdrmCidDytxT3gTJ3cHn1y8z_lLz8-dks7G60Yw8"
requests.post(webhook_url, json={"content": tin_nhan})
print("Đã bắn báo cáo thành công!")
