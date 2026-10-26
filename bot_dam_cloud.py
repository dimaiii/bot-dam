import requests
from datetime import date
import xml.etree.ElementTree as ET

print("Đang tổng hợp dữ liệu buổi sáng...")

# 1. Thời tiết Thái Bình (chuẩn độ C)
thoi_tiet = requests.get("https://wttr.in/Thai_Binh?format=3&M").text.strip()

# 2. Đếm ngược tới Tết Nguyên Đán 2027
ngay_hom_nay = date.today()
ngay_tet = date(2027, 2, 6)
so_ngay_con_lai = (ngay_tet - ngay_hom_nay).days

# 3. Lấy 1 câu quote hay ngẫu nhiên
try:
    quote_res = requests.get("https://api.quotable.io/random", timeout=5).json()
    quote_text = f'"{quote_res["content"]}" — *{quote_res["author"]}*'
except:
    quote_text = "Chúc dimai một ngày mới tốt lành và làm việc hiệu quả!"

# 4. Cào 3 tin tức nóng nhất từ RSS VnExpress
tin_tuc_str = ""
try:
    rss_res = requests.get("https://tuoitre.vn/rss/tin-moi-nhat.rss", timeout=5)
    root = ET.fromstring(rss_res.content)
    items = root.findall('.//item')[:3]
    
    danh_sach_tin = []
    for item in items:
        title = item.find('title').text
        danh_sach_tin.append(f"• {title}")
    tin_tuc_str = "\n".join(danh_sach_tin)
except:
    tin_tuc_str = "• Tạm thời không lấy được tin tức."

# 5. Đóng gói thành bản tin siêu cấp VIP
tin_nhan = f"""🌅 **BÁO CÁO BUỔI SÁNG (08:00 AM)** 🌅

☁️ **Thời tiết Thái Bình:** {thoi_tiet}
⏳ **Đếm ngược Tết:** Còn đúng **{so_ngay_con_lai}** ngày nữa!

💡 **Trích dẫn hôm nay:** 
> {quote_text}

📰 **Điểm tin nhanh sáng nay:**
{tin_tuc_str}

---
*Chúc dimai một ngày mới tràn đầy năng lượng!*"""

# 6. Bắn lên Discord qua Webhook
webhook_url = "https://discord.com/api/webhooks/1564287862290255957/gl6LrI_5SU3Obvs4qkKv8kbchzgUqdrmCidDytxT3gTJ3cHn1y8z_lLz8-dks7G60Yw8"
response = requests.post(webhook_url, json={"content": tin_nhan})

if response.status_code == 204:
    print("-> Đã bắn báo cáo full option thành công!")
else:
    print("-> Lỗi gửi tin nhắn!")
