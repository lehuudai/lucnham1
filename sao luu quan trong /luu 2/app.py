from flask import Flask, render_template, request
from datetime import datetime, timedelta
from lunarcalendar import Converter, Solar, Lunar
import math     
import ephem    

# ===== GỌI THƯ VIỆN 100 CÂU TẤT PHÁP PHÚ =====
from tat_phap_phu import quet_100_tat_phap_phu
# =============================================

app = Flask(__name__)

# ==========================================
# 1. HỆ THỐNG DỮ LIỆU CƠ BẢN LỤC NHÂM
# ==========================================
THIEN_CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
DIA_CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

KY_CUNG = {"Giáp": "Dần", "Ất": "Thìn", "Bính": "Tỵ", "Mậu": "Tỵ", "Đinh": "Mùi", "Kỷ": "Mùi", "Canh": "Thân", "Tân": "Tuất", "Nhâm": "Hợi", "Quý": "Sửu"}
THIEN_TUONG_LIST = ["Quý Nhân", "Đằng Xà", "Chu Tước", "Lục Hợp", "Câu Trần", "Thanh Long", "Thiên Không", "Bạch Hổ", "Thái Thường", "Huyền Vũ", "Thái Âm", "Thiên Hậu"]
LOAI_THAN_NAMES = ['Kiến', 'Lợi', 'Phúc', 'Hung', 'Cô', 'Phế', 'Hưu', 'Tử', 'Tù', 'Một', 'Thai', 'Vượng']

NGU_HANH = {
    "Giáp": "Mộc", "Ất": "Mộc", "Bính": "Hỏa", "Đinh": "Hỏa", "Mậu": "Thổ", "Kỷ": "Thổ", "Canh": "Kim", "Tân": "Kim", "Nhâm": "Thủy", "Quý": "Thủy",
    "Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc", "Thìn": "Thổ", "Tỵ": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ", "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy",
    "Quý Nhân": "Thổ", "Đằng Xà": "Hỏa", "Chu Tước": "Hỏa", "Lục Hợp": "Mộc", "Câu Trần": "Thổ", "Thanh Long": "Mộc", 
    "Thiên Không": "Thổ", "Bạch Hổ": "Kim", "Thái Thường": "Thổ", "Huyền Vũ": "Thủy", "Thái Âm": "Kim", "Thiên Hậu": "Thủy"
}

AM_DUONG = {
    "Giáp": "Dương", "Ất": "Âm", "Bính": "Dương", "Đinh": "Âm", "Mậu": "Dương", "Kỷ": "Âm", "Canh": "Dương", "Tân": "Âm", "Nhâm": "Dương", "Quý": "Âm",
    "Tý": "Dương", "Sửu": "Âm", "Dần": "Dương", "Mão": "Âm", "Thìn": "Dương", "Tỵ": "Âm", "Ngọ": "Dương", "Mùi": "Âm", "Thân": "Dương", "Dậu": "Âm", "Tuất": "Dương", "Hợi": "Âm"
}

XUNG_MAP = {"Tý":"Ngọ", "Sửu":"Mùi", "Dần":"Thân", "Mão":"Dậu", "Thìn":"Tuất", "Tỵ":"Hợi", "Ngọ":"Tý", "Mùi":"Sửu", "Thân":"Dần", "Dậu":"Mão", "Tuất":"Thìn", "Hợi":"Tỵ"}
HOP_MAP = {"Tý":"Sửu", "Sửu":"Tý", "Dần":"Hợi", "Hợi":"Dần", "Mão":"Tuất", "Tuất":"Mão", "Thìn":"Dậu", "Dậu":"Thìn", "Tỵ":"Thân", "Thân":"Tỵ", "Ngọ":"Mùi", "Mùi":"Ngọ"}

# ==========================================
# 2. CÁC HÀM TÍNH TOÁN LOGIC LỤC NHÂM
# ==========================================
def tinh_khong_vong(can, chi):
    idx_khong_1 = (DIA_CHI.index(chi) - THIEN_CAN.index(can) - 2) % 12
    return [DIA_CHI[idx_khong_1], DIA_CHI[(idx_khong_1 + 1) % 12]]

def get_don_can(can_ngay, chi_ngay, chi_dia_ban):
    idx_can = THIEN_CAN.index(can_ngay)
    idx_chi = DIA_CHI.index(chi_ngay)
    idx_tuan_thu = (idx_chi - idx_can + 12) % 12
    idx_target = DIA_CHI.index(chi_dia_ban)
    delta = (idx_target - idx_tuan_thu + 12) % 12
    if delta < 10: return THIEN_CAN[delta]
    else: return "Không"

def get_nguyen(can_ngay, chi_ngay):
    offset = THIEN_CAN.index(can_ngay) % 5
    phu_dau_chi = (DIA_CHI.index(chi_ngay) - offset + 12) % 12
    return 'Thượng Nguyên' if phu_dau_chi % 3 == 0 else ('Hạ Nguyên' if phu_dau_chi % 3 == 1 else 'Trung Nguyên')

def get_luc_than(can_ngay, chi_khach):
    ht, hk = NGU_HANH[can_ngay], NGU_HANH[chi_khach]
    sinh_out, sinh_in = {"Mộc":"Hỏa", "Hỏa":"Thổ", "Thổ":"Kim", "Kim":"Thủy", "Thủy":"Mộc"}, {"Mộc":"Thủy", "Hỏa":"Mộc", "Thổ":"Hỏa", "Kim":"Thổ", "Thủy":"Kim"}
    khac_out, khac_in = {"Mộc":"Thổ", "Hỏa":"Kim", "Thổ":"Thủy", "Kim":"Mộc", "Thủy":"Hỏa"}, {"Mộc":"Kim", "Hỏa":"Thủy", "Thổ":"Mộc", "Kim":"Hỏa", "Thủy":"Thổ"}
    if ht == hk: return "Huynh Đệ"
    if sinh_out[ht] == hk: return "Tử Tôn"
    if sinh_in[ht] == hk: return "Phụ Mẫu"
    if khac_out[ht] == hk: return "Thê Tài"
    if khac_in[ht] == hk: return "Quan Quỷ"
    return ""

def _nh(val): return NGU_HANH.get(val, val)

def nh_icon(element):
    icons = {"Mộc": "🌳 Mộc", "Hỏa": "🔥 Hỏa", "Thổ": "⛰️ Thổ", "Kim": "⚔️ Kim", "Thủy": "💧 Thủy"}
    return icons.get(element, element)

def la_khac(A, B): return {"Mộc":"Thổ", "Thổ":"Thủy", "Thủy":"Hỏa", "Hỏa":"Kim", "Kim":"Mộc"}.get(_nh(A)) == _nh(B)
def la_sinh(A, B): return {"Mộc":"Hỏa", "Hỏa":"Thổ", "Thổ":"Kim", "Kim":"Thủy", "Thủy":"Mộc"}.get(_nh(A)) == _nh(B)

def get_quan_he_sinh_khac(tren, duoi):
    if la_khac(duoi, tren): return "↑ Khắc (Tặc)"
    if la_khac(tren, duoi): return "↓ Khắc"
    if la_sinh(duoi, tren): return "↑ Sinh"
    if la_sinh(tren, duoi): return "↓ Sinh"
    return "= Tỷ Hòa"

def xet_lat_keo_ban_menh(mat_truyen_chi, ban_menh_chi):
    if not ban_menh_chi: return ""
    ngu_hanh_mat = NGU_HANH[mat_truyen_chi]
    ngu_hanh_menh = NGU_HANH[ban_menh_chi]
    if la_sinh(ngu_hanh_mat, ngu_hanh_menh): return f"Mạt sinh Mệnh ({ngu_hanh_mat} sinh {ngu_hanh_menh}) - CẢI TỬ HOÀN SINH: Trong họa có Phúc, được cứu vớt phút chót."
    elif la_khac(ngu_hanh_mat, ngu_hanh_menh): return f"Mạt khắc Mệnh ({ngu_hanh_mat} khắc {ngu_hanh_menh}) - BÁNH VẼ/ĐỘC DƯỢC: Có tiền/Cơ hội cũng không đến phần mình, ăn vào dễ mang họa."
    elif la_sinh(ngu_hanh_menh, ngu_hanh_mat): return f"Mệnh sinh Mạt ({ngu_hanh_menh} sinh {ngu_hanh_mat}) - SINH XUẤT: Bản thân phải lao tâm khổ tứ, hao sức tốn tài vì sự việc."
    elif la_khac(ngu_hanh_menh, ngu_hanh_mat): return f"Mệnh khắc Mạt ({ngu_hanh_menh} khắc {ngu_hanh_mat}) - KHẮC XUẤT: Bản thân chủ động kiểm soát được kết quả, tuy hơi vất vả."
    else: return f"Tỷ Hòa ({ngu_hanh_mat} - {ngu_hanh_menh}) - ĐỒNG HÀNH: Sự việc kết thúc bình ổn, kết quả tương xứng với năng lực."

