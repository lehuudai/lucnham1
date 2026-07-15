from flask import Flask, render_template, request
from datetime import datetime, timedelta
from lunarcalendar import Converter, Solar, Lunar

app = Flask(__name__)

# --- HỆ THỐNG DỮ LIỆU CƠ BẢN ---
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

# --- CÁC HÀM TÍNH TOÁN CƠ BẢN ---
def tinh_khong_vong(can, chi):
    idx_khong_1 = (DIA_CHI.index(chi) - THIEN_CAN.index(can) - 2) % 12
    return [DIA_CHI[idx_khong_1], DIA_CHI[(idx_khong_1 + 1) % 12]]

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

def la_khac(A, B):
    return {"Mộc":"Thổ", "Thổ":"Thủy", "Thủy":"Hỏa", "Hỏa":"Kim", "Kim":"Mộc"}.get(NGU_HANH.get(A)) == NGU_HANH.get(B)

def la_sinh(A, B):
    return {"Mộc":"Hỏa", "Hỏa":"Thổ", "Thổ":"Kim", "Kim":"Thủy", "Thủy":"Mộc"}.get(NGU_HANH.get(A)) == NGU_HANH.get(B)

def get_quan_he_sinh_khac(tren, duoi):
    """Tính toán mỗi quan hệ giữa Thượng và Hạ trong Tứ Khóa"""
    if la_khac(duoi, tren): return "↑ Khắc (Tặc)" # Hạ tặc Thượng
    if la_khac(tren, duoi): return "↓ Khắc"       # Thượng khắc Hạ
    if la_sinh(duoi, tren): return "↑ Sinh"       # Hạ sinh Thượng
    if la_sinh(tren, duoi): return "↓ Sinh"       # Thượng sinh Hạ
    return "= Tỷ Hòa"                             # Cùng ngũ hành

def lap_vong_thai_tue(nam_chi):
    sao_tue = ["Thái Tuế", "Thái Dương", "Tang Môn", "Thái Âm", "Quan Phù", "Tử Phù", "Tuế Phá", "Long Đức", "Bạch Hổ", "Phúc Đức", "Điếu Khách", "Bệnh Phù"]
    start_idx = DIA_CHI.index(nam_chi)
    return {DIA_CHI[(start_idx + i) % 12]: sao_tue[i] for i in range(12)}

def get_loai_than(day_chi, di_ban_idx):
    idx = (di_ban_idx - DIA_CHI.index(day_chi) + 12) % 12
    return LOAI_THAN_NAMES[idx]

def tinh_than_sat_thien_ban(can_ngay, chi_ngay, chi_nam, thien_ban_chi, kv_ngay):
    sat = []
    if thien_ban_chi == {"Giáp":"Dần", "Ất":"Mão", "Bính":"Tỵ", "Đinh":"Ngọ", "Mậu":"Tỵ", "Kỷ":"Ngọ", "Canh":"Thân", "Tân":"Dậu", "Nhâm":"Hợi", "Quý":"Tý"}.get(can_ngay): sat.append("Thiên Lộc")
    if thien_ban_chi == {"Thân":"Dần", "Tý":"Dần", "Thìn":"Dần", "Dần":"Thân", "Ngọ":"Thân", "Tuất":"Thân", "Tỵ":"Hợi", "Dậu":"Hợi", "Sửu":"Hợi", "Hợi":"Tỵ", "Mão":"Tỵ", "Mùi":"Tỵ"}.get(chi_ngay): sat.append("Thiên Mã")
    if thien_ban_chi == {"Thân":"Dậu", "Tý":"Dậu", "Thìn":"Dậu", "Dần":"Mão", "Ngọ":"Mão", "Tuất":"Mão", "Tỵ":"Ngọ", "Dậu":"Ngọ", "Sửu":"Ngọ", "Hợi":"Tý", "Mão":"Tý", "Mùi":"Tý"}.get(chi_ngay): sat.append("Đào Hoa")
    
    hoa_cai_map = {"Thân":"Thìn", "Tý":"Thìn", "Thìn":"Thìn", "Dần":"Tuất", "Ngọ":"Tuất", "Tuất":"Tuất", "Tỵ":"Sửu", "Dậu":"Sửu", "Sửu":"Sửu", "Hợi":"Mùi", "Mão":"Mùi", "Mùi":"Mùi"}
    if thien_ban_chi == hoa_cai_map.get(chi_ngay): sat.append("Hoa Cái")
    
    if thien_ban_chi == DIA_CHI[(DIA_CHI.index(chi_nam) + 6) % 12]: sat.append("Tuế Phá (Phá Toái)") 
    if thien_ban_chi in kv_ngay: sat.append("Tuần Không")
    
    hinh_map = {"Dần":"Tỵ", "Tỵ":"Thân", "Thân":"Dần", "Sửu":"Tuất", "Tuất":"Mùi", "Mùi":"Sửu", "Tý":"Mão", "Mão":"Tý", "Thìn":"Thìn", "Ngọ":"Ngọ", "Dậu":"Dậu", "Hợi":"Hợi"}
    if thien_ban_chi == hinh_map.get(chi_ngay): sat.append("Thiên Hình")
    
    return sat

