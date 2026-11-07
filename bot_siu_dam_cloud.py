import os
import random
import sys
from datetime import date, datetime
from zoneinfo import ZoneInfo

import requests

print("Đang tổng hợp dữ liệu buổi sáng...")

# Giờ Việt Nam (GitHub Actions chạy theo giờ UTC nên phải ép múi giờ)
VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")

# ---------------------------------------------------------------
# 1. Thời tiết Thái Bình
# ---------------------------------------------------------------
try:
    thoi_tiet = requests.get(
        "https://wttr.in/Thai_Binh?format=%c+%t&m", timeout=10
    ).text.strip()
except Exception:
    thoi_tiet = "(không lấy được thời tiết)"

# ---------------------------------------------------------------
# 2. Đếm ngược tới Tết
#    Tự chọn cái Tết sắp tới gần nhất trong danh sách, hết Tết này
#    thì tự nhảy sang Tết sau, không cần sửa code mỗi năm.
#    (Hết danh sách thì nhớ thêm năm mới vào.)
# ---------------------------------------------------------------
NGAY_TET = [
    date(2027, 2, 6),
    date(2028, 1, 26),
    date(2029, 2, 13),
]

ngay_hom_nay = datetime.now(VN_TZ).date()
tet_sap_toi = next((d for d in NGAY_TET if d >= ngay_hom_nay), None)

if tet_sap_toi is None:
    dem_nguoc = "chưa có ngày Tết mới trong danh sách, nhớ thêm vào code nhé!"
else:
    so_ngay_con_lai = (tet_sap_toi - ngay_hom_nay).days
    if so_ngay_con_lai == 0:
        dem_nguoc = "**Hôm nay là Tết rồi!** 🎊"
    else:
        dem_nguoc = f"Còn đúng **{so_ngay_con_lai}** ngày nữa!"

# ---------------------------------------------------------------
# 3. Lấy 1 câu quote
#    api.quotable.io đã chết (chứng chỉ SSL hết hạn), nên đổi sang
#    ZenQuotes, dự phòng DummyJSON, cuối cùng mới tới danh sách có sẵn.
# ---------------------------------------------------------------
# Danh sách dự phòng: API nào cũng sập thì vẫn random ra câu khác nhau
QUOTE_DU_PHONG = [
    "Đi chậm còn hơn đứng yên.",
    "Làm một việc nhỏ mỗi ngày, một năm sau sẽ khác.",
    "Muốn nhanh thì phải làm cho đúng trước.",
    "Hôm nay làm được một chút còn hơn chờ đủ hứng.",
    "Sai thì sửa, đừng bỏ.",
    "Kỷ luật quan trọng hơn cảm hứng.",
    "Tốc độ thành công phải nhanh hơn tốc độ già đi của ba mẹ",
    "Hoa hồng là hoa hồng, hoa sen là hoa sen. Chỉ nên xem đừng nên so sánh. Chúng ta có thể lấy những mặt xuất sắc và ưu tú của người khác để làm gương, nhưng vẫn phải giữ lấy bản sắc của riêng mình",
    "Khi bạn muốn thực hiện 1 điều gì, cả vũ trụ dường như hợp sức giúp bạn",
    "Kiếm tiền có thể khổ nhưng xin tiền còn khổ hơn",
    "Danh dự mới là điều thiêng liêng cao quý nhất",
    """Trời có 4 mùa: Xuân Hạ Thu Đông
    Đất có 4 phương: Đông Tây Nam Bắc
    Người có 4 đức: Cần Kiệm Liêm Chính
    Thiếu 1 mùa thì không thành Trời
    Thiếu 1 phương thì không thành Đất
    Thiếu 1 đức thì không thành Người""",
    "Ta hiếm khi nghĩ về những gì mình có, nhưng lại luôn trăn trở về những gì mình thiếu",
    """Suy nghĩ phải chín
    Tư tưởng phải thông
    Quyết tâm phải cao
    Nỗ lực phải lớn
    Hành động phải quyết liệt""",
    "Làm ngày không đủ, Tranh thủ làm đêm",
    """Biến không thành có 
    Biến khó thành dễ
    Biến cái không thể thành có thể""",
    "Lửa thử vàng, gian nan thử sức",
]

# Dòng ghi nguồn, chỉ hiện khi quote lấy từ ZenQuotes (họ yêu cầu ghi nguồn)
GHI_NGUON_ZEN = ""


def lay_quote():
    """Trả về (nội dung quote, dòng ghi nguồn nếu có)."""
    if random.random() < 0.7:
        return random.choice(QUOTE_DU_PHONG), ""
    # Nguồn 1: ZenQuotes
    try:
        r = requests.get("https://zenquotes.io/api/random", timeout=5)
        r.raise_for_status()
        q = r.json()[0]
        return f'"{q["q"]}" — *{q["a"]}*', GHI_NGUON_ZEN
    except Exception as e:
        print(f"ZenQuotes lỗi: {e}")

    # Nguồn 2: DummyJSON
    try:
        r = requests.get("https://dummyjson.com/quotes/random", timeout=5)
        r.raise_for_status()
        q = r.json()
        return f'"{q["quote"]}" — *{q["author"]}*', ""
    except Exception as e:
        print(f"DummyJSON lỗi: {e}")

    # Nguồn 3: danh sách có sẵn
    return random.choice(QUOTE_DU_PHONG), ""


quote_text, ghi_nguon = lay_quote()

# Bỏ khoảng trắng thừa đầu/cuối mỗi dòng, rồi thêm "> " vào TỪNG dòng
# để nhiều dòng (thơ) đều nằm gọn trong khung trích dẫn của Discord.
quote_text = "\n".join("> " + dong.strip() for dong in quote_text.split("\n"))

# ---------------------------------------------------------------
# 4. Đóng gói tin nhắn
# ---------------------------------------------------------------
tin_nhan = f"""🌅 **BÁO CÁO BUỔI SÁNG (08:00 AM)** 🌅

☁️ **Thời tiết Thái Bình:** {thoi_tiet}
⏳ **Đếm ngược Tết:** {dem_nguoc}
💡 **Trích dẫn hôm nay:**
{quote_text}{ghi_nguon}

---
*Chúc dimai một ngày mới tràn đầy năng lượng!*"""

# ---------------------------------------------------------------
# 5. Bắn lên Discord
#    URL webhook KHÔNG để trong code. Lấy từ biến môi trường
#    DISCORD_WEBHOOK (trên GitHub: Settings > Secrets and variables > Actions).
# ---------------------------------------------------------------
webhook_url = os.environ.get("DISCORD_WEBHOOK")

if not webhook_url:
    print("Chưa đặt biến DISCORD_WEBHOOK nên chỉ in thử, không gửi:\n")
    print(tin_nhan)
    sys.exit(0)

res = requests.post(webhook_url, json={"content": tin_nhan}, timeout=10)
res.raise_for_status()
print("Đã bắn báo cáo thành công!")