# BỔ SUNG: HÀM SO GĂNG MẠT TRUYỀN VỚI CAN NGÀY (TA)
def xet_lat_keo_mat_vs_can_ngay(mat_truyen_chi, can_ngay):
    ngu_hanh_mat = NGU_HANH[mat_truyen_chi]
    ngu_hanh_can = NGU_HANH[can_ngay]
    
    if la_sinh(ngu_hanh_mat, ngu_hanh_can): return f"🟢 Mạt sinh Can ({ngu_hanh_mat} sinh {ngu_hanh_can}): ĐẠI CÁT - Kết quả mỹ mãn. Lợi ích, tiền tài, thành công được dâng đến tận tay."
    elif la_khac(ngu_hanh_can, ngu_hanh_mat): return f"🟢 Can khắc Mạt ({ngu_hanh_can} khắc {ngu_hanh_mat}): TIỂU CÁT - Chiến thắng, đoạt được mục tiêu, nhưng phải nỗ lực kiểm soát tình hình."
    elif la_khac(ngu_hanh_mat, ngu_hanh_can): return f"🔴 Mạt khắc Can ({ngu_hanh_mat} khắc {ngu_hanh_can}): ĐẠI HUNG - Thất bại ê chề. Phút chót bị lật kèo, chèn ép, tổn thương. Nên từ bỏ."
    elif la_sinh(ngu_hanh_can, ngu_hanh_mat): return f"🔴 Can sinh Mạt ({ngu_hanh_can} sinh {ngu_hanh_mat}): HAO TỔN - Bị vắt kiệt. Dù việc thành thì cũng mất nhiều hơn được, làm lợi cho người khác."
    else: return f"⚪ Tỷ Hòa ({ngu_hanh_can} - {ngu_hanh_mat}): BÌNH ỔN - Kết quả xứng đáng với công sức bỏ ra, không biến động lớn."

def tinh_hanh_nien(nam_sinh_chi, nam_que_chi, gioi_tinh):
    idx_menh = DIA_CHI.index(nam_sinh_chi)
    idx_tuoihientai = DIA_CHI.index(nam_que_chi)
    delta = (idx_tuoihientai - idx_menh) % 12
    if gioi_tinh == "Nam": idx_hanh_nien = (DIA_CHI.index("Dần") + delta) % 12
    else: idx_hanh_nien = (DIA_CHI.index("Thân") - delta) % 12
    return DIA_CHI[idx_hanh_nien]

def get_quan_he_chi(chi1, chi2):
    if not chi1 or not chi2: return ""
    if chi1 == chi2:
        if chi1 in ["Thìn", "Ngọ", "Dậu", "Hợi"]: return "Tự Hình"
        return "Bình Hòa"
    luc_hop = [{"Tý", "Sửu"}, {"Dần", "Hợi"}, {"Mão", "Tuất"}, {"Thìn", "Dậu"}, {"Tỵ", "Thân"}, {"Ngọ", "Mùi"}]
    luc_xung = [{"Tý", "Ngọ"}, {"Sửu", "Mùi"}, {"Dần", "Thân"}, {"Mão", "Dậu"}, {"Thìn", "Tuất"}, {"Tỵ", "Hợi"}]
    res = []
    pair = {chi1, chi2}
    if pair in luc_hop: res.append("Lục Hợp")
    if pair in luc_xung: res.append("Lục Xung")
    if pair in [{"Dần", "Tỵ"}, {"Tỵ", "Thân"}, {"Dần", "Thân"}, {"Sửu", "Tuất"}, {"Tuất", "Mùi"}, {"Sửu", "Mùi"}, {"Tý", "Mão"}]: res.append("Hình")
    if pair in [{"Tý", "Mùi"}, {"Sửu", "Ngọ"}, {"Dần", "Tỵ"}, {"Mão", "Thìn"}, {"Thân", "Hợi"}, {"Dậu", "Tuất"}]: res.append("Hại")
    if pair in [{"Tý", "Dậu"}, {"Mão", "Ngọ"}, {"Sửu", "Thìn"}, {"Mùi", "Tuất"}, {"Dần", "Hợi"}, {"Tỵ", "Thân"}]: res.append("Phá")
    return " | ".join(res) if res else ""

def get_cuc_dien_tam_truyen(so, trung, mat):
    res = []
    chi_set = {so, trung, mat}
    tam_hop = [{"Dần", "Ngọ", "Tuất"}, {"Hợi", "Mão", "Mùi"}, {"Thân", "Tý", "Thìn"}, {"Tỵ", "Dậu", "Sửu"}]
    if chi_set in tam_hop: res.append("Tam Hợp Cục")
    tam_hinh = [{"Dần", "Tỵ", "Thân"}, {"Sửu", "Tuất", "Mùi"}]
    if chi_set in tam_hinh: res.append("Tam Hình Cục")
    if len(chi_set) == 1 and so in ["Thìn", "Ngọ", "Dậu", "Hợi"]: res.append("Toàn Cục Tự Hình")
    return res

# BỔ SUNG: XÁC ĐỊNH TRUYỀN TIẾN HAY TRUYỀN THOÁI
def get_tien_thoai_tam_truyen(so, trung, mat):
    idx_so = DIA_CHI.index(so)
    idx_trung = DIA_CHI.index(trung)
    idx_mat = DIA_CHI.index(mat)
    
    if (idx_so + 1) % 12 == idx_trung and (idx_trung + 1) % 12 == idx_mat:
        return "TRUYỀN TIẾN (Tiến tới): Sự việc phát triển thăng tiến, mở rộng, mau lẹ, không ngừng tiến về phía trước."
    elif (idx_so - 1) % 12 == idx_trung and (idx_trung - 1) % 12 == idx_mat:
        return "TRUYỀN THOÁI (Lùi lại): Sự việc tụt lùi, co cụm, chậm chạp, người cũ quay về, hoặc phải giải quyết dứt điểm chuyện quá khứ."
    elif idx_so == idx_trung and idx_trung == idx_mat:
         return "Dậm chân tại chỗ: Bế tắc, nhùng nhằng, không có diễn biến mới."
    return ""

def lap_vong_thai_tue(nam_chi):
    sao_tue = ["Thái Tuế", "Thái Dương", "Tang Môn", "Thái Âm", "Quan Phù", "Tử Phù", "Tuế Phá", "Long Đức", "Bạch Hổ", "Phúc Đức", "Điếu Khách", "Bệnh Phù"]
    start_idx = DIA_CHI.index(nam_chi)
    return {DIA_CHI[(start_idx + i) % 12]: sao_tue[i] for i in range(12)}

def get_loai_than(day_chi, di_ban_idx):
    idx = (di_ban_idx - DIA_CHI.index(day_chi) + 12) % 12
    return LOAI_THAN_NAMES[idx]