# --- 3 LỚP BỘ LỌC SINH TỬ ---
def tinh_vuong_suy(chi_can_xet, chi_thang):
    h_xet, h_thang = NGU_HANH[chi_can_xet], NGU_HANH[chi_thang]
    if h_xet == h_thang: return "VƯỢNG"
    if la_sinh(h_thang, h_xet): return "TƯỚNG"
    if la_sinh(h_xet, h_thang): return "HƯU"
    if la_khac(h_xet, h_thang): return "TÙ"
    if la_khac(h_thang, h_xet): return "TỬ"
    return ""

def xet_noi_ngoai_chien(thien_tuong, dia_chi_than):
    if la_khac(dia_chi_than, thien_tuong): return "NỘI CHIẾN (Gốc đâm Ngọn)"
    if la_khac(thien_tuong, dia_chi_than): return "NGOẠI CHIẾN (Ngọn đè Gốc)"
    return "Hòa Hợp"

def quet_tat_phap_phu(tu_khoa, tam_truyen, khong_vong_ngay, can_ngay):
    canh_bao = []
    so, trung, mat = tam_truyen["so"]["chi"], tam_truyen["trung"]["chi"], tam_truyen["mat"]["chi"]
    
    if tam_truyen["so"]["luc_than"] == "Quan Quỷ" and tam_truyen["mat"]["luc_than"] == "Quan Quỷ":
        canh_bao.append("⚠️ QUỶ LÂM SƠ MẠT: Cảnh báo Đại Hung! Tai họa ập đầu, kết cục bi đát, kiện tụng bế tắc. Tuyệt đối không phản công!")
        
    tuong_so, tuong_trung, tuong_mat = tam_truyen["so"]["tuong"], tam_truyen["trung"]["tuong"], tam_truyen["mat"]["tuong"]
    if ("Chu Tước" in [tuong_so, tuong_trung, tuong_mat] and (so in khong_vong_ngay or trung in khong_vong_ngay or mat in khong_vong_ngay)) or \
       (tam_truyen["so"]["luc_than"] == "Phụ Mẫu" and so in khong_vong_ngay) or (tam_truyen["mat"]["luc_than"] == "Phụ Mẫu" and mat in khong_vong_ngay):
        canh_bao.append("⚠️ BẾ KHẨU QUÁI: Giấy tờ bị bác bỏ, ra tòa cấm khẩu, đuối lý, có oan không kêu được.")
        
    for khoa in tu_khoa:
        if khoa["tren"] == "Tuất" and khoa["duoi"] == "Hợi":
            canh_bao.append("⚠️ KHÔI ĐỘ THIÊN MÔN: Ác thần chặn cổng trời. Lưới trời lồng lộng, chạy trời không khỏi nắng, bế tắc toàn tập.")
            break
            
    if la_sinh(so, trung) and la_sinh(mat, trung):
        canh_bao.append("✅ TIỀN HẬU DẪN TÙNG: Đại Cát! Trước có người dẹp đường, sau có người che chở. Thăng quan tiến chức.")
        
    return canh_bao

# --- CÁC HÀM XỬ LÝ LỊCH PHÁP & LẬP QUẺ ---
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

def tinh_can_chi_nam(year):
    return ["Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ"][year % 10], ["Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi"][year % 12]

def get_nguyet_tuong(month, day):
    tm = [("Tý", 1, 20), ("Hợi", 2, 19), ("Tuất", 3, 21), ("Dậu", 4, 20), ("Thân", 5, 21), ("Mùi", 6, 21), ("Ngọ", 7, 23), ("Tỵ", 8, 23), ("Thìn", 9, 23), ("Mão", 10, 23), ("Dần", 11, 22), ("Sửu", 12, 22)]
    for tuong, m, d in tm:
        if (month == m and day >= d) or (month == (m % 12) + 1 and day < tm[(m % 12)][2]): return tuong
    return "Tý"

def get_thang_am_can_chi(year, month, can_nam):
    chi_thang = DIA_CHI[(month + 1) % 12]
    start_can = {"Giáp":2, "Kỷ":2, "Ất":4, "Canh":4, "Bính":6, "Tân":6, "Đinh":8, "Nhâm":8, "Mậu":0, "Quý":0}[can_nam]
    return THIEN_CAN[(start_can + month - 1) % 10], chi_thang

def lap_thien_ban(nguyet_tuong, gio_gieo_que):
    idx_gio, idx_tuong = DIA_CHI.index(gio_gieo_que), DIA_CHI.index(nguyet_tuong)
    return {DIA_CHI[(idx_gio + i) % 12]: DIA_CHI[(idx_tuong + i) % 12] for i in range(12)}

def lap_12_thien_tuong(can_ngay, gio_que_chi, thien_ban):
    QN_TRU = {"Giáp":"Sửu", "Mậu":"Sửu", "Canh":"Sửu", "Ất":"Tý", "Kỷ":"Tý", "Bính":"Hợi", "Đinh":"Hợi", "Nhâm":"Tỵ", "Quý":"Tỵ", "Tân":"Ngọ"}
    QN_DA = {"Giáp":"Mùi", "Mậu":"Mùi", "Canh":"Mùi", "Ất":"Thân", "Kỷ":"Thân", "Bính":"Dậu", "Đinh":"Dậu", "Nhâm":"Mão", "Quý":"Mão", "Tân":"Dần"}
    is_tru = 3 <= DIA_CHI.index(gio_que_chi) <= 8
    chi_qn = QN_TRU[can_ngay] if is_tru else QN_DA[can_ngay]
    db_qn = [db for db, tb in thien_ban.items() if tb == chi_qn][0]
    step = 1 if DIA_CHI.index(db_qn) in [11, 0, 1, 2, 3, 4] else -1
    return {DIA_CHI[(DIA_CHI.index(db_qn) + i * step) % 12]: THIEN_TUONG_LIST[i] for i in range(12)}, is_tru

def tinh_tam_truyen_chi_tiet(can_ngay, chi_ngay, thien_ban, tu_khoa):
    k1_t, k1_d = tu_khoa[0], KY_CUNG[can_ngay]
    k2_t, k2_d = tu_khoa[1], tu_khoa[0]
    k3_t, k3_d = tu_khoa[2], chi_ngay
    k4_t, k4_d = tu_khoa[3], tu_khoa[2]
    
    tu_khoa_cung = [(k1_t, k1_d), (k2_t, k2_d), (k3_t, k3_d), (k4_t, k4_d)]
    tac_list = [uv for uv in tu_khoa_cung if la_khac(uv[1], uv[0])]
    khac_list = [uv for uv in tu_khoa_cung if la_khac(uv[0], uv[1])]
    
    so, trung, mat, ten_phap = "", "", "", ""
    cand_list = tac_list if tac_list else khac_list
    
    if cand_list:
        if len(cand_list) == 1:
            so, ten_phap = cand_list[0][0], ("Tặc Khắc (Trùng Cơ)" if tac_list else "Tặc Khắc (Nguyên Thủ)")
        else:
            ty_list = [uv for uv in cand_list if AM_DUONG[uv[0]] == AM_DUONG[can_ngay]]
            if len(ty_list) == 1:
                so, ten_phap = ty_list[0][0], "Tỷ Dụng (Tri Nhất)"
            else:
                ung_vien = ty_list if len(ty_list) > 1 else cand_list
                manh, trong = ["Dần", "Thân", "Tỵ", "Hợi"], ["Tý", "Ngọ", "Mão", "Dậu"]
                diem_uv = [(uv, 3 if uv[1] in manh else (2 if uv[1] in trong else 1)) for uv in ung_vien]
                max_diem = max([x[1] for x in diem_uv])
                so, ten_phap = [x[0] for x in diem_uv if x[1] == max_diem][0][0], "Thiệp Hại Pháp"
    else:
        so, ten_phap = (thien_ban["Dậu"] if AM_DUONG[can_ngay] == "Dương" else [db for db, tb in thien_ban.items() if tb == "Dậu"][0]), "Ngạn Sơ (Mão Tinh)"

    if not trung: trung = thien_ban[so]
    if not mat: mat = thien_ban[trung]
    return so, trung, mat, ten_phap