def tinh_than_sat_thien_ban(can_ngay, chi_ngay, chi_nam, chi_thang, thien_ban_chi, kv_ngay):
    sat = []
    if thien_ban_chi == chi_nam: sat.append("Thái Tuế")
    if thien_ban_chi == chi_thang: sat.append("Nguyệt Kiến")
    if thien_ban_chi == {"Giáp":"Dần", "Ất":"Mão", "Bính":"Tỵ", "Đinh":"Ngọ", "Mậu":"Tỵ", "Kỷ":"Ngọ", "Canh":"Thân", "Tân":"Dậu", "Nhâm":"Hợi", "Quý":"Tý"}.get(can_ngay): sat.append("Thiên Lộc")
    if thien_ban_chi == {"Thân":"Dần", "Tý":"Dần", "Thìn":"Dần", "Dần":"Thân", "Ngọ":"Thân", "Tuất":"Thân", "Tỵ":"Hợi", "Dậu":"Hợi", "Sửu":"Hợi", "Hợi":"Tỵ", "Mão":"Tỵ", "Mùi":"Tỵ"}.get(chi_ngay): sat.append("Thiên Mã")
    if thien_ban_chi == {"Thân":"Dậu", "Tý":"Dậu", "Thìn":"Dậu", "Dần":"Mão", "Ngọ":"Mão", "Tuất":"Mão", "Tỵ":"Ngọ", "Dậu":"Ngọ", "Sửu":"Ngọ", "Hợi":"Tý", "Mão":"Tý", "Mùi":"Tý"}.get(chi_ngay): sat.append("Đào Hoa")
    hoa_cai_map = {"Thân":"Thìn", "Tý":"Thìn", "Thìn":"Thìn", "Dần":"Tuất", "Ngọ":"Tuất", "Tuất":"Tuất", "Tỵ":"Sửu", "Dậu":"Sửu", "Sửu":"Sửu", "Hợi":"Mùi", "Mão":"Mùi", "Mùi":"Mùi"}
    if thien_ban_chi == hoa_cai_map.get(chi_ngay): sat.append("Hoa Cái")
    dai_sat_map = {"Dần": "Ngọ", "Mão": "Mão", "Thìn": "Tý", "Tỵ": "Dậu", "Ngọ": "Ngọ", "Mùi": "Mão", "Thân": "Tý", "Dậu": "Dậu", "Tuất": "Ngọ", "Hợi": "Mão", "Tý": "Tý", "Sửu": "Dậu"}
    tieu_sat_map = {"Dần": "Sửu", "Mão": "Tuất", "Thìn": "Mùi", "Tỵ": "Thìn", "Ngọ": "Sửu", "Mùi": "Tuất", "Thân": "Mùi", "Dậu": "Thìn", "Tuất": "Sửu", "Hợi": "Tuất", "Tý": "Mùi", "Sửu": "Thìn"}
    if thien_ban_chi == dai_sat_map.get(chi_thang): sat.append("Đại Sát")
    if thien_ban_chi == tieu_sat_map.get(chi_thang): sat.append("Tiểu Sát")
    if thien_ban_chi == DIA_CHI[(DIA_CHI.index(chi_thang) + 6) % 12]: sat.append("Nguyệt Phá")
    if thien_ban_chi == DIA_CHI[(DIA_CHI.index(chi_nam) + 6) % 12]: sat.append("Tuế Phá") 
    hinh_map = {"Dần":"Tỵ", "Tỵ":"Thân", "Thân":"Dần", "Sửu":"Tuất", "Tuất":"Mùi", "Mùi":"Sửu", "Tý":"Mão", "Mão":"Tý", "Thìn":"Thìn", "Ngọ":"Ngọ", "Dậu":"Dậu", "Hợi":"Hợi"}
    if thien_ban_chi == hinh_map.get(chi_ngay): sat.append("Thiên Hình")
    kiep_sat_map = {"Thân":"Tỵ", "Tý":"Tỵ", "Thìn":"Tỵ", "Dần":"Hợi", "Ngọ":"Hợi", "Tuất":"Hợi", "Tỵ":"Dần", "Dậu":"Dần", "Sửu":"Dần", "Hợi":"Thân", "Mão":"Thân", "Mùi":"Thân"}
    tai_sat_map = {"Thân":"Ngọ", "Tý":"Ngọ", "Thìn":"Ngọ", "Dần":"Tý", "Ngọ":"Tý", "Tuất":"Tý", "Tỵ":"Mão", "Dậu":"Mão", "Sửu":"Mão", "Hợi":"Dậu", "Mão":"Dậu", "Mùi":"Dậu"}
    if thien_ban_chi == kiep_sat_map.get(chi_ngay): sat.append("Kiếp Sát")
    if thien_ban_chi == tai_sat_map.get(chi_ngay): sat.append("Tai Sát")
    # BỔ SUNG ĐẠI CÁT THẦN CỨU MẠNG (Thiên Đức, Nguyệt Đức, Thiên Y)
    thien_duc_map = {"Tý":"Tỵ", "Sửu":"Canh", "Dần":"Đinh", "Mão":"Thân", "Thìn":"Nhâm", "Tỵ":"Hợi", "Ngọ":"Quý", "Mùi":"Giáp", "Thân":"Dậu", "Dậu":"Dần", "Tuất":"Bính", "Hợi":"Ất"}
    nguyet_duc_map = {"Dần":"Bính", "Ngọ":"Bính", "Tuất":"Bính", "Thân":"Nhâm", "Tý":"Nhâm", "Thìn":"Nhâm", "Hợi":"Giáp", "Mão":"Giáp", "Mùi":"Giáp", "Tỵ":"Canh", "Dậu":"Canh", "Sửu":"Canh"}
    thien_y_map = {"Dần":"Sửu", "Mão":"Dần", "Thìn":"Mão", "Tỵ":"Thìn", "Ngọ":"Tỵ", "Mùi":"Ngọ", "Thân":"Mùi", "Dậu":"Thân", "Tuất":"Dậu", "Hợi":"Tuất", "Tý":"Hợi", "Sửu":"Tý"}
    
    # Vì Thiên Đức/Nguyệt Đức có thể là Can, ta quy đổi Can về Chi tương ứng để xét trên mâm quẻ
    can_to_chi = {"Giáp":"Dần", "Ất":"Mão", "Bính":"Tỵ", "Đinh":"Ngọ", "Canh":"Thân", "Tân":"Dậu", "Nhâm":"Hợi", "Quý":"Tý"}
    
    td_val = thien_duc_map.get(chi_thang)
    if td_val in can_to_chi: td_val = can_to_chi[td_val]
    nd_val = nguyet_duc_map.get(chi_thang)
    if nd_val in can_to_chi: nd_val = can_to_chi[nd_val]

    if thien_ban_chi == td_val: sat.append("Thiên Đức (Giải Cứu)")
    if thien_ban_chi == nd_val: sat.append("Nguyệt Đức (Giải Cứu)")
    if thien_ban_chi == thien_y_map.get(chi_thang): sat.append("Thiên Y (Thần Y)")
    return sat

def tinh_vuong_suy(chi_can_xet, chi_thang):
    h_xet, h_thang = NGU_HANH[chi_can_xet], NGU_HANH[chi_thang]
    if h_xet == h_thang: return "VƯỢNG (100%)"
    if la_sinh(h_thang, h_xet): return "TƯỚNG (80%)"
    if la_sinh(h_xet, h_thang): return "HƯU (40%)"
    if la_khac(h_xet, h_thang): return "TÙ (20%)"
    if la_khac(h_thang, h_xet): return "TỬ (0%)"
    return ""

def get_12_truong_sinh(can_ngay, chi_dia_ban):
    TRUONG_SINH_STATES = ["Trường Sinh", "Mộc Dục", "Quan Đới", "Lâm Quan", "Đế Vượng", "Suy", "Bệnh", "Tử", "Mộ", "Tuyệt", "Thai", "Dưỡng"]
    start_map = {"Giáp": ("Hợi", 1), "Bính": ("Dần", 1), "Mậu": ("Dần", 1), "Canh": ("Tỵ", 1), "Nhâm": ("Thân", 1), "Ất": ("Ngọ", -1), "Đinh": ("Dậu", -1), "Kỷ": ("Dậu", -1), "Tân": ("Tý", -1), "Quý": ("Mão", -1)}
    start_chi, step = start_map[can_ngay]
    idx_start = DIA_CHI.index(start_chi)
    idx_chi = DIA_CHI.index(chi_dia_ban)
    if step == 1: idx = (idx_chi - idx_start) % 12
    else: idx = (idx_start - idx_chi) % 12
    return TRUONG_SINH_STATES[idx]

def xet_noi_ngoai_chien(tren, duoi):
    if la_khac(duoi, tren): return "NỘI CHIẾN (Gốc đâm Ngọn)"
    if la_khac(tren, duoi): return "NGOẠI CHIẾN (Ngọn đè Gốc)"
    if la_sinh(duoi, tren) or la_sinh(tren, duoi): return "TƯƠNG SINH (Hòa hợp)"
    return "TỶ HÒA (Bình hòa)"

def lap_12_thien_tuong_nang_cap(can_ngay, tru_da, thien_ban):
    QN_TRU = {"Giáp":"Sửu", "Mậu":"Sửu", "Canh":"Sửu", "Ất":"Tý", "Kỷ":"Tý", "Bính":"Hợi", "Đinh":"Hợi", "Nhâm":"Tỵ", "Quý":"Tỵ", "Tân":"Ngọ"}
    QN_DA = {"Giáp":"Mùi", "Mậu":"Mùi", "Canh":"Mùi", "Ất":"Thân", "Kỷ":"Thân", "Bính":"Dậu", "Đinh":"Dậu", "Nhâm":"Mão", "Quý":"Mão", "Tân":"Dần"}
    chi_qn = QN_TRU[can_ngay] if tru_da == "Ngày" else QN_DA[can_ngay]
    db_qn = [db for db, tb in thien_ban.items() if tb == chi_qn][0]
    idx_db_qn = DIA_CHI.index(db_qn)
    if idx_db_qn in [11, 0, 1, 2, 3, 4]: 
        step = 1; chieu_xoay = "THUẬN (Tiến lên - Cát thần thăng hoa, Hung thần bị khắc chế)"
    else: 
        step = -1; chieu_xoay = "NGHỊCH (Đi lùi - Rối ren, Cát thần kìm hãm, Hung thần được Buff tối đa)"
    thien_tuong_map = {DIA_CHI[(idx_db_qn + i * step) % 12]: THIEN_TUONG_LIST[i] for i in range(12)}
    return thien_tuong_map, chieu_xoay

def get_ung_ky_detail(thien_chi, thien_ban_dict, kv_ngay):
    dia_chi = [db for db, tb in thien_ban_dict.items() if tb == thien_chi][0]
    is_tk = thien_chi in kv_ngay
    mo_map = {"Mộc": "Mùi", "Hỏa": "Tuất", "Thổ": "Tuất", "Kim": "Sửu", "Thủy": "Thìn"}
    is_nm = dia_chi == mo_map.get(NGU_HANH[thien_chi])
    
    res = []
    if is_tk:
        res.append(f"XUẤT KHÔNG: Sự việc đang trống rỗng. Phải đợi đến Tháng/Ngày {thien_chi} (Điền thực lấp đầy) hoặc {XUNG_MAP[thien_chi]} (Xung để phá vỡ vỏ bọc) thì mới xảy ra.")
    if is_nm:
        res.append(f"PHÁ MỘ: Mọi thứ đang bị kẹt cứng ở kho {dia_chi}. Phải đợi đến đúng Tháng/Ngày {XUNG_MAP[dia_chi]} tông vỡ cửa kho thì mới giải quyết được.")
    if not is_tk and not is_nm:
        res.append(f"Nếu đang cãi vã, ly tán ➔ Đợi thời điểm {HOP_MAP[thien_chi]} để hòa hợp kết dính lại.")
        res.append(f"Nếu đang dây dưa, bế tắc ➔ Đợi thời điểm {XUNG_MAP[thien_chi]} để dứt điểm cắt đứt.")
    return res

def get_hinh(chi):
    hinh_dict = {"Tý":"Mão", "Mão":"Tý", "Dần":"Tỵ", "Tỵ":"Thân", "Thân":"Dần", "Sửu":"Tuất", "Tuất":"Mùi", "Mùi":"Sửu"}
    return hinh_dict.get(chi, chi)

def tinh_tam_truyen_chi_tiet(can_ngay, chi_ngay, thien_ban, tu_khoa):
    k1_t, k1_d = tu_khoa[0], KY_CUNG[can_ngay]
    k2_t, k2_d = tu_khoa[1], tu_khoa[0]
    k3_t, k3_d = tu_khoa[2], chi_ngay
    k4_t, k4_d = tu_khoa[3], tu_khoa[2]
    tu_khoa_cung = [(k1_t, k1_d), (k2_t, k2_d), (k3_t, k3_d), (k4_t, k4_d)]
    
    is_phuc_ngam = (thien_ban["Tý"] == "Tý")
    is_phan_ngam = (thien_ban["Tý"] == "Ngọ")

    tac_list = [(t, d) for t, d in tu_khoa_cung if la_khac(d, t)]
    khac_list = [(t, d) for t, d in tu_khoa_cung if la_khac(t, d)]
    
    cand_list = tac_list if tac_list else khac_list
    if cand_list:
        if len(cand_list) == 1:
            so = cand_list[0][0]
            ten_phap = "Tặc Khắc (Trùng Cơ)" if tac_list else "Tặc Khắc (Nguyên Thủ)"
            if is_phan_ngam: ten_phap = "Phản Ngâm (Vô Y)"
        else:
            ty_list = [uv for uv in cand_list if AM_DUONG[uv[0]] == AM_DUONG[can_ngay]]
            if len(ty_list) == 1:
                so = ty_list[0][0]
                ten_phap = "Tỷ Dụng (Tri Nhất)"
            else:
                ung_vien = ty_list if len(ty_list) > 1 else cand_list
                                
                # --- BƯỚC 1: ĐẾM SỐ BƯỚC THIỆP HẠI (ĐỘ SÂU DÀY VÒ) ---
                depth_uv = []
                for uv in ung_vien:
                    t_chi, d_chi = uv[0], uv[1]
                    start_idx = DIA_CHI.index(t_chi)
                    end_idx = DIA_CHI.index(d_chi)
                                    
                    # Tính số cung từ Bản vị Thiên Bàn đến cung Địa Bàn đang đậu
                    steps = (end_idx - start_idx + 12) % 12
                    if steps == 0: steps = 12
                                    
                    so_lan_day_vo = 0
                    # Quét các cung Địa Bàn dọc đường đi (tính cả Lâm cung đích đến)
                    for i in range(1, steps + 1):
                        cung_di_qua = DIA_CHI[(start_idx + i) % 12]
                        # Mỗi lần gặp Khắc nhập (Tặc) hoặc Khắc xuất (Khắc) là 1 lần chịu "dày vò"
                        if la_khac(cung_di_qua, t_chi) or la_khac(t_chi, cung_di_qua):
                            so_lan_day_vo += 1
                                            
                    depth_uv.append((uv, so_lan_day_vo))
                                
                # Lọc ra các ứng viên có số lần bị "dày vò" lớn nhất
                max_depth = max([x[1] for x in depth_uv])
                top_depth_uvs = [x[0] for x in depth_uv if x[1] == max_depth]
                                
                # --- BƯỚC 2: CHỈ XÉT MẠNH/TRỌNG/QUÝ NẾU ĐỘ SÂU HÒA NHAU ---
                if len(top_depth_uvs) == 1:
                    so = top_depth_uvs[0][0]
                else:
                    manh, trong = ["Dần", "Thân", "Tỵ", "Hợi"], ["Tý", "Ngọ", "Mão", "Dậu"]
                    # Gán điểm cho các ứng viên còn lại lọt qua vòng đếm bước
                    diem_uv = [(uv, 3 if uv[1] in manh else (2 if uv[1] in trong else 1)) for uv in top_depth_uvs]
                    max_diem = max([x[1] for x in diem_uv])
                    top_uvs = [x[0] for x in diem_uv if x[1] == max_diem]
                    so = top_uvs[0][0]
                                    
                ten_phap = "Thiệp Hại (Kiến Cơ)"
        trung = thien_ban[so]
        mat = thien_ban[trung]
        return so, trung, mat, ten_phap

    if is_phuc_ngam:
        so = k1_t if AM_DUONG[can_ngay] == "Dương" else k3_t
        trung = get_hinh(so)
        mat = get_hinh(trung)
        ten_phap = "Phục Ngâm (Tự Nhậm)"
        return so, trung, mat, ten_phap
        
    if KY_CUNG[can_ngay] == chi_ngay:
        if AM_DUONG[can_ngay] == "Dương":
            so = DIA_CHI[(DIA_CHI.index(k1_t) + 3) % 12]
        else:
            so = DIA_CHI[(DIA_CHI.index(k4_t) - 3) % 12]
        trung = k1_t
        mat = k1_t
        ten_phap = "Bát Chuyên (Vị Liệu)"
        return so, trung, mat, ten_phap

    dao_tac = [t for t in [k2_t, k3_t, k4_t] if la_khac(t, can_ngay)]
    dao_khac = [t for t in [k2_t, k3_t, k4_t] if la_khac(can_ngay, t)]
    if dao_tac or dao_khac:
        cand_list = dao_tac if dao_tac else dao_khac
        if len(cand_list) == 1:
            so = cand_list[0]
            ten_phap = "Dao Khắc (Hổ Thị)" if dao_tac else "Dao Khắc (Đạn Xạ)"
        else:
            ty_list = [uv for uv in cand_list if AM_DUONG[uv] == AM_DUONG[can_ngay]]
            if len(ty_list) == 1:
                so = ty_list[0]
                ten_phap = "Dao Khắc (Tỷ Dụng)"
            else:
                so = cand_list[0]
                ten_phap = "Dao Khắc (Thiệp Hại)"
        trung = thien_ban[so]
        mat = thien_ban[trung]
        return so, trung, mat, ten_phap

    unique_items = set([k1_t, k2_t, k3_t, k4_t])
    if len(unique_items) == 3:
        if AM_DUONG[can_ngay] == "Dương":
            hop_map = {"Giáp":"Kỷ", "Ất":"Canh", "Bính":"Tân", "Đinh":"Nhâm", "Mậu":"Quý", "Kỷ":"Giáp", "Canh":"Ất", "Tân":"Bính", "Nhâm":"Đinh", "Quý":"Mậu"}
            cung_hop = KY_CUNG[hop_map[can_ngay]]
            so = thien_ban[cung_hop]
        else:
            tam_hop_list = [["Dần", "Ngọ", "Tuất"], ["Hợi", "Mão", "Mùi"], ["Thân", "Tý", "Thìn"], ["Tỵ", "Dậu", "Sửu"]]
            for th in tam_hop_list:
                if chi_ngay in th:
                    idx = th.index(chi_ngay)
                    so = th[(idx - 1) % 3]
                    break
        trung = k1_t
        mat = k1_t
        ten_phap = "Biệt Trách (Bất Xuy)"
        return so, trung, mat, ten_phap

    if AM_DUONG[can_ngay] == "Dương":
        so = thien_ban["Dậu"]
        trung = k3_t
        mat = k1_t
    else:
        so = [db for db, tb in thien_ban.items() if tb == "Dậu"][0]
        trung = k1_t
        mat = k3_t
    ten_phap = "Mão Tinh (Ngạn Sơ)"
    return so, trung, mat, ten_phap

def parse_input_time(dt_str, cal_type):
    dt_obj = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M")
    if cal_type == "am":
        lunar_date = Lunar(dt_obj.year, dt_obj.month, dt_obj.day, isleap=False)
        solar_date = Converter.Lunar2Solar(lunar_date)
        return datetime(solar_date.year, solar_date.month, solar_date.day, dt_obj.hour, dt_obj.minute)
    return dt_obj

def get_can_chi_ngay(date_obj):
    delta = (date_obj.date() - datetime(1900, 1, 1).date()).days
    return THIEN_CAN[(0 + delta) % 10], DIA_CHI[(10 + delta) % 12]