@app.route("/", methods=["GET", "POST"])
def index():
    tinh_ban = None
    if request.method == "POST":
        dt_str = request.form["thoi_gian_que"]
        lich_que = request.form.get("lich_que", "duong")
        dt_que = parse_input_time(dt_str, lich_que)

        thoi_gian_sinh_str = request.form.get("thoi_gian_sinh", "")
        lich_sinh = request.form.get("lich_sinh", "duong")
        gioi_tinh = request.form.get("gioi_tinh", "Nam")

        if dt_que.hour >= 23: dt_que += timedelta(days=1)
        
        can_ngay, chi_ngay = get_can_chi_ngay(dt_que)
        can_nam, chi_nam = tinh_can_chi_nam(dt_que.year)
        can_thang, chi_thang = get_thang_am_can_chi(dt_que.year, dt_que.month, can_nam)
        chi_gio = get_chi_gio(dt_que.hour)
        can_gio = get_can_gio(can_ngay, chi_gio)
        
        nguyet_tuong = get_nguyet_tuong(dt_que.month, dt_que.day)
        nguyen = get_nguyen(can_ngay, chi_ngay)
        
        thien_ban = lap_thien_ban(nguyet_tuong, chi_gio)
        thien_tuong, is_daytime = lap_12_thien_tuong(can_ngay, chi_gio, thien_ban)
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
            {"tren": k1_tren, "duoi": k1_duoi, "tuong": thien_tuong[k1_duoi], "luc_than": get_luc_than(can_ngay, k1_tren), "noi_ngoai_chien": xet_noi_ngoai_chien(thien_tuong[k1_duoi], k1_tren), "sinh_khac": get_quan_he_sinh_khac(k1_tren, k1_duoi)},
            {"tren": k2_tren, "duoi": k2_duoi, "tuong": thien_tuong[k2_duoi], "luc_than": get_luc_than(can_ngay, k2_tren), "noi_ngoai_chien": xet_noi_ngoai_chien(thien_tuong[k2_duoi], k2_tren), "sinh_khac": get_quan_he_sinh_khac(k2_tren, k2_duoi)},
            {"tren": k3_tren, "duoi": k3_duoi, "tuong": thien_tuong[k3_duoi], "luc_than": get_luc_than(can_ngay, k3_tren), "noi_ngoai_chien": xet_noi_ngoai_chien(thien_tuong[k3_duoi], k3_tren), "sinh_khac": get_quan_he_sinh_khac(k3_tren, k3_duoi)},
            {"tren": k4_tren, "duoi": k4_duoi, "tuong": thien_tuong[k4_duoi], "luc_than": get_luc_than(can_ngay, k4_tren), "noi_ngoai_chien": xet_noi_ngoai_chien(thien_tuong[k4_duoi], k4_tren), "sinh_khac": get_quan_he_sinh_khac(k4_tren, k4_duoi)}
        ]

        so, trung, mat, ten_phap = tinh_tam_truyen_chi_tiet(can_ngay, chi_ngay, thien_ban, tu_khoa)
        tam_truyen_chi_tiet = {
            "so": {"chi": so, "tuong": thien_tuong[[db for db, tb in thien_ban.items() if tb == so][0]], "luc_than": get_luc_than(can_ngay, so), "vuong_suy": tinh_vuong_suy(so, chi_thang), "noi_ngoai_chien": xet_noi_ngoai_chien(thien_tuong[[db for db, tb in thien_ban.items() if tb == so][0]], so)},
            "trung": {"chi": trung, "tuong": thien_tuong[[db for db, tb in thien_ban.items() if tb == trung][0]], "luc_than": get_luc_than(can_ngay, trung), "vuong_suy": tinh_vuong_suy(trung, chi_thang), "noi_ngoai_chien": xet_noi_ngoai_chien(thien_tuong[[db for db, tb in thien_ban.items() if tb == trung][0]], trung)},
            "mat": {"chi": mat, "tuong": thien_tuong[[db for db, tb in thien_ban.items() if tb == mat][0]], "luc_than": get_luc_than(can_ngay, mat), "vuong_suy": tinh_vuong_suy(mat, chi_thang), "noi_ngoai_chien": xet_noi_ngoai_chien(thien_tuong[[db for db, tb in thien_ban.items() if tb == mat][0]], mat)},
            "ten_phap": ten_phap
        }

        thien_dia_ban = {}
        for idx, dia in enumerate(DIA_CHI):
            thien = thien_ban[dia]
            thien_dia_ban[dia] = {
                "thien": thien,
                "ngu_hanh": NGU_HANH[thien],
                "tuong": thien_tuong[dia],
                "thai_tue": vong_thai_tue[thien],
                "loai_than": get_loai_than(chi_ngay, idx),
                "than_sat": tinh_than_sat_thien_ban(can_ngay, chi_ngay, chi_nam, thien, kv_ngay)
            }
            
        canh_bao_tat_phap = quet_tat_phap_phu(tu_khoa_chi_tiet, tam_truyen_chi_tiet, kv_ngay, can_ngay)

        sinh_than_data = None
        if thoi_gian_sinh_str:
            dt_sinh = parse_input_time(thoi_gian_sinh_str, lich_sinh)
            if dt_sinh.hour >= 23: dt_sinh += timedelta(days=1)
            c_ngay_s, c_chi_s = get_can_chi_ngay(dt_sinh)
            c_nam_s, c_chi_nam_s = tinh_can_chi_nam(dt_sinh.year)
            c_thang_s, c_chi_thang_s = get_thang_am_can_chi(dt_sinh.year, dt_sinh.month, c_nam_s)
            c_chi_gio_s = get_chi_gio(dt_sinh.hour)
            c_can_gio_s = get_can_gio(c_ngay_s, c_chi_gio_s)
            
            sinh_than_data = {
                "gioi_tinh": gioi_tinh,
                "tu_tru": {"nam": f"{c_nam_s} {c_chi_nam_s}", "thang": f"{c_thang_s} {c_chi_thang_s}", "ngay": f"{c_ngay_s} {c_chi_s}", "gio": f"{c_can_gio_s} {c_chi_gio_s}"},
                "khong_vong": {"ngay": tinh_khong_vong(c_ngay_s, c_chi_s)},
                "menh": c_chi_nam_s, "nhat_chu_can": c_ngay_s, "nhat_chu_hanh": NGU_HANH[c_ngay_s]
            }

        tinh_ban = {
            "time_str": dt_que.strftime("%d/%m/%Y %H:%M"),
            "loai_lich_que": "Âm" if lich_que == "am" else "Dương",
            "tu_tru": {"nam": f"{can_nam} {chi_nam}", "thang": f"{can_thang} {chi_thang}", "ngay": f"{can_ngay} {chi_ngay}", "gio": f"{can_gio} {chi_gio}"},
            "khong_vong": {"ngay": kv_ngay},
            "nguyet_tuong": nguyet_tuong,
            "nguyet_kien": chi_thang,
            "nguyen": nguyen,
            "can_ngay": can_ngay, "chi_ngay": chi_ngay,
            "tu_khoa": tu_khoa_chi_tiet,
            "tam_truyen": tam_truyen_chi_tiet,
            "thien_dia_ban": thien_dia_ban,
            "sinh_than": sinh_than_data,
            "canh_bao_tat_phap": canh_bao_tat_phap
        }
    return render_template("index.html", tinh_ban=tinh_ban)

if __name__ == "__main__":
    app.run(debug=True)