def get_chi_gio(hour): return DIA_CHI[((hour + 1) // 2) % 12]
def get_can_gio(can_ngay, chi_gio):
    start_idx = {"Giáp":0, "Kỷ":0, "Ất":2, "Canh":2, "Bính":4, "Tân":4, "Đinh":6, "Nhâm":6, "Mậu":8, "Quý":8}[can_ngay]
    return THIEN_CAN[(start_idx + DIA_CHI.index(chi_gio)) % 10]

def tinh_can_chi_nam(year, month, day):
    if month == 1 or (month == 2 and day <= 3): year -= 1
    can_nam = ["Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ"][year % 10]
    chi_nam = ["Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi"][year % 12]
    return can_nam, chi_nam

def get_nguyet_kien(month, day):
    if (month == 2 and day >= 4) or (month == 3 and day <= 5): return "Dần"
    if (month == 3 and day >= 6) or (month == 4 and day <= 4): return "Mão"
    if (month == 4 and day >= 5) or (month == 5 and day <= 5): return "Thìn"
    if (month == 5 and day >= 6) or (month == 6 and day <= 5): return "Tỵ"
    if (month == 6 and day >= 6) or (month == 7 and day <= 6): return "Ngọ"
    if (month == 7 and day >= 7) or (month == 8 and day <= 7): return "Mùi"
    if (month == 8 and day >= 8) or (month == 9 and day <= 7): return "Thân"
    if (month == 9 and day >= 8) or (month == 10 and day <= 7): return "Dậu"
    if (month == 10 and day >= 8) or (month == 11 and day <= 6): return "Tuất"
    if (month == 11 and day >= 7) or (month == 12 and day <= 6): return "Hợi"
    if (month == 12 and day >= 7) or (month == 1 and day <= 5): return "Tý"
    if (month == 1 and day >= 6) or (month == 2 and day <= 3): return "Sửu"
    return "Dần"

def get_thang_am_can_chi(year, month, day, can_nam):
    chi_thang = get_nguyet_kien(month, day)
    start_can = {"Giáp":2, "Kỷ":2, "Ất":4, "Canh":4, "Bính":6, "Tân":6, "Đinh":8, "Nhâm":8, "Mậu":0, "Quý":0}[can_nam]
    offset = (DIA_CHI.index(chi_thang) - 2) % 12
    return THIEN_CAN[(start_can + offset) % 10], chi_thang

def get_nguyet_tuong(dt_obj, tz_offset=7.0):
    dt_utc = dt_obj - timedelta(hours=tz_offset)
    sun = ephem.Sun()
    sun.compute(ephem.Date(dt_utc))
    
    eq = ephem.Equatorial(sun.a_ra, sun.a_dec, epoch=ephem.Date(dt_utc))
    ecl = ephem.Ecliptic(eq)
    
    lon_deg = math.degrees(ecl.lon) % 360
    
    tuong_list = ["Tuất", "Dậu", "Thân", "Mùi", "Ngọ", "Tỵ", "Thìn", "Mão", "Dần", "Sửu", "Tý", "Hợi"]
    idx = int(lon_deg / 30)
    return tuong_list[idx]

def lap_thien_ban(nguyet_tuong, gio_gieo_que):
    idx_gio, idx_tuong = DIA_CHI.index(gio_gieo_que), DIA_CHI.index(nguyet_tuong)
    return {DIA_CHI[(idx_gio + i) % 12]: DIA_CHI[(idx_tuong + i) % 12] for i in range(12)}

def xac_dinh_tru_da(dt_obj, lat=21.0285, lon=105.8542, tz_offset=7.0):
    obs = ephem.Observer()
    obs.lat = str(lat)
    obs.lon = str(lon)
    obs.date = dt_obj - timedelta(hours=tz_offset) 
    sun = ephem.Sun()
    sun.compute(obs)
    if sun.alt > 0:
        return "Ngày"
    else:
        return "Đêm"

# ==========================================
# 5. FLASK ROUTE CHÍNH
# ==========================================
@app.route("/", methods=["GET", "POST"])
def index():
    tinh_ban = None
    if request.method == "POST":
        dt_str = request.form["thoi_gian_que"]
        lich_que = request.form.get("lich_que", "duong")
        
        try:
            lat = float(request.form.get("lat", 21.0285))
            lon = float(request.form.get("lon", 105.8542))
            tz_offset = float(request.form.get("tz_offset", 7.0))
        except:
            lat, lon, tz_offset = 21.0285, 105.8542, 7.0
            
        dt_que = parse_input_time(dt_str, lich_que)
        thoi_gian_sinh_str = request.form.get("thoi_gian_sinh", "")
        lich_sinh = request.form.get("lich_sinh", "duong")
        gioi_tinh = request.form.get("gioi_tinh", "Nam")

        if dt_que.hour >= 23: dt_que += timedelta(days=1)
        
        can_ngay, chi_ngay = get_can_chi_ngay(dt_que)
        can_nam, chi_nam = tinh_can_chi_nam(dt_que.year, dt_que.month, dt_que.day)
        can_thang, chi_thang = get_thang_am_can_chi(dt_que.year, dt_que.month, dt_que.day, can_nam)
        chi_gio = get_chi_gio(dt_que.hour)
        can_gio = get_can_gio(can_ngay, chi_gio)
        
        nguyet_tuong = get_nguyet_tuong(dt_que, tz_offset)
        nguyen = get_nguyen(can_ngay, chi_ngay)
        
        thien_ban = lap_thien_ban(nguyet_tuong, chi_gio)
        
        tru_da_input = request.form.get("tru_da", "Auto")
        if tru_da_input == "Auto":
            tru_da = xac_dinh_tru_da(dt_que, lat, lon, tz_offset)
            msg_tru_da = f"Tự động theo IP Ngầm (Lat: {lat:.2f}, Lon: {lon:.2f}): Ban {tru_da}"
        else:
            tru_da = tru_da_input
            msg_tru_da = f"Thiết lập thủ công: Ban {tru_da}"

        thien_tuong, chieu_xoay = lap_12_thien_tuong_nang_cap(can_ngay, tru_da, thien_ban)
        
        vong_thai_tue = lap_vong_thai_tue(chi_nam)
        kv_ngay = tinh_khong_vong(can_ngay, chi_ngay)

        k1_duoi = KY_CUNG[can_ngay]
        k1_tren = thien_ban[k1_duoi]
        k2_duoi = k1_tren
        k2_tren = thien_ban[k2_duoi]
        k3_duoi = chi_ngay
        k3_tren = thien_ban[k3_duoi]
        k4_duoi = k3_tren
        k4_tren = thien_ban[k4_duoi]
        
        tu_khoa = [k1_tren, k2_tren, k3_tren, k4_tren]
        
        tu_khoa_chi_tiet = [
            {
                "tren": k1_tren, "duoi": k1_duoi, 
                "ngu_hanh_tren_icon": nh_icon(NGU_HANH[k1_tren]),
                "ngu_hanh_duoi_icon": nh_icon(NGU_HANH[k1_duoi]),
                "quan_he": get_quan_he_chi(k1_tren, k1_duoi), 
                "tuong": thien_tuong[k1_duoi], 
                "ngu_hanh_tuong_icon": nh_icon(NGU_HANH[thien_tuong[k1_duoi]]),
                "luc_than": get_luc_than(can_ngay, k1_tren), 
                "noi_ngoai_chien": xet_noi_ngoai_chien(thien_tuong[k1_duoi], k1_tren), 
                "sinh_khac": get_quan_he_sinh_khac(k1_tren, k1_duoi),
                "is_tuan_khong": k1_tren in kv_ngay 
            },
            {
                "tren": k2_tren, "duoi": k2_duoi, 
                "ngu_hanh_tren_icon": nh_icon(NGU_HANH[k2_tren]),
                "ngu_hanh_duoi_icon": nh_icon(NGU_HANH[k2_duoi]),
                "quan_he": get_quan_he_chi(k2_tren, k2_duoi), 
                "tuong": thien_tuong[k2_duoi], 
                "ngu_hanh_tuong_icon": nh_icon(NGU_HANH[thien_tuong[k2_duoi]]),
                "luc_than": get_luc_than(can_ngay, k2_tren), 
                "noi_ngoai_chien": xet_noi_ngoai_chien(thien_tuong[k2_duoi], k2_tren), 
                "sinh_khac": get_quan_he_sinh_khac(k2_tren, k2_duoi),
                "is_tuan_khong": k2_tren in kv_ngay 
            },
            {
                "tren": k3_tren, "duoi": k3_duoi, 
                "ngu_hanh_tren_icon": nh_icon(NGU_HANH[k3_tren]),
                "ngu_hanh_duoi_icon": nh_icon(NGU_HANH[k3_duoi]),
                "quan_he": get_quan_he_chi(k3_tren, k3_duoi), 
                "tuong": thien_tuong[k3_duoi], 
                "ngu_hanh_tuong_icon": nh_icon(NGU_HANH[thien_tuong[k3_duoi]]),
                "luc_than": get_luc_than(can_ngay, k3_tren), 
                "noi_ngoai_chien": xet_noi_ngoai_chien(thien_tuong[k3_duoi], k3_tren), 
                "sinh_khac": get_quan_he_sinh_khac(k3_tren, k3_duoi),
                "is_tuan_khong": k3_tren in kv_ngay 
            },
            {
                "tren": k4_tren, "duoi": k4_duoi, 
                "ngu_hanh_tren_icon": nh_icon(NGU_HANH[k4_tren]),
                "ngu_hanh_duoi_icon": nh_icon(NGU_HANH[k4_duoi]),
                "quan_he": get_quan_he_chi(k4_tren, k4_duoi), 
                "tuong": thien_tuong[k4_duoi], 
                "ngu_hanh_tuong_icon": nh_icon(NGU_HANH[thien_tuong[k4_duoi]]),
                "luc_than": get_luc_than(can_ngay, k4_tren), 
                "noi_ngoai_chien": xet_noi_ngoai_chien(thien_tuong[k4_duoi], k4_tren), 
                "sinh_khac": get_quan_he_sinh_khac(k4_tren, k4_duoi),
                "is_tuan_khong": k4_tren in kv_ngay 
            }
        ]

        quan_he_k1_k3 = get_quan_he_chi(k1_tren, k3_tren)

        the_tran = ""
        the_tran_msg = ""
        if k1_tren == k1_duoi and k3_tren == k3_duoi:
            the_tran = "PHỤC NGÂM (Vũ trụ Đóng Băng)"
            the_tran_msg = "Mọi thứ kẹt cứng, dậm chân tại chỗ, bế tắc. Binh pháp: 'TỊNH' (Án binh bất động, tuyệt đối không xuất tiền hay thay đổi)."
        elif k1_tren == XUNG_MAP.get(k1_duoi) and k3_tren == XUNG_MAP.get(k3_duoi):
            the_tran = "PHẢN NGÂM (Vũ trụ Lật Bàn)"
            the_tran_msg = "Biến động thần tốc, đảo lộn, lật kèo phút chót. Binh pháp: 'ĐỘNG' (Đánh nhanh rút gọn, chuẩn bị sẵn Plan B, không ôm lâu)."

        nh_k1 = NGU_HANH[k1_tren]
        nh_k2 = NGU_HANH[k2_tren]
        nh_k3 = NGU_HANH[k3_tren]
        nh_k4 = NGU_HANH[k4_tren]
        
        # 1. TỔNG QUAN CAN CHI NGÀY (BƯỚC 1)
        nh_can_ngay = NGU_HANH[can_ngay]
        nh_chi_ngay = NGU_HANH[chi_ngay]
        
        if la_khac(nh_can_ngay, nh_chi_ngay):
            can_chi_msg = f"Can khắc Chi ({nh_can_ngay} khắc {nh_chi_ngay}): TA nắm thế chủ động, kiểm soát được hoàn cảnh và đối tác."
        elif la_khac(nh_chi_ngay, nh_can_ngay):
            can_chi_msg = f"Chi khắc Can ({nh_chi_ngay} khắc {nh_can_ngay}): Hoàn cảnh/Đối tác gây áp lực, TA bị chèn ép, mệt mỏi thụ động."
        elif la_sinh(nh_can_ngay, nh_chi_ngay):
            can_chi_msg = f"Can sinh Chi ({nh_can_ngay} sinh {nh_chi_ngay}): SINH XUẤT. TA phải chủ động đi hao tâm tổn trí, chạy theo chăm lo cho sự việc."
        elif la_sinh(nh_chi_ngay, nh_can_ngay):
            can_chi_msg = f"Chi sinh Can ({nh_chi_ngay} sinh {nh_can_ngay}): QUÁ TỐT (Sinh nhập). Hoàn cảnh ưu ái, đối tác mang lợi ích tự tìm đến TA."
        else:
            can_chi_msg = f"Tỷ Hòa ({nh_can_ngay} - {nh_chi_ngay}): Hoàn cảnh và TA ngang thế, bình đẳng, môi trường thuận hòa."
            
        quan_he_can_chi = {
            "can_ngay_icon": nh_icon(nh_can_ngay),
            "chi_ngay_icon": nh_icon(nh_chi_ngay),
            "msg": can_chi_msg
        }
        
        if la_khac(nh_k1, nh_k3): ngang_msg = f"Ta ({nh_k1}) khắc Khách ({nh_k3}): Ta nắm đằng chuôi, chiếm ưu thế, ép giá."
        elif la_khac(nh_k3, nh_k1): ngang_msg = f"Khách ({nh_k3}) khắc Ta ({nh_k1}): Đối tác cửa trên, Ta bị chèn ép, vùi dập."
        elif la_sinh(nh_k1, nh_k3): ngang_msg = f"Ta ({nh_k1}) sinh Khách ({nh_k3}): Ta hao tâm tổn trí, vất vả chạy theo phục vụ đối phương."
        elif la_sinh(nh_k3, nh_k1): ngang_msg = f"Khách ({nh_k3}) sinh Ta ({nh_k1}): Đối tác nhượng bộ, mang lợi lộc, dâng cỗ cho Ta."
        else: ngang_msg = f"Tỷ Hòa ({nh_k1}-{nh_k3}): Hai bên ngang thế, bình đẳng trên bàn đàm phán."

        if la_khac(nh_k1, nh_k4): k1_k4_msg = f"Ta ({nh_k1}) tấn công/kiểm soát sân sau Khách ({nh_k4})"
        elif la_khac(nh_k4, nh_k1): k1_k4_msg = f"Sân sau Khách ({nh_k4}) uy hiếp Ta ({nh_k1})"
        elif la_sinh(nh_k1, nh_k4): k1_k4_msg = f"Ta ({nh_k1}) bồi đắp/nuôi dưỡng sân sau Khách ({nh_k4})"
        elif la_sinh(nh_k4, nh_k1): k1_k4_msg = f"Sân sau Khách ({nh_k4}) mang lợi lộc cho Ta ({nh_k1})"
        else: k1_k4_msg = f"Ta ({nh_k1}) và sân sau Khách ({nh_k4}) hòa hoãn (Tỷ Hòa)"

        if la_khac(nh_k3, nh_k2): k3_k2_msg = f"Khách ({nh_k3}) phá nát/rút ruột sân sau Ta ({nh_k2})"
        elif la_khac(nh_k2, nh_k3): k3_k2_msg = f"Sân sau Ta ({nh_k2}) phản kích/kiểm soát Khách ({nh_k3})"
        elif la_sinh(nh_k3, nh_k2): k3_k2_msg = f"Khách ({nh_k3}) bồi đắp/đầu tư cho sân sau Ta ({nh_k2})"
        elif la_sinh(nh_k2, nh_k3): k3_k2_msg = f"Sân sau Ta ({nh_k2}) bị vắt kiệt/hút máu để nuôi Khách ({nh_k3})"
        else: k3_k2_msg = f"Khách ({nh_k3}) và sân sau Ta ({nh_k2}) hòa hoãn (Tỷ Hòa)"

        if (la_sinh(nh_k1, nh_k4) or la_sinh(nh_k4, nh_k1)) and (la_sinh(nh_k3, nh_k2) or la_sinh(nh_k2, nh_k3)):
            giao_xa_kL = "HỖ SINH (Đại Win-Win): Đôi bên cùng có lợi tột độ. Âm thầm nuôi dưỡng hậu phương của nhau. Hợp tác tuyệt vời!"
        elif (la_khac(nh_k1, nh_k4) or la_khac(nh_k4, nh_k1)) and (la_khac(nh_k3, nh_k2) or la_khac(nh_k2, nh_k3)):
            giao_xa_kL = "HỖ KHẮC (Bữa tiệc đẫm máu): Cẩn thận! Bề ngoài có thể êm đẹp nhưng bắt chéo lại ngầm gài bẫy, triệt hạ hậu phương của nhau."
        elif la_sinh(nh_k3, nh_k1) and la_sinh(nh_k2, nh_k3):
            giao_xa_kL = "MẬT NGỌT CHẾT RUỒI (Rút củi đáy nồi): Khách tỏ ra nhún nhường bề ngoài, nhưng thực chất đang âm thầm vắt kiệt tài nguyên (sân sau) của bạn!"
        else:
            giao_xa_kL = "Giao Xa bình thường, diễn biến theo bề nổi."

        if la_khac(nh_k1, nh_k2) or la_khac(nh_k2, nh_k1):
            noi_bo_ta_msg = "TỰ KHẮC: Nội bộ bên Ta đang lục đục, bản thân do dự, có mâu thuẫn nội tại."
        else:
            noi_bo_ta_msg = "Hòa hợp: Nội bộ bên Ta đồng lòng, bản thân kiên định."

        if la_khac(nh_k3, nh_k4) or la_khac(nh_k4, nh_k3):
            noi_bo_khach_msg = "TỰ KHẮC: Công ty/Đối tác kia rỗng tuếch, đang có phốt, thùng rỗng kêu to."
        else:
            noi_bo_khach_msg = "Hòa hợp: Công ty/Đối tác kia có nền tảng vững vàng, nội bộ đoàn kết."

        dong_luc_hoc = {
            "quet_ngang": ngang_msg,
            "k1_k4": k1_k4_msg,
            "k3_k2": k3_k2_msg,
            "giao_xa_ket_luan": giao_xa_kL,
            "noi_bo_ta": noi_bo_ta_msg,       
            "noi_bo_khach": noi_bo_khach_msg  
        }

        so, trung, mat, ten_phap = tinh_tam_truyen_chi_tiet(can_ngay, chi_ngay, thien_ban, tu_khoa)
        
        so_tuong = thien_tuong[[db for db, tb in thien_ban.items() if tb == so][0]]
        trung_tuong = thien_tuong[[db for db, tb in thien_ban.items() if tb == trung][0]]
        mat_tuong = thien_tuong[[db for db, tb in thien_ban.items() if tb == mat][0]]
        
        so_lt = get_luc_than(can_ngay, so)
        trung_lt = get_luc_than(can_ngay, trung)
        mat_lt = get_luc_than(can_ngay, mat)

        so_vs = tinh_vuong_suy(so, chi_thang)
        trung_vs = tinh_vuong_suy(trung, chi_thang)
        mat_vs = tinh_vuong_suy(mat, chi_thang)

        def phan_tich_tinh_chat_kv(is_tk, tuong, luc_than, vuong_suy):
            if not is_tk: return None
            hung_than_sao = ["Bạch Hổ", "Đằng Xà", "Chu Tước", "Câu Trần", "Huyền Vũ", "Thiên Không"]
            hung_luc_than = ["Quan Quỷ"]
            is_hung = tuong in hung_than_sao or luc_than in hung_luc_than
            cat_hung_msg = "RẤT TỐT (Hung phùng Không): Họa biến mất, bom xịt ngòi, tai ách tự tiêu tan." if is_hung else "RẤT XẤU (Cát phùng Không): Tin vui bị dập tắt, tài lộc/quý nhân chỉ là hư ảo."
            
            is_gia = "VƯỢNG" in vuong_suy or "TƯỚNG" in vuong_suy
            chan_gia_msg = "GIẢ KHÔNG (Khí Vượng/Tướng): Trống rỗng tạm thời. Chờ thời điểm Xuất Không/Xung Không sẽ bùng nổ hiện thực." if is_gia else "TUYỆT KHÔNG (Khí Hưu/Tù/Tử): Chết hẳn, vĩnh viễn không bao giờ thành sự thật."
            
            return {"cat_hung": cat_hung_msg, "chan_gia": chan_gia_msg}

        khong_vong_msg = []
        if (k1_tren in kv_ngay) or (k2_tren in kv_ngay):
            khong_vong_msg.append("🛡️ KHÓA 1/2 (Phe Ta) KHÔNG VONG: Bạn đang bị rỗng tuếch, do dự, thiếu năng lực hoặc nguồn vốn chỉ là ảo.")
        if (k3_tren in kv_ngay) or (k4_tren in kv_ngay):
            khong_vong_msg.append("🎭 KHÓA 3/4 (Phe Khách) KHÔNG VONG: Đối tác đang 'phông bạt', dự án bánh vẽ, nội bộ trống rỗng, không có thực lực.")
        if so in kv_ngay:
            khong_vong_msg.append("🎬 SƠ TRUYỀN KHÔNG VONG: Khởi đầu chỉ là hô hào suông, có tiếng không có miếng, sự việc nằm trên ý tưởng.")
        if trung in kv_ngay:
            khong_vong_msg.append("🚧 TRUNG TRUYỀN KHÔNG VONG: Giữa chừng gãy gánh, đứt đoạn liên lạc, mất phương hướng không biết làm gì tiếp.")
        if mat in kv_ngay:
            khong_vong_msg.append("🛑 MẠT TRUYỀN KHÔNG VONG: 'Xôi hỏng bỏng không'. Dù quá trình có đẹp đến mấy, kết quả cuối cùng vẫn là con số 0.")

        so_am_than = thien_ban[so]
        trung_am_than = thien_ban[trung]
        mat_am_than = thien_ban[mat]
        
        so_don_can = get_don_can(can_ngay, chi_ngay, so)
        trung_don_can = get_don_can(can_ngay, chi_ngay, trung)
        mat_don_can = get_don_can(can_ngay, chi_ngay, mat)

        ung_ky_so = get_ung_ky_detail(so, thien_ban, kv_ngay)
        ung_ky_trung = get_ung_ky_detail(trung, thien_ban, kv_ngay)
        ung_ky_mat = get_ung_ky_detail(mat, thien_ban, kv_ngay)

        tam_truyen_chi_tiet = {
            "so": {
                "chi": so, 
                "ngu_hanh_chi_icon": nh_icon(NGU_HANH[so]),
                "tuong": so_tuong, 
                "ngu_hanh_tuong_icon": nh_icon(NGU_HANH[so_tuong]),
                "luc_than": so_lt, 
                "vuong_suy": so_vs, 
                "noi_ngoai_chien": xet_noi_ngoai_chien(so_tuong, so),
                "am_than": so_am_than,
                "ngu_hanh_am_than_icon": nh_icon(NGU_HANH[so_am_than]),
                "am_than_tuong": thien_tuong[so],
                "ngu_hanh_am_than_tuong_icon": nh_icon(NGU_HANH[thien_tuong[so]]),
                "don_can": so_don_can,
                "don_can_luc_than": get_luc_than(can_ngay, so_don_can) if so_don_can != "Không" else "",
                "ung_ky": ung_ky_so,
                "is_tuan_khong": so in kv_ngay,
                "kv_tinh_chat": phan_tich_tinh_chat_kv(so in kv_ngay, so_tuong, so_lt, so_vs)
            },
            "trung": {
                "chi": trung, 
                "ngu_hanh_chi_icon": nh_icon(NGU_HANH[trung]),
                "tuong": trung_tuong, 
                "ngu_hanh_tuong_icon": nh_icon(NGU_HANH[trung_tuong]),
                "luc_than": trung_lt, 
                "vuong_suy": trung_vs, 
                "noi_ngoai_chien": xet_noi_ngoai_chien(trung_tuong, trung),
                "am_than": trung_am_than,
                "ngu_hanh_am_than_icon": nh_icon(NGU_HANH[trung_am_than]),
                "am_than_tuong": thien_tuong[trung],
                "ngu_hanh_am_than_tuong_icon": nh_icon(NGU_HANH[thien_tuong[trung]]),
                "don_can": trung_don_can,
                "don_can_luc_than": get_luc_than(can_ngay, trung_don_can) if trung_don_can != "Không" else "",
                "ung_ky": ung_ky_trung,
                "is_tuan_khong": trung in kv_ngay,
                "kv_tinh_chat": phan_tich_tinh_chat_kv(trung in kv_ngay, trung_tuong, trung_lt, trung_vs)
            },
            "mat": {
                "chi": mat, 
                "ngu_hanh_chi_icon": nh_icon(NGU_HANH[mat]),
                "tuong": mat_tuong, 
                "ngu_hanh_tuong_icon": nh_icon(NGU_HANH[mat_tuong]),
                "luc_than": mat_lt, 
                "vuong_suy": mat_vs, 
                "noi_ngoai_chien": xet_noi_ngoai_chien(mat_tuong, mat),
                "am_than": mat_am_than,
                "ngu_hanh_am_than_icon": nh_icon(NGU_HANH[mat_am_than]),
                "am_than_tuong": thien_tuong[mat],
                "ngu_hanh_am_than_tuong_icon": nh_icon(NGU_HANH[thien_tuong[mat]]),
                "don_can": mat_don_can,
                "don_can_luc_than": get_luc_than(can_ngay, mat_don_can) if mat_don_can != "Không" else "",
                "ung_ky": ung_ky_mat,
                "is_tuan_khong": mat in kv_ngay,
                "kv_tinh_chat": phan_tich_tinh_chat_kv(mat in kv_ngay, mat_tuong, mat_lt, mat_vs)
            },
            "ten_phap": ten_phap,
            "quan_he_so_mat": get_quan_he_chi(so, mat),
            "tien_thoai": get_tien_thoai_tam_truyen(so, trung, mat),  # BỔ SUNG: Tiến Thoái
            "cuc_dien": get_cuc_dien_tam_truyen(so, trung, mat),
            "lat_keo_mat_can": xet_lat_keo_mat_vs_can_ngay(mat, can_ngay) # BỔ SUNG: Chốt hạ Mạt vs Can Ngày
        }

        sinh_than_data = None
        phuong_an_lat_keo = ""
        c_chi_nam_s = None
        hanh_nien = None
        nt_menh_msg = ""
        
        if thoi_gian_sinh_str:
            dt_sinh = parse_input_time(thoi_gian_sinh_str, lich_sinh)
            if dt_sinh.hour >= 23: dt_sinh += timedelta(days=1)
            c_ngay_s, c_chi_s = get_can_chi_ngay(dt_sinh)
            c_nam_s, c_chi_nam_s = tinh_can_chi_nam(dt_sinh.year, dt_sinh.month, dt_sinh.day)
            c_thang_s, c_chi_thang_s = get_thang_am_can_chi(dt_sinh.year, dt_sinh.month, dt_sinh.day, c_nam_s)
            c_chi_gio_s = get_chi_gio(dt_sinh.hour)
            c_can_gio_s = get_can_gio(c_ngay_s, c_chi_gio_s)
            
            hanh_nien = tinh_hanh_nien(c_chi_nam_s, chi_nam, gioi_tinh)
            phuong_an_lat_keo = xet_lat_keo_ban_menh(mat, c_chi_nam_s)
            # --- TUYỆT KỸ BỔ SUNG: THƯỢNG THẦN BẢN MỆNH & HÀNH NIÊN ---
            thuong_than_menh = thien_ban[c_chi_nam_s]
            tt_menh_lt = get_luc_than(can_ngay, thuong_than_menh)
            tt_menh_tuong = thien_tuong[c_chi_nam_s]
            
            thuong_than_hn = thien_ban[hanh_nien]
            tt_hn_lt = get_luc_than(can_ngay, thuong_than_hn)
            tt_hn_tuong = thien_tuong[hanh_nien]
            
            thuong_than_msg = f"Đè trên Bản Mệnh là {thuong_than_menh} ({tt_menh_lt} + {tt_menh_tuong}). Đè trên Vận năm nay là {thuong_than_hn} ({tt_hn_lt} + {tt_hn_tuong})."
            # -----------------------------------------------------------

            if thien_ban[c_chi_nam_s] == nguyet_tuong:
                nt_menh_msg = f"NGUYỆT TƯỚNG ({nguyet_tuong}) ĐẬU CUNG BẢN MỆNH ({c_chi_nam_s}): Có bề trên che chở, có phép màu cứu vớt phút chót!"
            
            sinh_than_data = {
                "gioi_tinh": gioi_tinh,
                "tu_tru": {"nam": f"{c_nam_s} {c_chi_nam_s}", "thang": f"{c_thang_s} {c_chi_thang_s}", "ngay": f"{c_ngay_s} {c_chi_s}", "gio": f"{c_can_gio_s} {c_chi_gio_s}"},
                "khong_vong": {"ngay": tinh_khong_vong(c_ngay_s, c_chi_s)},
                "menh": c_chi_nam_s, 
                "nhat_chu_can": c_ngay_s, 
                "nhat_chu_hanh": NGU_HANH[c_ngay_s],
                "hanh_nien": hanh_nien,
                "thuong_than_msg": thuong_than_msg, # <-- Truyền ra HTML
                "lat_keo": phuong_an_lat_keo
            }

        mo_map = {"Mộc": "Mùi", "Hỏa": "Tuất", "Thổ": "Tuất", "Kim": "Sửu", "Thủy": "Thìn"}
        thien_dia_ban = []
        for idx, dia in enumerate(DIA_CHI):
            thien = thien_ban[dia]
            tuong = thien_tuong[dia]
            vuong_suy = tinh_vuong_suy(thien, chi_thang)
            truong_sinh = get_12_truong_sinh(can_ngay, dia)
            is_tk = thien in kv_ngay
            is_nm = (dia == mo_map.get(NGU_HANH[thien]))
            
            tuong_than_chien = xet_noi_ngoai_chien(tuong, thien)
            thien_dia_chien = xet_noi_ngoai_chien(thien, dia)
            
            is_chiem_thoi = (dia == chi_gio)
            is_nguyet_tuong = (thien == nguyet_tuong)
            is_ban_menh = (dia == c_chi_nam_s) if c_chi_nam_s else False
            is_hanh_nien = (dia == hanh_nien) if hanh_nien else False
            
            don_can_cung = get_don_can(can_ngay, chi_ngay, dia)
            don_can_luc_than = get_luc_than(can_ngay, don_can_cung) if don_can_cung != "Không" else ""
            
            thien_dia_ban.append({
                "dia": dia, "thien": thien, 
                "ngu_hanh_dia": NGU_HANH[dia],
                "ngu_hanh_thien": NGU_HANH[thien],
                "ngu_hanh_tuong": NGU_HANH[tuong],
                "ngu_hanh": NGU_HANH[thien],
                "tuong": tuong, 
                "tuong_than_chien": tuong_than_chien,
                "thien_dia_chien": thien_dia_chien,
                "thai_tue": vong_thai_tue[thien],
                "loai_than": get_loai_than(chi_ngay, idx),
                "luc_than": get_luc_than(can_ngay, thien),
                "than_sat": tinh_than_sat_thien_ban(can_ngay, chi_ngay, chi_nam, chi_thang, thien, kv_ngay),
                "vuong_suy": vuong_suy, "truong_sinh": truong_sinh,
                "is_tuan_khong": is_tk, "is_nhap_mo": is_nm,
                "is_chiem_thoi": is_chiem_thoi,
                "is_nguyet_tuong": is_nguyet_tuong,
                "is_ban_menh": is_ban_menh,
                "is_hanh_nien": is_hanh_nien,
                "don_can": don_can_cung,
                "don_can_luc_than": don_can_luc_than
            })
            
        canh_bao_tat_phap = quet_100_tat_phap_phu(tu_khoa_chi_tiet, tam_truyen_chi_tiet, kv_ngay, can_ngay)

        nh_thai_tue = NGU_HANH[chi_nam]
        nh_nguyet_kien = NGU_HANH[chi_thang]
        nh_so_truyen = NGU_HANH[so]

        if la_khac(nh_thai_tue, nh_so_truyen):
            tt_so_msg = f"THÁI TUẾ KHẮC SƠ TRUYỀN ({nh_thai_tue} khắc {nh_so_truyen}) -> ĐẠI HUNG: Đi ngược vĩ mô, pháp luật, sếp lớn đè bẹp. Dự án sụp đổ!"
        elif la_sinh(nh_thai_tue, nh_so_truyen):
            tt_so_msg = f"THÁI TUẾ SINH SƠ TRUYỀN ({nh_thai_tue} sinh {nh_so_truyen}) -> ĐẠI CÁT: Thuận Đạo trời, được chính sách/xu hướng ủng hộ."
        else:
            tt_so_msg = f"Bình hòa ({nh_thai_tue} - {nh_so_truyen}): Không bị Thái Tuế cản trở."

        if la_khac(nh_nguyet_kien, nh_so_truyen):
            nk_so_msg = f"NGUYỆT KIẾN KHẮC SƠ TRUYỀN ({nh_nguyet_kien} khắc {nh_so_truyen}) -> LƯU Ý: Bị quan chức địa phương, sếp trực tiếp chèn ép."
        elif la_sinh(nh_nguyet_kien, nh_so_truyen):
            nk_so_msg = f"NGUYỆT KIẾN SINH SƠ TRUYỀN ({nh_nguyet_kien} sinh {nh_so_truyen}) -> TỐT: Được cấp trên trực tiếp nâng đỡ."
        else:
            nk_so_msg = f"Bình hòa ({nh_nguyet_kien} - {nh_so_truyen}): Không bị Nguyệt Kiến cản trở."

        vi_mo_data = {
            "thai_tue": tt_so_msg,
            "nguyet_kien": nk_so_msg,
            "nguyet_tuong_menh": nt_menh_msg
        }

        tinh_ban = {
            "time_str": dt_que.strftime("%d/%m/%Y %H:%M"),
            "loai_lich_que": "Âm" if lich_que == "am" else "Dương",
            "tru_da": tru_da,              
            "msg_tru_da": msg_tru_da,
            "chieu_xoay": chieu_xoay,      
            "tu_tru": {"nam": f"{can_nam} {chi_nam}", "thang": f"{can_thang} {chi_thang}", "ngay": f"{can_ngay} {chi_ngay}", "gio": f"{can_gio} {chi_gio}"},
            "chiem_thoi": chi_gio,
            "khong_vong": {"ngay": kv_ngay},
            "thai_tue": chi_nam, "nguyet_kien": chi_thang, "nguyet_tuong": nguyet_tuong,
            "nguyen": nguyen, "cuu_tong_mon": ten_phap,
            "can_ngay": can_ngay, "chi_ngay": chi_ngay,
            "quan_he_can_chi": quan_he_can_chi,
            "tu_khoa": tu_khoa_chi_tiet,
            "dong_luc_hoc": dong_luc_hoc,
            "quan_he_k1_k3": quan_he_k1_k3,
            "tam_truyen": tam_truyen_chi_tiet,
            "the_tran": the_tran,           
            "the_tran_msg": the_tran_msg,   
            "thien_dia_ban": thien_dia_ban,
            "sinh_than": sinh_than_data,
            "canh_bao_tat_phap": canh_bao_tat_phap,
            "vi_mo": vi_mo_data,
            "khong_vong_msg": khong_vong_msg
        }
    return render_template("index.html", tinh_ban=tinh_ban)

if __name__ == "__main__":
    app.run(debug=True)