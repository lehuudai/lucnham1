# ==========================================
# FILE: tat_phap_phu.py
# CHỨC NĂNG: Thư viện 100 CÂU TẤT PHÁP PHÚ (Lục Nhâm Đại Toàn Quyển 3)
# TÁC GIẢ: Lăng Phúc Chi (Nam Tống) - Chuyển ngữ Thuật toán AI bởi Đại Tông Sư
# BẢN CẬP NHẬT: Tích hợp Đa Tầng Không Gian & Thời Gian (8 Trục Dữ Liệu)
# ==========================================

# KHAI BÁO CÁC DANH SÁCH & ĐỊNH LUẬT CƠ BẢN CỦA VŨ TRỤ
THIEN_CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
DIA_CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

NGU_HANH = {
    "Giáp": "Mộc", "Ất": "Mộc", "Bính": "Hỏa", "Đinh": "Hỏa", "Mậu": "Thổ", "Kỷ": "Thổ", "Canh": "Kim", "Tân": "Kim", "Nhâm": "Thủy", "Quý": "Thủy",
    "Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc", "Thìn": "Thổ", "Tỵ": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ", "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"
}

AM_DUONG = {
    "Giáp": "Dương", "Ất": "Âm", "Bính": "Dương", "Đinh": "Âm", "Mậu": "Dương", "Kỷ": "Âm", "Canh": "Dương", "Tân": "Âm", "Nhâm": "Dương", "Quý": "Âm",
    "Tý": "Dương", "Sửu": "Âm", "Dần": "Dương", "Mão": "Âm", "Thìn": "Dương", "Tỵ": "Âm", "Ngọ": "Dương", "Mùi": "Âm", "Thân": "Dương", "Dậu": "Âm", "Tuất": "Dương", "Hợi": "Âm"
}

MO_MAP = {"Mộc": "Mùi", "Hỏa": "Tuất", "Thổ": "Tuất", "Kim": "Sửu", "Thủy": "Thìn"}

def _nh(val): 
    return NGU_HANH.get(val, val)

def la_sinh(A, B): 
    return {"Mộc":"Hỏa", "Hỏa":"Thổ", "Thổ":"Kim", "Kim":"Thủy", "Thủy":"Mộc"}.get(_nh(A)) == _nh(B)

def la_khac(A, B): 
    return {"Mộc":"Thổ", "Thổ":"Thủy", "Thủy":"Hỏa", "Hỏa":"Kim", "Kim":"Mộc"}.get(_nh(A)) == _nh(B)

def is_luc_hop(A, B):
    luc_hop = [{"Tý", "Sửu"}, {"Dần", "Hợi"}, {"Mão", "Tuất"}, {"Thìn", "Dậu"}, {"Tỵ", "Thân"}, {"Ngọ", "Mùi"}]
    return {A, B} in luc_hop

def is_luc_xung(A, B):
    luc_xung = [{"Tý", "Ngọ"}, {"Sửu", "Mùi"}, {"Dần", "Thân"}, {"Mão", "Dậu"}, {"Thìn", "Tuất"}, {"Tỵ", "Hợi"}]
    return {A, B} in luc_xung

def is_luc_hai(A, B):
    luc_hai = [{"Tý", "Mùi"}, {"Sửu", "Ngọ"}, {"Dần", "Tỵ"}, {"Mão", "Thìn"}, {"Thân", "Hợi"}, {"Dậu", "Tuất"}]
    return {A, B} in luc_hai

def quet_100_tat_phap_phu(tu_khoa, tam_truyen, khong_vong_ngay, can_ngay, thien_dia_ban=None, ban_menh_data=None, vi_mo_data=None, tu_tru=None):
    """
    Hệ thống quét 100 câu Tất Pháp Phú (Tối thượng bản 100/100).
    Đã mở khóa toàn bộ các tham số đầu vào Đa tầng để phục vụ nâng cấp thuật toán Lục Nhâm về sau.
    """
    canh_bao = []
    
    # ========================================================
    # I. TRÍCH XUẤT DỮ LIỆU CỐT LÕI (GIỮ NGUYÊN HOẠT ĐỘNG 100%)
    # ========================================================
    
    # --- 1. TỨ KHÓA ---
    k1, k2, k3, k4 = tu_khoa[0], tu_khoa[1], tu_khoa[2], tu_khoa[3]
    
    k1_t, k1_d = k1["tren"], k1["duoi"]
    k1_tuong = k1.get("tuong", "")
    k1_lt = k1.get("luc_than", "")
    k1_vs = k1.get("vuong_suy", "")
    k1_ts = k1.get("truong_sinh", "")
    k1_tk = k1.get("is_tuan_khong", False)
    k1_nm = k1.get("is_nhap_mo", False)
    k1_sat = k1.get("than_sat", [])
    k1_don_can = k1.get("don_can", "Không")

    k2_t, k2_d = k2["tren"], k2["duoi"]
    k2_tuong = k2.get("tuong", "")
    k2_lt = k2.get("luc_than", "")
    k2_vs = k2.get("vuong_suy", "")
    k2_ts = k2.get("truong_sinh", "")
    k2_tk = k2.get("is_tuan_khong", False)
    k2_nm = k2.get("is_nhap_mo", False)
    k2_sat = k2.get("than_sat", [])
    k2_don_can = k2.get("don_can", "Không")

    k3_t, k3_d = k3["tren"], k3["duoi"]
    k3_tuong = k3.get("tuong", "")
    k3_lt = k3.get("luc_than", "")
    k3_vs = k3.get("vuong_suy", "")
    k3_ts = k3.get("truong_sinh", "")
    k3_tk = k3.get("is_tuan_khong", False)
    k3_nm = k3.get("is_nhap_mo", False)
    k3_sat = k3.get("than_sat", [])
    k3_don_can = k3.get("don_can", "Không")

    k4_t, k4_d = k4["tren"], k4["duoi"]
    k4_tuong = k4.get("tuong", "")
    k4_lt = k4.get("luc_than", "")
    k4_vs = k4.get("vuong_suy", "")
    k4_ts = k4.get("truong_sinh", "")
    k4_tk = k4.get("is_tuan_khong", False)
    k4_nm = k4.get("is_nhap_mo", False)
    k4_sat = k4.get("than_sat", [])
    k4_don_can = k4.get("don_can", "Không")

    chi_ngay = k3_d

    # --- 2. TAM TRUYỀN ---
    t_so = tam_truyen["so"]
    so_chi = t_so["chi"]
    tuong_so = t_so.get("tuong", "")
    lt_so = t_so.get("luc_than", "")
    vs_so = t_so.get("vuong_suy", "")
    ts_so = t_so.get("truong_sinh", "")
    tk_so = t_so.get("is_tuan_khong", False)
    nm_so = t_so.get("is_nhap_mo", False)
    sat_so = t_so.get("than_sat", [])
    am_than_so = t_so.get("am_than", "")
    don_can_so = t_so.get("don_can", "Không")

    t_trung = tam_truyen["trung"]
    trung_chi = t_trung["chi"]
    tuong_trung = t_trung.get("tuong", "")
    lt_trung = t_trung.get("luc_than", "")
    vs_trung = t_trung.get("vuong_suy", "")
    ts_trung = t_trung.get("truong_sinh", "")
    tk_trung = t_trung.get("is_tuan_khong", False)
    nm_trung = t_trung.get("is_nhap_mo", False)
    sat_trung = t_trung.get("than_sat", [])
    am_than_trung = t_trung.get("am_than", "")
    don_can_trung = t_trung.get("don_can", "Không")

    t_mat = tam_truyen["mat"]
    mat_chi = t_mat["chi"]
    tuong_mat = t_mat.get("tuong", "")
    lt_mat = t_mat.get("luc_than", "")
    vs_mat = t_mat.get("vuong_suy", "")
    ts_mat = t_mat.get("truong_sinh", "")
    tk_mat = t_mat.get("is_tuan_khong", False)
    nm_mat = t_mat.get("is_nhap_mo", False)
    sat_mat = t_mat.get("than_sat", [])
    am_than_mat = t_mat.get("am_than", "")
    don_can_mat = t_mat.get("don_can", "Không")

    # Danh sách tổng hợp để check cục diện
    tat_ca_am_duong = [AM_DUONG.get(c) for c in [k1_t, k2_t, k3_t, k4_t, so_chi, trung_chi, mat_chi] if AM_DUONG.get(c)]
    tat_ca_tuong = [k1_tuong, k2_tuong, k3_tuong, k4_tuong, tuong_so, tuong_trung, tuong_mat]

    # ========================================================
    # II. TRÍCH XUẤT DỮ LIỆU ĐA TẦNG (CHUẨN BỊ CHO NÂNG CẤP)
    # ========================================================
    
    # 1. Tứ Trụ
    chi_nam = tu_tru["nam"].split()[1] if tu_tru else ""
    chi_thang = tu_tru["thang"].split()[1] if tu_tru else ""
    chi_gio = tu_tru["gio"].split()[1] if tu_tru else ""

    # 2. Bản Mệnh & Hành Niên
    menh_chi = ban_menh_data.get("menh", "") if ban_menh_data else ""
    hanh_nien_chi = ban_menh_data.get("hanh_nien", "") if ban_menh_data else ""

    # Lưu ý: Các biến mới trích xuất ở đây chưa trực tiếp tham gia vào 100 câu TPP cổ điển. 
    # Nhưng đã sẵn sàng cho việc bạn tự thêm các định lý luận giải nâng cao vào cuối hàm này.

    # ========================================================
    # NHÓM 1: QUY LUẬT TIẾN THOÁI & QUAN LỘC (Câu 1 - 10)
    # Lấy trọn vẹn lý thuyết gốc Lục Nhâm Đại Toàn Quyển 3
    # ========================================================
    
    # CÂU 1: Tiền hậu dẫn tùng thăng thiên cát
    # Lý thuyết: Tam truyền tương sinh tuần tự (Sơ sinh Trung, Trung sinh Mạt) VÀ có sự liên kết tương sinh với Can ngày (Can sinh Sơ hoặc Mạt sinh Can), không rớt Tuần Không.
    truyen_sinh_nhau = la_sinh(so_chi, trung_chi) and la_sinh(trung_chi, mat_chi)
    mat_sinh_can = la_sinh(mat_chi, can_ngay)
    can_sinh_so = la_sinh(can_ngay, so_chi)
    if truyen_sinh_nhau and (mat_sinh_can or can_sinh_so) and not (tk_so or tk_trung or tk_mat):
        canh_bao.append("✅ CÂU 1 (Tiền hậu dẫn tùng thăng thiên cát): Tam truyền liên tục sinh nhau và có tình ý tương sinh với Can ngày. Vạn sự hanh thông, công danh thăng tiến rực rỡ, được người đi trước kẻ đi sau nâng đỡ dìu dắt.")

    # CÂU 2: Thủ vĩ tương kiến thủy chung nghi
    # Lý thuyết: Sơ truyền và Mạt truyền gặp lại nhau (Trùng nhau - Hồi Hoàn Cục) hoặc đối đầu nhau (Tương Xung - Phản Ngâm Cục).
    if so_chi == mat_chi:
        canh_bao.append("⚠️ CÂU 2 (Thủ vĩ tương kiến thủy chung nghi): Sơ truyền và Mạt truyền trùng nhau (Hồi Hoàn cục). Sự việc dây dưa quanh quẩn, đi một vòng rồi lại trở về vạch xuất phát, lặp lại không dứt.")
    elif is_luc_xung(so_chi, mat_chi):
        canh_bao.append("⚠️ CÂU 2 (Thủ vĩ tương kiến thủy chung nghi): Sơ truyền và Mạt truyền tương xung nhau (Phản Ngâm cục). Sự việc có biến động mạnh, phản phúc, trước sau bất nhất, có sự đổi trắng thay đen phút chót.")

    # CÂU 3: Liêm mạc Quý nhân cao giáp đệ
    # Lý thuyết: Quý Nhân giáng trực tiếp tại Thượng Thần Can Ngày (Khóa 1) hoặc Thượng Thần Chi Ngày (Khóa 3), điều kiện là Không bị Khắc từ dưới lên, và Không bị Tuần Không.
    if k1_tuong == "Quý Nhân" and not k1_tk and not la_khac(k1_d, k1_t):
        canh_bao.append("✅ CÂU 3 (Liêm mạc Quý nhân cao giáp đệ): Quý Nhân giáng trực tiếp lên bản mệnh (Khóa 1), không bị Không Vong hay nội chiến. Đại cát cho công danh, thi cử đỗ đạt, được sếp lớn đặc biệt che chở.")
    elif k3_tuong == "Quý Nhân" and not k3_tk and not la_khac(k3_d, k3_t):
        canh_bao.append("✅ CÂU 3 (Liêm mạc Quý nhân cao giáp đệ): Quý Nhân giáng thẳng vào cửa nhà/cơ quan (Khóa 3). Quý nhân chủ động ghé thăm, gia đạo bình an, kinh doanh được đối tác lớn chống lưng.")

    # CÂU 4: Thôi quan sứ giả phó quan kỳ
    # Lý thuyết: Quan Quỷ cõng Thiên Mã, hoặc Sơ truyền cõng Lộc/Mã/Thái Tuế. Lệnh hành chính đi thần tốc.
    if lt_so == "Quan Quỷ" and ("Thiên Mã" in sat_so or "Thái Tuế" in sat_so or "Nguyệt Kiến" in sat_so):
        canh_bao.append("✅ CÂU 4 (Thôi quan sứ giả phó quan kỳ): Lệnh bài Quan Quỷ cõng Thiên Mã / Thái Tuế tại Sơ truyền. Tốc tốc cử hành! Lệnh thăng chức, điều động công tác hoặc giấy tờ hành chính sẽ giáng xuống ngay lập tức thần tốc.")

    # CÂU 5 & 6: Lục Dương & Lục Âm
    # Lý thuyết: Cả 4 Khóa (Can, Chi, Âm Can, Âm Chi) và 3 Truyền (Sơ, Trung, Mạt) toàn bộ là Dương hoặc toàn bộ là Âm. 
    if len(tat_ca_am_duong) == 7 and all(x == "Dương" for x in tat_ca_am_duong):
        canh_bao.append("✅ CÂU 5 (Lục dương số túc tu công dụng): Quẻ thuần Dương (Tứ Khóa, Tam Truyền gồm 7 chi đều Dương). Mọi việc quang minh chính đại, không giấu giếm, thích hợp làm việc công khai minh bạch sẽ thuận lợi.")
    if len(tat_ca_am_duong) == 7 and all(x == "Âm" for x in tat_ca_am_duong):
        canh_bao.append("⚠️ CÂU 6 (Lục âm tương kế tận hôn mê): Quẻ thuần Âm (Tứ Khóa, Tam Truyền gồm 7 chi đều Âm). Mọi việc mờ ám, u uất, thiếu minh bạch. Có kẻ gian giật dây, cẩn thận bị lừa gạt đâm sau lưng trong bóng tối.")

    # CÂU 7: Vượng lộc lâm thân đồ vọng tác
    # Lý thuyết: Lộc của Can Ngày giáng Thượng thần Can Ngày (Lâm Thân), nhưng Khí quá Vượng (Vật cực tất phản), dễ sinh tự cao tự đại, khinh suất làm liều dẫn đến tai họa.
    if "Thiên Lộc" in k1_sat:
        if k1_vs in ["VƯỢNG (100%)", "TƯỚNG (80%)"] or k1_tk:
            canh_bao.append("⚠️ CÂU 7 (Vượng lộc lâm thân đồ vọng tác): Thiên Lộc lâm thân (Khóa 1). Khí thế bản thân đang cực kỳ Vượng. Nhưng 'Vật cực tất phản', dễ sinh tâm kiêu ngạo, bốc đồng làm liều vượt quá giới hạn sẽ tự chuốc lấy thất bại vỡ lở.")

    # CÂU 8: Quyền nhiếp bất chính lộc lâm chi
    # Lý thuyết: Lộc của Can Ngày đáng ra phải ở phe Can, nay lại giáng xuống Thượng thần Địa Chi (Khóa 3). Lộc Vua vào tay Khách.
    if "Thiên Lộc" in k3_sat:
        canh_bao.append("⚠️ CÂU 8 (Quyền nhiếp bất chính lộc lâm chi): Thiên Lộc của Bản mệnh lại giáng xuống cung Địa chi/Khách (Khóa 3). Lợi ích rơi vào tay người khác, kẻ dưới lấn quyền, bản thân ngồi ghế hư danh không có thực quyền.")

    # CÂU 9: Tị nạn đào sinh tu khí cựu
    # Lý thuyết: Khởi đầu bằng Hung hãn (Sơ truyền Quan Quỷ) hoặc Sơ Không Vong, nhưng Mạt truyền lại gỡ gạc bằng Trường Sinh hoặc Sinh lại cho Can Ngày.
    if (lt_so == "Quan Quỷ" or tk_so) and (ts_mat == "Trường Sinh" or la_sinh(mat_chi, can_ngay)):
        canh_bao.append("✅ CÂU 9 (Tị nạn đào sinh tu khí cựu): Sơ truyền là Tai Họa / Không Vong mang tới bế tắc, nhưng Mạt truyền lại là Trường Sinh / Sinh Can cứu mạng. Quẻ báo: Phải dứt bỏ cái cũ nát, tìm phương thức mới thì cuối con đường ắt có sinh lộ rực rỡ.")

    # CÂU 10: Hủ mộc nan điêu biệt tác vi
    # Lý thuyết: Can Chi (Khóa 1 & 3) Không Vong, Sơ Mạt cũng Không Vong. Vạn sự thoái bại, nền tảng rỗng tuếch.
    if k1_tk and k3_tk and tk_so and tk_trung:
        canh_bao.append("⚠️ CÂU 10 (Hủ mộc nan điêu biệt tác vi): Gỗ mục nan điêu! Cả Ta (Khóa 1), Khách (Khóa 3) và Diễn biến (Sơ/Trung) đều chìm trong hố Không Vong. Sự việc rỗng tuếch từ gốc đến ngọn, tuyệt đối đừng tốn công cố chấp, buông bỏ làm việc khác ngay.")

   # ========================================================
    # NHÓM 2: TƯƠNG TÁC QUỶ TÀI & TUẦN KHÔNG (Câu 11 - 20)
    # Lấy trọn vẹn lý thuyết gốc Lục Nhâm Đại Toàn Quyển 3
    # ========================================================

    # CÂU 11: Chúng quỷ tuy chương toàn bất úy
    # Lý thuyết: Sơ truyền và Trung truyền đều là Quan Quỷ (hoặc Tứ Khóa có Quỷ phát dụng), ác sát bủa vây.
    # Nhưng Mạt truyền là Tử Tôn (Cứu thần / Giải thần) tột đỉnh và KHÔNG bị Tuần Không.
    if (lt_so == "Quan Quỷ" or lt_trung == "Quan Quỷ") and lt_mat == "Tử Tôn" and not tk_mat:
        canh_bao.append("✅ CÂU 11 (Chúng quỷ tuy chương toàn bất úy): Tai họa (Quan Quỷ) nổi lên hung hãn ở Sơ/Trung truyền, nhưng Mạt truyền lại là Tử Tôn (Thần cứu giải) khắc ngược lại Quỷ. Trong họa có phúc, dù nguy hiểm đến mấy thì phút 89 vẫn có cao nhân/lối thoát hóa hiểm thành an.")

    # CÂU 12: Tuy ưu hồ giả hổ uy nghi
    # Lý thuyết: Tướng của Sơ truyền là Bạch Hổ hoặc Đằng Xà (Ác thần), dọa dẫm kinh hoàng. Nhưng bản thân Sơ truyền bị rớt Tuần Không.
    if (tuong_so == "Bạch Hổ" or tuong_so == "Đằng Xà") and tk_so:
        # Xét thêm Vượng Suy để luận Giả Không (đợi ngày nổ) hay Tuyệt Không (chết hẳn)
        if "VƯỢNG" in vs_so or "TƯỚNG" in vs_so:
            canh_bao.append("⚠️ CÂU 12 (Tuy ưu hồ giả hổ uy nghi): Ác thần (Hổ/Xà) ngự Sơ truyền nhưng rớt Tuần Không (Giả Không vì Khí Vượng). Đối thủ 'Cáo mượn oai hùm' dọa dẫm bề ngoài, hiện tại chưa hại được ta, nhưng tuyệt đối không chủ quan vì ngày Xung Không nó sẽ cắn càn.")
        else:
            canh_bao.append("✅ CÂU 12 (Tuy ưu hồ giả hổ uy nghi): Ác thần (Hổ/Xà) ngự Sơ truyền rớt TUYỆT KHÔNG (Khí Hưu/Tù/Tử). Hoàn toàn là báo động giả, đối phương rỗng tuếch, dọa dẫm không có thực lực, đừng hoảng sợ vô ích.")

    # CÂU 13: Quỷ tặc đương thời vô úy kỵ
    # Lý thuyết: Lục Thần của Sơ truyền là Quan Quỷ, rớt vào Tuần Không, hoặc bị Thiên/Địa bàn (Mẫu) xung khắc triệt tiêu (Tử/Mộ/Tuyệt).
    if lt_so == "Quan Quỷ":
        if tk_so:
            canh_bao.append("✅ CÂU 13 (Quỷ tặc đương thời vô úy kỵ): Tai họa / Kẻ tiểu nhân (Quan Quỷ) rớt vào Tuần Không. Lực sát thương bằng 0, sấm to mưa nhỏ, chuyện lớn hóa nhỏ, chuyện nhỏ hóa không.")
        elif la_khac(tuong_so, so_chi) or ts_so in ["Tử", "Mộ", "Tuyệt"]: # Bị Tướng khắc (Nội chiến) hoặc rớt đất Tử/Mộ
            canh_bao.append("✅ CÂU 13 (Quỷ tặc đương thời vô úy kỵ): Quan Quỷ (Tai họa) vướng cảnh Nội Chiến (bị Tướng đè) hoặc rớt vào hố Tử/Mộ/Tuyệt. Hung tinh tự diệt, địch thủ tự có lục đục nội bộ mà tan rã, ta ngồi không đắc lợi.")

    # CÂU 14: Truyền tài thái vượng phản tài khuy
    # Lý thuyết: Tam truyền toàn là Thê Tài (Sơ, Trung, Mạt đều là Tài, hoặc hợp thành Tam Hợp Tài cục). Tài đa ép Thân, Can suy không gánh nổi.
    tam_truyen_cuc_dien = tam_truyen.get("cuc_dien", [])
    is_tai_cuc = ("Tam Hợp Cục" in tam_truyen_cuc_dien and lt_so == "Thê Tài")
    if (lt_so == "Thê Tài" and lt_trung == "Thê Tài" and lt_mat == "Thê Tài") or is_tai_cuc:
        canh_bao.append("⚠️ CÂU 14 (Truyền tài thái vượng phản tài khuy): Tam truyền toàn là Tiền bạc / Tài Cục. Tài quá vượng hóa Sát! Cực kỳ cẩn thận: Tiền nhiều nhưng bản mệnh gánh không nổi sinh ra tai họa (vì tiền mà đứt gánh, lừa đảo, phá sản, hoặc vì tửu sắc mà thân bại danh liệt).")

    # CÂU 15: Thoát thượng phùng thoát phòng hư trá
    # Lý thuyết: Tứ khóa liên tục sinh xuất (Can sinh K1, K1 sinh K2...), hoặc Tam truyền toàn Tử Tôn (Tiết khí). Bị rút ruột tột độ.
    rut_ruot_k1 = la_sinh(k1_d, k1_t) and la_sinh(k1_t, k2_t)
    rut_ruot_k3 = la_sinh(k3_d, k3_t) and la_sinh(k3_t, k4_t)
    toan_tu_ton = (lt_so == "Tử Tôn" and lt_trung == "Tử Tôn" and lt_mat == "Tử Tôn")
    if rut_ruot_k1 or rut_ruot_k3 or toan_tu_ton:
        canh_bao.append("⚠️ CÂU 15 (Thoát thượng phùng thoát phòng hư trá): Toàn cục Sinh xuất (Thoát khí / Tử Tôn thái quá). Năng lượng bản thân / nguồn vốn đang bị bòn rút kiệt quệ. Đề phòng bị lừa đảo tinh vi (bánh vẽ), đầu tư làm nhiều nhưng kẻ khác hưởng trọn, hao tâm tổn trí vô ích.")

    # CÂU 16: Không thượng thừa không sự mạc truy
    # Lý thuyết: Sơ truyền rớt Không Vong, Mạt truyền cũng rớt Không Vong.
    if tk_so and tk_mat:
        canh_bao.append("⚠️ CÂU 16 (Không thượng thừa không sự mạc truy): Sơ Không, Mạt Không. Cả Khởi đầu và Kết thúc đều là hố đen rỗng tuếch. Sự việc này là ảo vọng, không có thực tế, hãy buông bỏ ngay đừng tốn công theo đuổi (Sự mạc truy).")

    # CÂU 17: Tiến như không vong nghi thoái bộ
    # Lý thuyết: Sơ truyền Không Vong, nhưng Cục diện đang là "TRUYỀN TIẾN" (Sơ -> Trung -> Mạt tiến lên). Phía trước là hố sâu!
    tien_thoai = tam_truyen.get("tien_thoai", "")
    if tk_so and "TRUYỀN TIẾN" in tien_thoai:
        canh_bao.append("⚠️ CÂU 17 (Tiến như không vong nghi thoái bộ): Sơ truyền Không Vong, nhưng Tam truyền lại đang bước Tiến. Đi tới là đâm đầu vào hố Không Vong! Tuyệt đối không được mở rộng quy mô hay làm liều, hãy lùi lại phòng thủ ngay lập tức.")

    # CÂU 18: Đạp cước không vong tiến dụng nghi
    # Lý thuyết: Sơ truyền Không Vong, nhưng Cục diện đang là "TRUYỀN THOÁI" (Lùi lại). Bước hụt để tạo đà.
    if tk_so and "TRUYỀN THOÁI" in tien_thoai:
        canh_bao.append("✅ CÂU 18 (Đạp cước không vong tiến dụng nghi): Sơ Không Vong, Tam truyền bước Lùi (Truyền Thoái). Bước hụt ban đầu giúp ta lùi lại tĩnh tâm lấy đà, tránh được hố sâu. Khởi đầu gian nan, nhưng nhờ thoái lui nhìn nhận lại, càng về sau càng vững chắc thành công.")

    # CÂU 19: Thai tài sinh khí thê hoài dựng
    # Lý thuyết: Sơ truyền là Thê Tài, Ngũ hành của Sơ lại Sinh cho Can Ngày. Hoặc mang cát thần (Thiên Hậu, Lục Hợp).
    if lt_so == "Thê Tài" and (la_sinh(so_chi, can_ngay) or tuong_so in ["Thiên Hậu", "Lục Hợp"]):
        canh_bao.append("✅ CÂU 19 (Thai tài sinh khí thê hoài dựng): Sơ truyền Thê Tài mang Tương Sinh / Cát Thần giáng Bản Mệnh. Điềm báo Đại Hỷ! Gia đạo êm ấm, vợ có thai, sinh đẻ bình an, hoặc một khối tài sản khổng lồ đang âm thầm nhen nhóm chờ ngày thu hoạch.")

    # CÂU 20: Thai tài tử khí tổn thai thôi
    # Lý thuyết: Sơ truyền là Thê Tài, nhưng bị Can Ngày Khắc (Tử Khí), hoặc mang Ác thần (Bạch Hổ / Đằng Xà), hoặc rớt Không Vong.
    if lt_so == "Thê Tài" and (la_khac(can_ngay, so_chi) or tuong_so in ["Bạch Hổ", "Đằng Xà"] or tk_so):
        canh_bao.append("⚠️ CÂU 20 (Thai tài tử khí tổn thai thôi): Sơ truyền Thê Tài nhưng mang Tử Khí / Ác Thần / Không Vong. Điềm hung hại! Cảnh báo sẩy thai, thai lưu với nữ giới. Với kinh doanh: Mối làm ăn/tiền bạc vừa nhen nhóm đã bị triệt tiêu từ trong trứng nước, vốn liếng bốc hơi.")

   # ========================================================
    # NHÓM 3: ĐỘNG LỰC HỌC CHỦ KHÁCH & GIAO XA (Câu 21 - 30)
    # Lấy trọn vẹn lý thuyết gốc Lục Nhâm Đại Toàn Quyển 3
    # ========================================================

    # CÂU 21: Giao xa tương hợp giao quan lợi
    # Lý thuyết: Thượng thần Can (K1) Hợp với Âm thần Chi (K4), và Thượng thần Chi (K3) Hợp với Âm thần Can (K2). Hoặc K1 hợp K3 chéo góc. Ta gọi là Giao Xa Lục Hợp.
    if is_luc_hop(k1_t, k4_t) and is_luc_hop(k2_t, k3_t):
        canh_bao.append("✅ CÂU 21 (Giao xa tương hợp giao quan lợi): Tứ khóa đan chéo Lục Hợp hoàn hảo (Giao xa tương hợp). Chủ Khách đồng tâm hiệp lực, âm thầm bảo vệ hậu phương cho nhau. Rất đại cát cho việc đàm phán, kết hôn, hợp tác kinh doanh Win-Win.")

    # CÂU 22: Thượng hạ giai hợp lưỡng tâm tề
    # Lý thuyết: Can và Thượng thần Can Hợp nhau (K1 trên dưới hợp). Chi và Thượng thần Chi Hợp nhau (K3 trên dưới hợp).
    if is_luc_hop(k1_t, k1_d) and is_luc_hop(k3_t, k3_d):
        canh_bao.append("✅ CÂU 22 (Thượng hạ giai hợp lưỡng tâm tề): Trên dưới Lục Hợp. Nền tảng Ta (Can) êm ấm, nền tảng Khách/Công việc (Chi) cũng thuận hòa. Cục diện đoàn kết nội bộ vững chắc, đồng cam cộng khổ, việc gì cũng thành.")

    # CÂU 23: Bỉ cầu ngã sự chi truyền can
    # Lý thuyết: Mũi tên đi từ Chi (Khách) sang Can (Ta). Tức là Sơ truyền phát động từ Thượng thần Chi (K3), và Mạt truyền kết thúc tại Thượng thần Can (K1).
    if k3_t == so_chi and k1_t == mat_chi:
        canh_bao.append("🎯 CÂU 23 (Bỉ cầu ngã sự chi truyền can): Mũi tên bay từ Chi sang Can. Đối phương (Khách/Đối tác) đang rất cần Ta, chủ động đến tìm nhờ vả hoặc dâng cơ hội. Ta đang nắm đằng chuôi, ở thế thượng phong, cứ ép giá và đặt điều kiện!")

    # CÂU 24: Ngã cầu bỉ sự can truyền chi
    # Lý thuyết: Mũi tên đi từ Can (Ta) sang Chi (Khách). Tức là Sơ truyền phát động từ Thượng thần Can (K1), kết thúc tại Thượng thần Chi (K3).
    if k1_t == so_chi and k3_t == mat_chi:
        canh_bao.append("🎯 CÂU 24 (Ngã cầu bỉ sự can truyền chi): Mũi tên bay từ Can sang Chi. Ta đang chủ động chạy đi tìm Khách để nhờ vả, xin việc, gọi vốn. Ta đang ở thế cửa dưới, phải nhẫn nhịn, khéo léo và lụy người ta thì mới xong việc.")

    # CÂU 25: Kim nhật phùng Đinh hung họa động
    # Lý thuyết: Ngày hành Kim (Canh, Tân), Độn can của Sơ truyền là Đinh (Hỏa). Đinh Hỏa nung chảy Kim bản mệnh. Lửa cháy ngầm.
    if NGU_HANH.get(can_ngay) == "Kim" and don_can_so == "Đinh" and not tk_so:
        canh_bao.append("⚠️ CÂU 25 (Kim nhật phùng Đinh hung họa động): Ngày hành Kim gặp Độn Can Sơ truyền là Đinh. Lửa nung chảy sắt! Điềm báo có tai họa, đổ máu, hỏa hoạn hoặc mâu thuẫn bạo phát bất ngờ thần tốc. Tuyệt đối cẩn thận đi lại, tranh chấp.")

    # CÂU 26: Thủy nhật phùng Đinh tài động chi
    # Lý thuyết: Ngày hành Thủy (Nhâm, Quý), Độn can của Sơ truyền là Đinh (Hỏa). Thủy khắc Hỏa làm Tài (Tiền bạc). Tài lộc động.
    if NGU_HANH.get(can_ngay) == "Thủy" and don_can_so == "Đinh" and not tk_so:
        canh_bao.append("✅ CÂU 26 (Thủy nhật phùng Đinh tài động chi): Ngày hành Thủy gặp Độn Can Sơ truyền là Đinh (Tài). Động lực kiếm tiền bùng nổ, sẽ có luồng tiền bất ngờ xuất hiện, hoặc cơ hội chốt sale thần tốc mang lại lợi nhuận cao.")

    # CÂU 27: Truyền tài hóa quỷ tài hưu mịch
    # Lý thuyết: Sơ truyền là Thê Tài (Tiền bạc/Tình ái), nhưng Mạt truyền lại biến thành Quan Quỷ (Tai họa/Hình ngục).
    if lt_so == "Thê Tài" and lt_mat == "Quan Quỷ":
        canh_bao.append("⚠️ CÂU 27 (Truyền tài hóa quỷ tài hưu mịch): Bắt đầu bằng Tiền/Sắc, kết thúc bằng Tai Họa. Quẻ báo bẫy lừa đảo kinh tế. Chớ tham lam, thấy lợi nhỏ trước mắt mà lao vào vì đích đến cuối cùng là phá sản hoặc tù tội!")

    # CÂU 28: Truyền quỷ hóa tài tài hiểm nguy
    # Lý thuyết: Sơ truyền là Quan Quỷ (Gian nan/Nguy hiểm), nhưng Mạt truyền lại biến thành Thê Tài (Lợi nhuận).
    if lt_so == "Quan Quỷ" and lt_mat == "Thê Tài":
        canh_bao.append("✅ CÂU 28 (Truyền quỷ hóa tài tài hiểm nguy): Bắt đầu bằng bĩ cực gian nan, nhưng kết thúc lại thu được lợi nhuận khổng lồ. Khổ tận cam lai. Dự án này rủi ro cực cao, nhưng nếu dám đánh đổi và vượt qua, lợi nhuận sẽ vô cùng rực rỡ.")

    # CÂU 29: Quyến thuộc phong doanh cư hiệp trạch
    # Lý thuyết: Khóa Can (Ta) vượng khí (Tương sinh), nhưng Khóa Chi (Nhà cửa/Cơ sở) lại rớt vào Không Vong hoặc Suy Tuyệt.
    can_vuong = la_sinh(k1_d, k1_t) or la_sinh(k1_t, k1_d)
    if can_vuong and k3_tk:
        canh_bao.append("⚠️ CÂU 29 (Quyến thuộc phong doanh cư hiệp trạch): Chủ Vượng nhưng Khách (Nhà cửa/Cơ sở) lại Không Vong. Nhà hẹp người đông, nền tảng cơ sở vật chất (vốn, mặt bằng) không theo kịp tham vọng và nguồn nhân lực. Bị kìm hãm không bành trướng được.")

    # CÂU 30: Ốc trạch khoan quảng trí nhân suy
    # Lý thuyết: Khóa Chi (Nhà cửa/Dự án) vượng khí (Tương sinh), nhưng Khóa Can (Ta/Nhân sự) lại rớt vào Không Vong.
    chi_vuong = la_sinh(k3_t, k3_d) or la_sinh(k3_d, k3_t)
    if k1_tk and chi_vuong:
        canh_bao.append("⚠️ CÂU 30 (Ốc trạch khoan quảng trí nhân suy): Chủ Không Vong nhưng Khách (Nhà cửa/Dự án) quá Vượng. Nhà rộng người thưa. Nguồn lực phân tán, nhân sự mỏng nhưng quy mô vận hành quá lớn, dẫn đến hao tốn tài sản để gánh vác cơ ngơi quá sức.")

    # ========================================================
    # NHÓM 4: THẾ TRẬN SINH KHẮC VÀ ĐẢO LỘN (Câu 31 - 40)
    # Lấy trọn vẹn lý thuyết gốc Lục Nhâm Đại Toàn Quyển 3
    # ========================================================

    # CÂU 31: Tam truyền đệ sinh nhân cử tiến
    # Lý thuyết: Tam truyền tương sinh liên hoàn. Gồm 2 cục: Sơ sinh Trung, Trung sinh Mạt (Tiến) HOẶC Mạt sinh Trung, Trung sinh Sơ (Thoái).
    de_sinh_tien = la_sinh(so_chi, trung_chi) and la_sinh(trung_chi, mat_chi)
    de_sinh_thoai = la_sinh(mat_chi, trung_chi) and la_sinh(trung_chi, so_chi)
    if de_sinh_tien or de_sinh_thoai:
        canh_bao.append("✅ CÂU 31 (Tam truyền đệ sinh nhân cử tiến): Khí tuần hoàn tương sinh liên tục. Nếu đi từ Sơ đến Mạt là có quý nhân nâng bước tiến lên. Nếu đi từ Mạt ngược về Sơ là có người hậu thuẫn từ phía sau. Đại cát cho thi cử, thăng quan, phát triển mạng lưới.")

    # CÂU 32: Tam truyền hỗ khắc chúng nhân khi
    # Lý thuyết: Tam truyền khắc nhau liên hoàn (Sơ khắc Trung, Trung khắc Mạt hoặc ngược lại). Khí bị cản trở, đứt gãy.
    ho_khac_tien = la_khac(so_chi, trung_chi) and la_khac(trung_chi, mat_chi)
    ho_khac_thoai = la_khac(mat_chi, trung_chi) and la_khac(trung_chi, so_chi)
    if ho_khac_tien or ho_khac_thoai:
        canh_bao.append("⚠️ CÂU 32 (Tam truyền hỗ khắc chúng nhân khi): Tam truyền tự cắn xé nhau liên hoàn. Môi trường độc hại, đi đâu cũng bị chèn ép, vùi dập. Nội bộ công ty đâm sau lưng, đối tác thì lật lọng, vạn sự bất thành.")

    # CÂU 33: Hữu thủy vô chung nan biến dịch
    # Lý thuyết: Sơ truyền vượng tướng/có khí, nhưng Mạt truyền lại rớt Không Vong hoặc đất Tử/Tuyệt.
    if (not tk_so) and (tk_mat or ts_mat in ["Tử", "Tuyệt", "Bại"]):
        canh_bao.append("⚠️ CÂU 33 (Hữu thủy vô chung nan biến dịch): Có mở đầu rầm rộ nhưng kết thúc lại rơi vào Không Vong hoặc Tử/Tuyệt. Bệnh 'Đầu voi đuôi chuột', dự án khai trương hoành tráng nhưng âm thầm lụi tàn, gãy gánh giữa đường.")

    # CÂU 34: Khổ khứ cam lai lạc lý bi
    # Lý thuyết: Gồm 2 vế. 
    # Vế 1 (Khổ khứ cam lai): Sơ là Quỷ (Hung), Mạt là Sinh/Phụ Mẫu/Tử Tôn (Cát).
    # Vế 2 (Lạc lý bi): Sơ là Sinh/Tài (Cát), Mạt là Quỷ (Hung).
    if lt_so == "Quan Quỷ" and lt_mat in ["Phụ Mẫu", "Tử Tôn"]:
        canh_bao.append("✅ CÂU 34 (Khổ khứ cam lai - Đầu đắng đuôi ngọt): Khởi đầu là Tai họa/Áp lực (Sơ Quỷ), nhưng kết thúc lại được Sinh phò/Cứu giải (Mạt Phụ Mẫu/Tử Tôn). Gian nan chỉ là thử thách ban đầu, hậu vận cực kỳ êm ấm vinh quang.")
    elif lt_so in ["Phụ Mẫu", "Thê Tài"] and lt_mat == "Quan Quỷ":
        canh_bao.append("⚠️ CÂU 34 (Lạc lý bi - Trong vui có buồn): Khởi đầu thuận lợi, dễ kiếm tiền hoặc được o bế (Sơ Tài/Sinh), nhưng kết cục lại vướng vào Tai họa/Pháp luật (Mạt Quỷ). Tuyệt đối cẩn thận bẫy 'Mật ngọt chết ruồi'.")

    # CÂU 35: Nhân trạch thụ thoát câu chiêu đạo
    # Lý thuyết: Khóa 1 (Can/Người) sinh xuất cho Khóa 2. Khóa 3 (Chi/Nhà) sinh xuất cho Khóa 4. Cả Chủ và Khách đều bị 'Thoát khí' (Tiết rò rỉ).
    if la_sinh(k1_d, k1_t) and la_sinh(k3_d, k3_t):
        canh_bao.append("⚠️ CÂU 35 (Nhân trạch thụ thoát câu chiêu đạo): Cả Ta (Nhân) và Khách/Nhà cửa (Trạch) đều bị Thoát khí (Sinh xuất). Cực kỳ hao tốn! Năng lượng, tiền tài, sức khỏe rò rỉ mỗi ngày một ít. Cẩn thận mất trộm, hoặc ốm đau tốn tiền thuốc men dai dẳng.")

    # CÂU 36: Can chi giai bại thế khuynh đồi
    # Lý thuyết: Can và Chi cùng rớt Không Vong, VÀ đồng thời lâm vào đất Tử/Tuyệt/Bại (vòng Trường Sinh) hoặc Xung nhau.
    if k1_tk and k3_tk and (is_luc_xung(k1_t, k3_t) or k1_ts in ["Tử", "Tuyệt", "Bại"] or k3_ts in ["Tử", "Tuyệt", "Bại"]):
        canh_bao.append("⚠️ CÂU 36 (Can chi giai bại thế khuynh đồi): Tứ Khóa Can Chi đều rớt Tuần Không, lại nằm trên đất Tuyệt/Bại. Thế trận nghiêng đổ, không thể cứu vãn. Doanh nghiệp nguy cơ phá sản, gia đạo sụp đổ ly tán, vạn sự vô phương cứu chữa.")

    # CÂU 37: Mạt trợ sơ hề tam đẳng luận
    # Lý thuyết: Mạt truyền quay ngược lại Sinh cho Sơ truyền, hoặc Mạt và Sơ Lục Hợp/Bán Hợp nhau. Khí quay vòng tuần hoàn.
    if la_sinh(mat_chi, so_chi) or is_luc_hop(mat_chi, so_chi):
        canh_bao.append("💡 CÂU 37 (Mạt trợ sơ hề tam đẳng luận): Kết thúc lại quay lại Sinh trợ hoặc Hợp với Khởi đầu. Sự việc mang tính chất quay vòng tuần hoàn, quả thu được lại đem gieo làm nhân (Tái đầu tư sinh lời liên tục). Cũ không đi, mới không đến.")

    # CÂU 38: Bế khẩu quái thể lưỡng ban thôi
    # Lý thuyết: Quẻ 'Bế Khẩu'. Xảy ra khi: Tuần Không giáng vào Chu Tước (Lời nói/Giấy tờ), HOẶC Sơ truyền là Phụ Mẫu (Giấy tờ/Văn bản) rớt Không Vong.
    is_chu_tuoc_khong = ("Chu Tước" in tat_ca_tuong and (tk_so or tk_trung or tk_mat))
    is_phu_mau_khong = (lt_so == "Phụ Mẫu" and tk_so)
    if is_chu_tuoc_khong or is_phu_mau_khong:
        canh_bao.append("⚠️ CÂU 38 (Bế khẩu quái thể lưỡng ban thôi): Quẻ Bế Khẩu (Bịt miệng)! Lời nói bị cấm đoán, giấy tờ/hợp đồng xin phép bị bác bỏ, bưu kiện thất lạc. Ra tòa kiện tụng dù có uẩn khúc cũng không kêu oan được, đuối lý đàm phán.")

    # CÂU 39: Thái dương chiếu Vũ nghi cầm tặc
    # Lý thuyết: Trong quẻ nổi lên Huyền Vũ (Ăn trộm, lừa đảo, mờ ám). Nhưng có Thái Dương (Mặt trời/Ngọ) hoặc Thiên Tướng chiếu rọi thẳng vào nó.
    co_huyen_vu = "Huyền Vũ" in tat_ca_tuong
    co_anh_sang = ("Ngọ" in [k1_t, k2_t, k3_t, k4_t, so_chi, trung_chi, mat_chi] or "Thái Dương" in k1_sat or "Nguyệt Tướng" in k1_sat)
    if co_huyen_vu and co_anh_sang:
        canh_bao.append("✅ CÂU 39 (Thái dương chiếu Vũ nghi cầm tặc): Ánh sáng Mặt Trời rọi thẳng vào bóng tối Huyền Vũ. Cháy nhà ra mặt chuột! Đồ mất chắc chắn tìm lại được, kẻ lừa đảo, tham ô, ngoại tình lập tức bị vạch trần phơi bày ra ánh sáng.")

    # CÂU 40: Hậu Hợp chiếm hôn khởi dụng môi
    # Lý thuyết: Cát thần Thiên Hậu (Phụ nữ/Âm) và Lục Hợp (Hôn nhân/Kết hợp) cùng xuất hiện. Tượng trưng cho sự tự nguyện.
    if "Thiên Hậu" in tat_ca_tuong and "Lục Hợp" in tat_ca_tuong:
        canh_bao.append("✅ CÂU 40 (Hậu Hợp chiếm hôn khởi dụng môi): Quẻ nổi lên đồng thời Thiên Hậu và Lục Hợp. Xem tình duyên/đối tác thì hai bên tự nguyện cuốn hút lấy nhau, môn đăng hộ đối, cưới xin/hợp tác êm thấm thuận lợi mà không cần qua trung gian mai mối.")
   
   # ========================================================
    # NHÓM 5: HỆ THỐNG QUÝ NHÂN VÀ CỨU GIẢI (Câu 41 - 50)
    # Lấy trọn vẹn lý thuyết gốc Lục Nhâm Đại Toàn Quyển 3
    # ========================================================

    # CÂU 41: Phú quý can chi phùng lộc mã
    # Lý thuyết: Bản mệnh (Can) hoặc Cơ sở (Chi) hội tụ cả Thiên Lộc (Tiền tài/Quyền lực) và Thiên Mã (Tốc độ/Thăng tiến).
    loc_ma_k1 = any("Thiên Lộc" in s for s in k1_sat) and any("Thiên Mã" in s for s in k1_sat)
    loc_ma_k3 = any("Thiên Lộc" in s for s in k3_sat) and any("Thiên Mã" in s for s in k3_sat)
    if loc_ma_k1 or loc_ma_k3:
        canh_bao.append("✅ CÂU 41 (Phú quý can chi phùng lộc mã): Can hoặc Chi hội tụ cả Thiên Lộc và Thiên Mã. Mệnh 'Cưỡi ngựa ôm vàng'. Đại phú đại quý, sự nghiệp lên như diều gặp gió, vừa có chức vừa có lộc thực tế.")

    # CÂU 42: Tôn sùng thị nội ngộ tam kỳ (Giải cứu tột đỉnh)
    # Lý thuyết: Quẻ hung hiểm nhưng xuất hiện Thiên Đức, Nguyệt Đức hoặc Tam Kỳ. Đây là những "Kim bài miễn tử" mạnh nhất trong thuật số.
    co_giai_cuu = any("Đức" in s for s in k1_sat + k3_sat + sat_so)
    if co_giai_cuu and (lt_so == "Quan Quỷ" or lt_trung == "Quan Quỷ"):
        canh_bao.append("✅ CÂU 42 (Tôn sùng thị nội ngộ tam kỳ): Bĩ cực thái lai! Quẻ có Ác Sát/Quan Quỷ nhưng lại xuất hiện Thiên Đức/Nguyệt Đức phò trợ. Có nhân vật thế lực cực lớn (Sếp/Chính quyền) ra tay che chở, 'kim bài miễn tử' cứu qua cơn hoạn nạn phút chót.")

    # CÂU 43: Hại quý tụng trực tao khúc đoán
    # Lý thuyết: Quý Nhân xuất hiện nhưng bị Địa Bàn (Mẫu) xung hoặc khắc từ dưới lên. Quý nhân bị tổn thương, mất năng lực bảo vệ.
    quy_bi_thuong = (k1_tuong == "Quý Nhân" and (la_khac(k1_d, k1_t) or is_luc_xung(k1_d, k1_t))) or \
                    (tuong_so == "Quý Nhân" and (la_khac(can_ngay, so_chi) or is_luc_xung(can_ngay, so_chi)))
    if quy_bi_thuong:
        canh_bao.append("⚠️ CÂU 43 (Hại quý tụng trực tao khúc đoán): Quý Nhân xuất hiện nhưng bị Xung/Khắc từ dưới lên. Quý nhân bị trói tay, bị tổn hại. Đi kiện tụng dù đúng lý cũng bị xử thua oan uổng, sếp muốn bảo vệ mình cũng lực bất tòng tâm.")

    # CÂU 44: Khóa truyền câu quý chuyển vô y
    # Lý thuyết: Tứ Khóa Tam Truyền xuất hiện quá nhiều Quý Nhân (Từ 2 trở lên). Lắm mối tối nằm không.
    so_luong_quy = tat_ca_tuong.count("Quý Nhân")
    if so_luong_quy >= 2:
        canh_bao.append("⚠️ CÂU 44 (Khóa truyền câu quý chuyển vô y): Quẻ xuất hiện quá nhiều Quý Nhân ("+str(so_luong_quy)+" người). 'Lắm thầy thối ma', nhiều người can thiệp, ai cũng hứa giúp nhưng đùn đẩy trách nhiệm cho nhau. Rốt cục ỷ lại sinh ra hỏng việc, không chỗ nương tựa.")

    # CÂU 45: Trú dạ quý gia cầu lưỡng quý
    # Lý thuyết: Quý nhân ban ngày và ban đêm đều bảo hộ, giáng lâm ở các vị trí chốt chặn (Khóa 1 và Khóa 3, hoặc Sơ và Mạt) mà KHÔNG bị khắc.
    if (k1_tuong == "Quý Nhân" and k3_tuong == "Quý Nhân") or (tuong_so == "Quý Nhân" and tuong_mat == "Quý Nhân"):
        if not k1_tk and not k3_tk and not tk_so:
            canh_bao.append("✅ CÂU 45 (Trú dạ quý gia cầu lưỡng quý): Ngày đêm Quý Nhân đều giáng lâm phù trợ ở cả Ta và Khách (hoặc Đầu và Cuối). Bôn ba khắp nơi đều có người trải thảm đỏ mời chào, đi đâu cũng được trọng dụng giúp đỡ nhiệt tình.")

    # CÂU 46: Quý nhân sa trật sự sâm si
    # Lý thuyết: Quý Nhân rớt vào hố Tuần Không. Quyền lực ảo.
    if (k1_tuong == "Quý Nhân" and k1_tk) or (tuong_so == "Quý Nhân" and tk_so):
        canh_bao.append("⚠️ CÂU 46 (Quý nhân sa trật sự sâm si): Quý Nhân rớt vào Tuần Không (Sa trật). Người hứa giúp rốt cuộc chỉ là hứa suông, hoặc họ đang mất chức, thất thế. Lúc gian nan họ sẽ ngoảnh mặt làm ngơ, đừng nuôi ảo mộng.")

    # CÂU 47: Quý tuy tọa ngục nghi lâm can
    # Lý thuyết: Quý Nhân bị kẹt ở Thiên La Địa Võng (Thìn/Tuất) gọi là 'Tọa Ngục', bình thường không cứu được. NHƯNG nếu giáng thẳng vào Thượng thần Can Ngày (Khóa 1) thì vẫn gỡ gạc được.
    if k1_tuong == "Quý Nhân" and k1_d in ["Thìn", "Tuất"]:
        canh_bao.append("💡 CÂU 47 (Quý tuy tọa ngục nghi lâm can): Quý Nhân tuy bị mắc kẹt chuyện riêng (Ngồi lưới Thìn/Tuất) nhưng lại giáng trực tiếp vào Bản mệnh (Lâm Can). Quý nhân đang khó khăn nhưng vẫn ngoái lại bảo vệ bạn. Hãy kiên nhẫn bám trụ, thiết tha cầu xin ắt vẫn còn cơ hội cứu vớt.")

    # CÂU 48: Quỷ thừa Thiên Ất nãi thần kỳ
    # Lý thuyết: Lục Thần là Quan Quỷ (Áp lực/Luật pháp) nhưng Tướng lại là Quý Nhân. Thần phật hoặc Sếp lớn đè nén.
    if lt_so == "Quan Quỷ" and tuong_so == "Quý Nhân":
        canh_bao.append("⚠️ CÂU 48 (Quỷ thừa Thiên Ất nãi thần kỳ): Quan Quỷ (Tai họa/Áp lực) mượn danh Quý Nhân. Cẩn thận thần thánh quở trách, hoặc Sếp lớn/Chính quyền trực tiếp tạo áp lực đè ép không thể phản kháng. Phải thuận tòng, không được chống đối.")

    # CÂU 49: Lưỡng quý thụ khắc nan can quý
    # Lý thuyết: Quý Nhân ở Sơ truyền hoặc Khóa 1 bị chính nền tảng dưới chân (Địa Bàn) khắc lên mạnh mẽ, mà bản thân Can Ngày cũng đang Suy/Tử/Tuyệt.
    if (tuong_so == "Quý Nhân" and la_khac(k1_d, so_chi)) or (k1_tuong == "Quý Nhân" and la_khac(k1_d, k1_t)):
        canh_bao.append("⚠️ CÂU 49 (Lưỡng quý thụ khắc nan can quý): Quý Nhân bị chính nền tảng Địa Bàn khắc chế dữ dội (Hạ tặc Thượng). Kêu trời trời không thấu, cửa quan bị kẹt, xin xỏ vô ích. Tự mình phải tự thân vận động đối mặt với giông bão.")

    # CÂU 50: Nhị quý giai không hư hỷ kỳ
    # Lý thuyết: Quẻ xem có cả 2 Quý Nhân xuất hiện (Ví dụ ở Can và Chi, hoặc Khóa và Truyền) nhưng CẢ HAI đều rớt Tuần Không.
    if (k1_tuong == "Quý Nhân" and k1_tk) and (tuong_so == "Quý Nhân" and tk_so):
        canh_bao.append("⚠️ CÂU 50 (Nhị quý giai không hư hỷ kỳ): Toàn bộ Quý Nhân (Ngày và Đêm) đều dính Tuần Không. Mọi lời hứa thăng chức, hứa cho vay tiền, bảo lãnh đều là tin đồn thất thiệt, niềm vui ảo. Trận chiến này bạn hoàn toàn cô độc.")

    # ========================================================
    # NHÓM 6: THIÊN LA ĐỊA VÕNG & CẠM BẪY (Câu 51 - 60)
    # Lấy trọn vẹn lý thuyết gốc Lục Nhâm Đại Toàn Quyển 3
    # ========================================================

    # CÂU 51: Khôi độ Thiên môn quan cách định
    # Lý thuyết: Sao Thiên Khôi (Tuất) là cửa ngục/ác thần, giáng xuống Thiên Môn (Hợi). Mọi con đường lên trời kêu cứu đều bị bịt kín.
    # Quét Tứ khóa xem có cung nào Tuất (Thiên Bàn) đè lên Hợi (Địa Bàn) hay không.
    co_khoi_do_thien_mon = any(khoa["t"] == "Tuất" and khoa["d"] == "Hợi" for khoa in [{"t":k1_t, "d":k1_d}, {"t":k2_t, "d":k2_d}, {"t":k3_t, "d":k3_d}, {"t":k4_t, "d":k4_d}])
    if co_khoi_do_thien_mon:
        canh_bao.append("⚠️ CÂU 51 (Khôi độ Thiên môn quan cách định): Ác thần Tuất (Thiên Khôi) chặn đứng Cổng Trời Hợi (Thiên Môn). Mọi con đường giải thoát, thông quan, chạy án, rút vốn đều bị bịt kín. Cục diện cực kỳ tuyệt vọng, hãy dừng mọi hành động vùng vẫy.")

    # CÂU 52: Cương tuy quỷ hộ nhậm mưu vi
    # Lý thuyết: Sao Thiên Cương (Thìn - Đại cát) rớt vào Quỷ Hộ (Dần/Mão). Tuy bị kẹt ở cửa Quỷ nhưng Thìn có sức mạnh tuyệt đối, có thể dùng mưu trí xảo quyệt để lật ngược tình thế.
    if k1_t == "Thìn" and k1_d in ["Dần", "Mão"]:
        canh_bao.append("💡 CÂU 52 (Cương tuy quỷ hộ nhậm mưu vi): Thiên Cương (Thìn) rớt vào Cửa Quỷ (Dần/Mão). Bối cảnh vô cùng xảo quyệt và nguy hiểm. Lời khuyên: Phải dùng mưu kế thâm sâu, mượn tay gian hùng hoặc thế lực ngầm (dĩ độc trị độc) thì mới làm nên việc lớn.")

    # CÂU 53: Lưỡng Xà giáp mộ hung nan miễn
    # Lý thuyết: Ác thần Đằng Xà (Sợ hãi, mờ ám, tà thuật) kẹp ở cả Sơ truyền và Mạt truyền. Ở giữa (Trung truyền) lại là Mộ khố (Thìn, Tuất, Sửu, Mùi). 
    if tuong_so == "Đằng Xà" and tuong_mat == "Đằng Xà" and trung_chi in ["Thìn", "Tuất", "Sửu", "Mùi"]:
        canh_bao.append("⚠️ CÂU 53 (Lưỡng Xà giáp mộ hung nan miễn): Hai con Đằng Xà kẹp lấy Mộ khố. Ác mộng tột độ! Quẻ báo điềm bị giam cầm, dính líu đến tà ngải, vong linh quấy phá, hoặc một cuộc khủng hoảng truyền thông kinh hoàng đang bủa vây không lối thoát.")

    # CÂU 54: Hổ thị phùng Hổ lực nan thi
    # Lý thuyết: Bạch Hổ xuất hiện liên tiếp (Sơ Bạch Hổ, Trung Bạch Hổ). Hoặc Tướng Hổ gặp Độn Can cũng thuộc dòng sát thương.
    if tuong_so == "Bạch Hổ" and tuong_trung == "Bạch Hổ":
        canh_bao.append("⚠️ CÂU 54 (Hổ thị phùng Hổ lực nan thi): Bạch Hổ đối đầu Bạch Hổ. Lưỡng hổ tranh hùng, họa đổ máu gầm thét. Cảnh báo tai nạn giao thông, phẫu thuật bạo phát, kiện tụng hoặc tranh chấp dẫn đến thương vong, sức lực cá nhân nan thi (không thể chống đỡ).")

    # CÂU 55: Sở mưu đa chuyết phùng võng la
    # Lý thuyết: Tam truyền không thoát ra khỏi Thiên La (Thìn, Tỵ) và Địa Võng (Tuất, Hợi). 
    if so_chi in ["Thìn", "Tuất"] and trung_chi in ["Thìn", "Tuất"]:
        canh_bao.append("⚠️ CÂU 55 (Sở mưu đa chuyết phùng võng la): Sự việc bị kẹt cứng trong Thiên La Địa Võng. Càng dùng mưu trí cựa quậy càng vụng về (đa chuyết), càng gỡ càng rối, càng trói càng chặt. Hãy chấp nhận nằm im chịu trận chờ thời qua đi.")

    # CÂU 56: Thiên võng tự khỏa kỷ chiêu phi
    # Lý thuyết: Thiên Võng là lúc Thiên bàn và Địa bàn trùng nhau (Tự hình), đặc biệt rơi vào 4 cung góc Thìn, Tuất, Tỵ, Hợi. Tự mình đào hố chôn mình.
    if k1_t in ["Thìn", "Tuất", "Tỵ", "Hợi"] and k1_t == k1_d:
        canh_bao.append("⚠️ CÂU 56 (Thiên võng tự khỏa kỷ chiêu phi): Bản thân ngự trên Lưới Trời (Tự Hình). Lỗi không do ai cả, chính sự bốc đồng, tự cao, làm sai quy trình pháp luật của mình đã tự rước họa vào thân. Mau chóng tự thú hoặc sửa sai trước khi vỡ lở.")

    # CÂU 57: Phí hữu dư nhi đắc bất túc
    # Lý thuyết: Chủ Sinh xuất (Hao tốn năng lượng), Khách Khắc Chủ (Chống đối). Tiền vứt qua cửa sổ.
    if la_sinh(k1_d, k1_t) and la_khac(k3_t, k3_d):
        canh_bao.append("⚠️ CÂU 57 (Phí hữu dư nhi đắc bất túc): Ta hao tổn sinh ra, nhưng Khách lại bị đè nén/chống đối. Chi phí đầu tư bạt ngàn, làm rầm rộ nhưng thu về nhỏ giọt, dòng tiền đứt gãy. Tuyệt đối không được mở rộng thêm dự án này.")

    # CÂU 58: Dụng phá thân tâm vô sở quy
    # Lý thuyết: Dụng thần (Sơ truyền) rớt vào Không Vong (Phá), lại bị các Ác thần (Bạch Hổ, Câu Trần, Đằng Xà, Chu Tước) án ngữ làm tinh thần hoảng loạn.
    if tk_so and tuong_so in ["Bạch Hổ", "Câu Trần", "Đằng Xà", "Chu Tước"]:
        canh_bao.append("⚠️ CÂU 58 (Dụng phá thân tâm vô sở quy): Khởi đầu vướng Không Vong lại cõng Ác Thần. Tâm trí hoảng loạn, trầm cảm tột độ, mất định hướng trầm trọng, có cảm giác muốn bỏ trốn đi thật xa vì không còn chốn nương thân.")

    # CÂU 59: Hoa cái phúc nhật nhân hôn hối
    # Lý thuyết: Thần sát 'Hoa Cái' (Chủ về nghệ thuật, tâm linh, nhưng u buồn, che giấu) giáng thẳng xuống Can Ngày (Khóa 1). Mây đen che lấp mặt trời.
    if "Hoa Cái" in k1_sat:
        canh_bao.append("⚠️ CÂU 59 (Hoa cái phúc nhật nhân hôn hối): Ám tinh Hoa Cái che mờ Bản mệnh. Năng lực bị sếp/thế lực khác lấp bóng cướp công. Tâm trạng u uất, dễ bị lừa gạt, hoặc bản thân đang cố che giấu một sự thật mờ ám nào đó.")

    # CÂU 60: Thái dương xạ trạch ốc quang huy
    # Lý thuyết: Thượng thần của Địa Chi (Khóa 3 - Trạch) có Thái Dương (Mặt trời) hoặc là Địa Chi Ngọ (Hỏa). Chiếu sáng xua tan mọi tà khí.
    if k3_t == "Ngọ" or "Thái Dương" in k3_sat:
        canh_bao.append("✅ CÂU 60 (Thái dương xạ trạch ốc quang huy): Ánh sáng Thái Dương rọi thẳng vào Nhà Cửa/Công ty (Khóa 3). Vận khí bừng sáng rực rỡ, tẩy uế mọi tà khí, phong thủy nhà đất cực vượng, đầu tư bất động sản sẽ thắng lớn.")

    # ========================================================
    # NHÓM 7: BỆNH TẬT, PHÁP LÝ & GIA ĐẠO (Câu 61 - 70)
    # Lấy trọn vẹn lý thuyết gốc Lục Nhâm Đại Toàn Quyển 3
    # ========================================================

    # Tính toán trước Mộ Khố của Can và Chi để dùng cho Nhóm 7
    mo_can = MO_MAP.get(NGU_HANH.get(can_ngay, ""))
    mo_chi = MO_MAP.get(NGU_HANH.get(chi_ngay, ""))

    # CÂU 61: Can thừa mộ Hổ vô chiếm bệnh
    # Lý thuyết: Thượng thần Khóa 1 (Can/Người) vừa là Mộ Khố của Can, vừa cõng Bạch Hổ. 
    # Bệnh nhân đã bước 1 chân vào nấm mồ lại bị Hổ cắn.
    if k1_tuong == "Bạch Hổ" and k1_t == mo_can:
        canh_bao.append("⚠️ CÂU 61 (Can thừa mộ Hổ vô chiếm bệnh): Bạch Hổ rơi vào Mộ giáng thẳng xuống Bản mệnh. Quẻ hỏi bệnh thì cầm chắc án tử, vô phương cứu chữa, hãy chuẩn bị hậu sự. Nếu hỏi việc thì vướng vòng lao lý, bị giam cầm tột độ.")

    # CÂU 62: Chi thừa mộ Hổ hữu phục thi
    # Lý thuyết: Thượng thần Khóa 3 (Chi/Nhà cửa) vừa là Mộ Khố của Chi, vừa cõng Bạch Hổ.
    # Đất ở có xương cốt, phong thủy cực độc.
    if k3_tuong == "Bạch Hổ" and k3_t == mo_chi:
        canh_bao.append("⚠️ CÂU 62 (Chi thừa mộ Hổ hữu phục thi): Bạch Hổ nhập Mộ ở cung Địa Chi (Khách/Trạch). Nếu xem Gia trạch: Dưới móng nhà có cốt/hài nhi vô danh, phong thủy có phục thi tà ma quấy phá. Nếu xem công ty: Cơ sở vật chất đang mục nát, có nợ xấu chôn vùi.")

    # CÂU 63: Bỉ thử toàn thương phòng lưỡng tổn
    # Lý thuyết: Khóa 1 (Can) tự khắc nhau (Hạ tặc Thượng hoặc Thượng khắc Hạ), đồng thời Khóa 3 (Chi) cũng tự khắc nhau.
    # Cả Ta và Khách đều đang có nội chiến, tổn thương.
    can_tu_khac = la_khac(k1_t, k1_d) or la_khac(k1_d, k1_t)
    chi_tu_khac = la_khac(k3_t, k3_d) or la_khac(k3_d, k3_t)
    if can_tu_khac and chi_tu_khac:
        canh_bao.append("⚠️ CÂU 63 (Bỉ thử toàn thương phòng lưỡng tổn): Cả Ta và Khách đều đang bị nội chiến tự đâm xé lẫn nhau. Đôi bên cùng thiệt hại nặng nề. Hợp tác sẽ dắt tay nhau xuống hố, đánh nhau thì lưỡng bại câu thương, không ai được lợi.")

    # CÂU 64: Phu phụ vu dâm các hữu tư
    # Lý thuyết: Trong quẻ nổi lên các sao Đào Hoa, Thiên Hậu (Nữ), Lục Hợp (Giao hoan), Huyền Vũ (Mờ ám) kết hợp đan chéo. 
    # Đại diện cho sự ngoại tình, tà dâm.
    co_sao_tinh_ai = ("Thiên Hậu" in tat_ca_tuong and "Lục Hợp" in tat_ca_tuong)
    co_sao_mo_am = ("Đào Hoa" in k1_sat or "Đào Hoa" in k3_sat or "Huyền Vũ" in tat_ca_tuong)
    if co_sao_tinh_ai and co_sao_mo_am:
        canh_bao.append("⚠️ CÂU 64 (Phu phụ vu dâm các hữu tư): Quẻ xuất hiện Thiên Hậu và Lục Hợp bị tà khí (Đào hoa/Huyền Vũ) xâm lấn. Dấu hiệu ngoại tình rõ rệt! Vợ chồng bất hòa, đồng sàng dị mộng, mỗi người đều có nhân tình hoặc toan tính mờ ám riêng bên ngoài.")

    # CÂU 65: Can mộ tịnh quan nhân trạch phế
    # Lý thuyết: Thượng thần Khóa 1 (Ta) rơi vào Mộ của Chi. Thượng thần Khóa 3 (Nhà) rơi vào Mộ của Can. 
    # Ta chui vào mộ nhà, Nhà chôn cất ta.
    if k1_t == mo_chi and k3_t == mo_can:
        canh_bao.append("⚠️ CÂU 65 (Can mộ tịnh quan nhân trạch phế): Chủ chui vào Mộ của Khách, Khách chui vào Mộ của Chủ. Trạch phế người kiệt! Công ty phá sản sụp đổ, gia đình ly tán bán xới dọn ra đường ở. Năng lượng triệt tiêu hoàn toàn.")

    # CÂU 66: Chi phần tài tịnh lữ trình kê
    # Lý thuyết: Sơ truyền là Thê Tài (Tiền/Hàng hóa) nhưng rơi vào Mộ Khố (Thìn, Tuất, Sửu, Mùi) lại mang theo Bạch Hổ.
    if lt_so == "Thê Tài" and so_chi in ["Sửu", "Thìn", "Mùi", "Tuất"] and tuong_so == "Bạch Hổ":
        canh_bao.append("⚠️ CÂU 66 (Chi phần tài tịnh lữ trình kê): Tài sản/Hàng hóa kẹt cứng trong Mộ lại bị Hổ cắn. Đường đi bị chặn đứng. Đi lại du lịch công tác bị hoãn, hàng hóa đọng kho mục nát không xuất được, tiền kẹt cứng trong đất/dự án không rút ra được.")

    # CÂU 67: Thụ Hổ khắc thần vi bệnh chứng
    # Lý thuyết: Ác thần Bạch Hổ giáng xuống và khắc trực tiếp Bản mệnh (Khóa 1) hoặc Sơ truyền.
    if k1_tuong == "Bạch Hổ" and la_khac(k1_t, k1_d):
        canh_bao.append("⚠️ CÂU 67 (Thụ Hổ khắc thần vi bệnh chứng): Bạch Hổ (Thần máu me, bệnh tật) đâm thẳng vào Bản mệnh. Cảnh báo bệnh tật bạo phát, có nguy cơ phải phẫu thuật dao kéo đổ máu, khối u, tai nạn cấp cứu. Ngũ hành của Bạch Hổ chính là bộ phận phát bệnh (Kim: Phổi/Xương, Mộc: Gan...)")

    # CÂU 68: Chế quỷ chi vị nãi lương y
    # Lý thuyết: Trong quẻ có Quan Quỷ (Bệnh tật/Tai họa), nhưng xuất hiện Tử Tôn (Thần y/Luật sư) đi ra khắc chế lại Quỷ.
    co_quy = (lt_so == "Quan Quỷ" or lt_trung == "Quan Quỷ")
    co_tu_ton = (lt_mat == "Tử Tôn" or lt_trung == "Tử Tôn")
    if co_quy and co_tu_ton:
        canh_bao.append("✅ CÂU 68 (Chế quỷ chi vị nãi lương y): Bệnh nặng cỡ nào, án lớn cỡ nào cũng có đường thoát! Tử Tôn (Thần Y / Cứu tinh) đã xuất hiện để khắc chế Quan Quỷ. Hãy tìm bác sĩ hoặc luật sư có đặc điểm (Ngũ hành/Phương hướng) ứng với Tử Tôn, họ chính là người giải cứu bạn!")

    # CÂU 69: Hổ thừa độn quỷ ương phi thiển
    # Lý thuyết: Bạch Hổ ở Sơ truyền, mà Độn Can của Sơ truyền lại là Quan Quỷ khắc Can Ngày. (Hổ cõng Quỷ)
    don_can_ngu_hanh = NGU_HANH.get(don_can_so, "")
    don_can_la_quy = {"Mộc":"Kim", "Hỏa":"Thủy", "Thổ":"Mộc", "Kim":"Hỏa", "Thủy":"Thổ"}.get(NGU_HANH.get(can_ngay)) == don_can_ngu_hanh
    if tuong_so == "Bạch Hổ" and don_can_la_quy:
        canh_bao.append("⚠️ CÂU 69 (Hổ thừa độn quỷ ương phi thiển): Hổ cõng theo Quỷ môn (Độn can là Quỷ). Ách tai đến rất sâu và hiểm độc. Tàn phá khủng khiếp gia đạo, tang tóc cận kề, kiện tụng không chừa lối thoát. Tuyệt đối không được chủ quan!")

    # CÂU 70: Quỷ lâm tam tứ tụng tai tùy
    # Lý thuyết: Quan Quỷ chiếm cứ cả Khóa 3 (Thượng thần Chi) và Khóa 4 (Âm thần Chi). Căn nhà/Đối tác toàn là Quỷ.
    if k3_lt == "Quan Quỷ" and k4_lt == "Quan Quỷ":
        canh_bao.append("⚠️ CÂU 70 (Quỷ lâm tam tứ tụng tai tùy): Quan Quỷ (Tai họa) chiếm cứ toàn bộ nền tảng Khách/Nhà cửa (Khóa 3 và 4). Việc kiện tụng/mâu thuẫn càng kéo dài càng bất lợi, đối phương vô cùng hung hiểm, tà khí bám gót không buông.")

    # ========================================================
    # NHÓM 8: HUNG HỌA ĐẢO CHIỀU & XUNG HẠI (Câu 71 - 80)
    # Lấy trọn vẹn lý thuyết gốc Lục Nhâm Đại Toàn Quyển 3
    # ========================================================

    # CÂU 71: Bệnh phù khắc trạch toàn gia hoạn
    # Lý thuyết: Thần sát 'Bệnh Phù' giáng xuống Thượng thần Địa Chi (Khóa 3 - Trạch) và khắc lên Địa bàn (Hạ tặc Thượng). 
    # Cả nhà/công ty bị dịch bệnh/suy thoái.
    if "Bệnh Phù" in k3_sat and la_khac(k3_t, k3_d):
        canh_bao.append("⚠️ CÂU 71 (Bệnh phù khắc trạch toàn gia hoạn): Sao Bệnh Phù khắc trực tiếp lên Khóa 3 (Trạch). Dịch bệnh lây lan, phong thủy tà khí làm cả gia đình/công ty ốm liệt giường hoặc suy thoái đồng loạt.")

    # CÂU 72: Tang điếu toàn phùng quải cảo y
    # Lý thuyết: Thần sát 'Tang Môn' (Khóa 1) và 'Điếu Khách' (Khóa 3) cùng xuất hiện. 
    # Điềm báo tang tóc, chuyện buồn phiền.
    if "Tang Môn" in k1_sat and "Điếu Khách" in k3_sat:
        canh_bao.append("⚠️ CÂU 72 (Tang điếu toàn phùng quải cảo y): Tang Môn và Điếu Khách hội tụ hai bờ Chủ Khách. Dấu hiệu hung tang rất nặng, có chuyện phải mặc đồ xô gai, hoặc chuyện buồn phiền đưa tới liên miên.")

    # CÂU 73: Tiền hậu bức bách nan tiến thoái
    # Lý thuyết: Tam truyền bị kẹp giữa những thế lực khắc nhau (Nội chiến). 
    # Sơ khắc Trung, Trung khắc Mạt (hoặc ngược lại). 
    if la_khac(trung_chi, so_chi) and la_khac(mat_chi, trung_chi):
        canh_bao.append("⚠️ CÂU 73 (Tiền hậu bức bách nan tiến thoái): Tam truyền đi lùi và khắc nhau liên tục. Bạn đang bị kẹp giữa làn đạn, áp lực tứ bề, tiến không được mà thoái không xong.")

    # CÂU 74: Không không như dã sự hưu truy
    # Lý thuyết: Đại Không Vong (Tam truyền cả 3 vòng đều rớt Tuần Không). Sự việc hoàn toàn vô căn cứ.
    if tk_so and tk_trung and tk_mat:
        canh_bao.append("⚠️ CÂU 74 (Không không như dã sự hưu truy): Tam truyền ĐẠI KHÔNG VONG. Trống rỗng hoàn toàn, bong bóng xà phòng. Tuyệt đối đừng tốn công vô ích, đây là quẻ 'không có thực', buông bỏ ngay.")

    # CÂU 75: Tân chủ bất đầu hình tại thượng
    # Lý thuyết: Khóa 1 (Ta) và Khóa 3 (Khách) tương Xung (Lục xung). Mâu thuẫn đối đầu trực diện.
    if is_luc_xung(k1_t, k3_t):
        canh_bao.append("⚠️ CÂU 75 (Tân chủ bất đầu hình tại thượng): Chủ và Khách đối đầu (Lục Xung). Đàm phán vỡ lở, cãi vã tung tóe, không ai nhường ai. Đừng hy vọng hợp tác, hãy chuẩn bị cho một cuộc đối đầu trực diện.")

    # CÂU 76: Bỉ thử xai kỵ hại tương tùy
    # Lý thuyết: Khóa 1 (Ta) và Khóa 3 (Khách) tương Hại (Lục hại). Bằng mặt không bằng lòng, gài bẫy.
    if is_luc_hai(k1_t, k3_t):
        canh_bao.append("⚠️ CÂU 76 (Bỉ thử xai kỵ hại tương tùy): Hai bên Chủ Khách Lục Hại nhau. Bằng mặt không bằng lòng, đối phương gài bẫy đâm lén, nghi kỵ tột độ. Coi chừng bị chơi xỏ từ sau lưng.")

    # CÂU 77: Hỗ sinh câu sinh phàm sự ích
    # Lý thuyết: Thiên bàn Can (K1) sinh Địa bàn (K1), Thiên bàn Chi (K3) sinh Địa bàn (K3) HOẶC chéo góc sinh. Sự tương hỗ âm thầm.
    if la_sinh(k1_t, k4_t) and la_sinh(k3_t, k2_t):
        canh_bao.append("✅ CÂU 77 (Hỗ sinh câu sinh phàm sự ích): Đôi bên cùng âm thầm bồi đắp cho nhau. Hợp tác sinh lợi lớn, mọi việc trơn tru êm đẹp, lấy lợi ích chung làm trọng.")

    # CÂU 78: Hỗ vượng giai vượng tọa mưu nghi
    # Lý thuyết: Khí thế của Tứ Khóa (Can/Chi) đều đạt Vượng/Tướng (Không bị Tuần Không). Đủ lực làm việc lớn.
    if not k1_tk and not k3_tk and ("VƯỢNG" in k1_vs or "TƯỚNG" in k1_vs):
        canh_bao.append("✅ CÂU 78 (Hỗ vượng giai vượng tọa mưu nghi): Khí thế cả Ta và Khách đều đạt đỉnh Vượng. Làm ăn lớn, đầu tư lớn ắt thắng đậm, cục thế hưng thịnh tột bậc, thời cơ chín muồi.")

    # CÂU 79: Can chi thừa khí đa giao đoạt
    # Lý thuyết: Thiên bàn của Can và Chi có 'Kiếp Sát' hoặc khắc nhau dữ dội (Giao đoạt). Hiện tượng tranh giành cướp khách, cướp tài sản.
    if "Kiếp Sát" in k1_sat and "Kiếp Sát" in k3_sat:
        canh_bao.append("⚠️ CÂU 79 (Can chi thừa khí đa giao đoạt): Năng lượng hỗn loạn, Kiếp Sát lâm môn. Cẩn thận có hiện tượng tranh giành tài sản, cướp khách, bị đối thủ chơi xấu chia chác không đều.")

    # CÂU 80: Hóa khách vi chủ chỉ tu trì
    # Lý thuyết: Thiên bàn Khóa 3 (Khách) lại chuyển thành Địa bàn Khóa 1 (Ta) và ngược lại. Sự chuyển thế Chủ-Khách.
    if k1_t == k3_d and k3_t == k1_d:
        canh_bao.append("💡 CÂU 80 (Hóa khách vi chủ chỉ tu trì): Đảo lộn vị thế Chủ Khách (Chuyển Hóa). Mình đang từ thế bị động, tự nhiên chuyển thành thế chủ động nắm quyền kiểm soát. Hãy giữ vững vị thế này.")

    # ========================================================
    # NHÓM 9: THAM HỢP VONG XUNG VÀ ĐỘNG TĨNH (Câu 81 - 90)
    # Lý thuyết: Tâm lý học năng lượng - Sự cám dỗ và Lãng quên
    # ========================================================

    # CÂU 81: Tham sinh vong khắc nguyên phi khắc
    # Lý thuyết: Kẻ thù (Sơ truyền) định đến khắc Ta (Can Ngày). 
    # Nhưng Sơ truyền lại thấy Trung truyền là thứ nó sinh ra được, nó mê mải chạy theo Trung truyền mà quên mất việc hại Ta.
    if la_khac(so_chi, can_ngay) and la_sinh(so_chi, trung_chi):
        canh_bao.append("✅ CÂU 81 (Tham sinh vong khắc nguyên phi khắc): Quẻ có Thái binh! Kẻ định hãm hại/khắc chế bạn lại bị lực lượng khác dụ dỗ (Tham sinh quên khắc). Họa tự tiêu tan một cách thần kỳ vì đối thủ đang bận rộn chạy theo mục tiêu khác.")

    # CÂU 82: Tham hợp vong sinh diệc bất sinh
    # Lý thuyết: Người định đến giúp Ta (Sơ truyền sinh Can).
    # Nhưng Sơ truyền lại gặp Trung truyền Lục Hợp với nó. Nó mê mải tình ái/hợp tác với kẻ khác mà quên mất việc giúp Ta.
    if la_sinh(so_chi, can_ngay) and is_luc_hop(so_chi, trung_chi):
        canh_bao.append("⚠️ CÂU 82 (Tham hợp vong sinh diệc bất sinh): Người hứa hẹn giúp đỡ/rót vốn cho bạn lại bị rủ rê đi hợp tác với kẻ khác mất rồi (Tham hợp quên sinh). Sự trợ giúp bị đứt gánh giữa đường, không trông cậy được gì đâu.")

    # CÂU 83: Vạn sự hỉ hân tam lục hợp
    # Lý thuyết: Tam Truyền tạo thành cục Tam Hợp (VD: Dần-Ngọ-Tuất, Thân-Tý-Thìn). Năng lượng quần tụ vô cùng mạnh mẽ.
    if "Tam Hợp Cục" in tam_truyen.get("cuc_dien", []):
        canh_bao.append("✅ CÂU 83 (Vạn sự hỉ hân tam lục hợp): Quẻ đắc Tam Hợp cục. Vạn vật vui vẻ, quần tụ. Sự việc thành công viên mãn, có sự chung tay của nhiều thế lực, quy mô được mở rộng và vô cùng bền vững.")

    # CÂU 84: Hợp trung phạm sát mật trung tỳ
    # Lý thuyết: Bề mặt thì Khóa 1 và Khóa 3 Lục Hợp nhau (Hòa hảo). 
    # Nhưng bên trong nội bộ Tứ Khóa lại có Tương khắc (Nội chiến) hoặc Tướng mang Bạch Hổ/Câu Trần.
    co_giao_hop = is_luc_hop(k1_t, k3_t) or (is_luc_hop(k1_t, k4_t) and is_luc_hop(k2_t, k3_t))
    co_noi_sat = la_khac(k1_t, k1_d) or la_khac(k3_t, k3_d) or ("Bạch Hổ" in tat_ca_tuong)
    if co_giao_hop and co_noi_sat:
        canh_bao.append("⚠️ CÂU 84 (Hợp trung phạm sát mật trung tỳ): Mật ngọt chết ruồi! Bề ngoài đối tác tỏ ra cực kỳ thân thiện êm ấm (Lục Hợp), nhưng bên trong đã gài sẵn bẫy sát thương đứt ruột. Cú lừa siêu kinh điển, đọc kỹ lại hợp đồng!")

    # CÂU 85: Sơ tao giáp khắc bất do kỷ
    # Lý thuyết: Sơ truyền bị kẹp giữa 2 làn đạn (Ví dụ: Bị Thiên Can khắc, và bị chính Tướng của nó khắc). Thân bất do kỷ.
    bi_can_khac = la_khac(can_ngay, so_chi)
    bi_tuong_khac = la_khac(tuong_so, so_chi)
    if bi_can_khac and bi_tuong_khac:
        canh_bao.append("⚠️ CÂU 85 (Sơ tao giáp khắc bất do kỷ): Bị áp lực kẹp chặt từ cả 2 phía (Nội Ngoại đều khắc). Thân bất do kỷ, bị thế lực lớn mạnh hơn ép buộc làm việc mình không muốn, không có lối thoát từ chối.")

    # CÂU 86: Tướng phùng nội chiến sở mưu nguy
    # Lý thuyết: Sơ truyền bị "Nội chiến" (Thiên bàn khắc Địa bàn, hoặc Tướng khắc Chi). Nền tảng tự sụp đổ.
    if tam_truyen["so"].get("noi_ngoai_chien", "") == "NỘI CHIẾN (Gốc đâm Ngọn)":
        canh_bao.append("⚠️ CÂU 86 (Tướng phùng nội chiến sở mưu nguy): Bề ngoài hào nhoáng nhưng bên trong đang Nội Chiến dữ dội (Tướng khắc Chi). Nhân viên đâm sau lưng sếp, đối tác lừa gạt đâm lén nhau. Việc mưu cầu ắt thất bại từ trong trứng nước.")

    # CÂU 87: Nhân trạch tọa mộ cam chiêu hối
    # Lý thuyết: Khóa 1 (Người) và Khóa 3 (Nhà) cùng lúc ngự trên Mộ khố của vòng Trường sinh, hoặc ngự trên Thìn/Tuất/Sửu/Mùi.
    if k1_d in ["Thìn", "Tuất", "Sửu", "Mùi"] and k3_d in ["Thìn", "Tuất", "Sửu", "Mùi"]:
        canh_bao.append("⚠️ CÂU 87 (Nhân trạch tọa mộ cam chiêu hối): Cả Người và Nhà đều đang ngồi bệt trong Mộ khố. U uất, bế tắc, trầm cảm, làm những việc mờ ám để rồi tự chuốc lấy tiếng nhơ, hối hận không kịp.")

    # CÂU 88: Can chi thừa mộ các hôn mê
    # Lý thuyết: Thượng thần của Can là Mộ của Can. Thượng thần của Chi là Mộ của Chi. Mù quáng toàn tập.
    if k1_t == MO_MAP.get(NGU_HANH.get(can_ngay, "")) and k3_t == MO_MAP.get(NGU_HANH.get(chi_ngay, "")):
        canh_bao.append("⚠️ CÂU 88 (Can chi thừa mộ các hôn mê): Cả Can và Chi đều bị Thượng thần úp Mộ lên đầu (Hôn mê). Quyết định đầu tư lúc này y hệt người mù bịt mắt đi đêm, đầu óc không tỉnh táo, đâm đầu xuống vực sâu.")

    # CÂU 89: Nhậm tín Đinh Mã tu ngôn động
    # Lý thuyết: Quẻ vừa có Thiên Mã ở Tứ khóa, lại vừa có Độn Can Đinh ở Sơ truyền. Cực Động!
    co_thien_ma = any("Thiên Mã" in s for s in k1_sat + k3_sat)
    if don_can_so == "Đinh" and co_thien_ma:
        canh_bao.append("✅ CÂU 89 (Nhậm tín Đinh Mã tu ngôn động): Ngựa cất vó, tín lệnh đã phát! Độn Can Đinh hội tụ Thiên Mã. Sự việc không thể nằm im, ắt phải có xê dịch thần tốc, công tác, dời nhà, nhảy việc ngay lập tức.")

    # CÂU 90: Lai khứ câu không khởi động nghi
    # Lý thuyết: Khóa 1 (Đến/Bản thân) rớt Không Vong, Khóa 3 (Đi/Sự việc) cũng rớt Không Vong.
    if k1_tk and k3_tk:
        canh_bao.append("⚠️ CÂU 90 (Lai khứ câu không khởi động nghi): Tứ Khóa 1 và 3 đều rơi vào Tuần Không. Đến cũng không, đi cũng không. Chân không chạm đất. Mọi kế hoạch lúc này đều là ảo tưởng phi thực tế, hãy hủy bỏ hết đi, tuyệt đối không hành động.")

    # ========================================================
    # NHÓM 10: KỸ THUẬT BẮN TỈA CHỐT HẠ (Câu 91 - 100)
    # Lý thuyết: Các quy tắc Meta phá vỡ logic thông thường
    # ========================================================

    # CÂU 91: Hổ lâm can quỷ hung tốc tốc
    # Lý thuyết: Khóa 1 (Can Ngày) vừa là Quan Quỷ, lại vừa cõng Bạch Hổ. Mức độ bạo phát nhanh nhất trong Lục Nhâm.
    if k1_tuong == "Bạch Hổ" and k1_lt == "Quan Quỷ":
        canh_bao.append("⚠️ CÂU 91 (Hổ lâm can quỷ hung tốc tốc): Tử thần gõ cửa! Hổ cõng Quỷ giáng ngay trên đầu Bản mệnh. Họa tới chân rồi, thần tốc tàn phá: Phẫu thuật, hình ngục, tai nạn giao thông lập tức ập xuống. Phải vô cùng cẩn trọng!")

    # CÂU 92: Long gia sinh khí cát trì trì
    # Lý thuyết: Khóa 1 (Can Ngày) là sao Trường Sinh, hoặc Tương sinh, lại cõng Thanh Long. Cực cát nhưng cực chậm.
    if k1_tuong == "Thanh Long" and (k1_ts == "Trường Sinh" or la_sinh(k1_t, k1_d)):
        canh_bao.append("✅ CÂU 92 (Long gia sinh khí cát trì trì): Thanh Long mang sinh khí giáng xuống Bản mệnh. Việc cực tốt, tiền tài vượng phát, nhưng SẼ ĐẾN TỪ TỪ. Cấm nóng vội, giục tốc bất đạt, cứ thong thả tĩnh tâm mà thu lưới.")

    # CÂU 93: Vọng dụng tam truyền tai phúc dị
    # Lý thuyết: Sơ truyền là Huynh Đệ (Kẻ cướp), Mạt truyền quay lại Khắc Sơ truyền. Sai từ bước đầu.
    if lt_so == "Huynh Đệ" and la_khac(mat_chi, so_chi):
        canh_bao.append("⚠️ CÂU 93 (Vọng dụng tam truyền tai phúc dị): Sơ truyền là Kẻ cướp, Mạt truyền kết liễu luôn Sơ truyền. Cảnh báo: Dùng sai người, chọn nhầm đường lối, 'rước giặc vào nhà' dẫn đến kết cục tai họa khôn lường!")

    # CÂU 94: Hỉ cụ không vong nãi diệu cơ
    # Lý thuyết: Chìa khóa vàng của Lục Nhâm. Cát tinh rớt Không Vong thì vui hụt. Hung tinh rớt Không Vong thì thoát chết.
    # Đã được lồng ghép logic này rải rác ở các câu Không Vong phía trên.
    if tk_so:
        canh_bao.append("💡 CÂU 94 (Hỉ cụ không vong nãi diệu cơ): Khởi đầu vướng Tuần Không. Cát rơi vào Không thì vui mừng hụt. Nhưng Hung rớt vào Không thì tai họa tiêu tan. Tuần Không là cỗ máy đảo lộn sinh tử tột đỉnh trong Lục Nhâm.")

    # CÂU 95: Lục hào hiện quái phòng kỳ khắc
    # Lý thuyết: Tứ Khóa (4) + Sơ Truyền (1) + Trung Truyền (1) nổi lên tạo thành 6 Địa Chi khác nhau hoàn toàn. Nhưng bên trong lại có Xung/Khắc ngầm.
    chi_hien_dien = [k1_t, k2_t, k3_t, k4_t, so_chi, trung_chi]
    if len(set(chi_hien_dien)) == 6 and (la_khac(tuong_so, so_chi) or la_khac(tuong_trung, trung_chi)):
        canh_bao.append("⚠️ CÂU 95 (Lục hào hiện quái phòng kỳ khắc): 6 Hào đều nổi lên mặt nước chật chội, nhưng lại có Tương Khắc ngầm. Cẩn thận sát thủ giấu mặt từ các phe phái đâm lén chéo nhau trong nội bộ. Việc có nhiều mưu mô phức tạp.")

    # CÂU 96: Tuần nội không vong trục loại thôi
    # Lý thuyết: Tuần Không Vong chia làm Giả Không (Vượng tướng) và Tuyệt Không (Hưu tù).
    if tk_so and ("VƯỢNG" in vs_so or "TƯỚNG" in vs_so):
        canh_bao.append("💡 CÂU 96 (Tuần nội không vong trục loại thôi): Ác thần / Năng lượng rớt Tuần Không nhưng lại mang Khí Vượng Tướng. Đây là GIẢ KHÔNG. Đừng tưởng là không có gì, nó chỉ bị kẹt tạm thời, hãy đợi tới ngày Xung Không thì quả bom sẽ nổ tung!")

    # CÂU 97: Sở thệ bất nhập nhưng bằng loại
    # Lý thuyết: Quẻ không xuất hiện thứ khách hỏi (Ví dụ: Hỏi tiền mà Tam truyền không có Thê Tài). Phải tìm ở Độn Can hoặc dưới Địa Bàn.
    luc_than_tam_truyen = [lt_so, lt_trung, lt_mat]
    if "Thê Tài" not in luc_than_tam_truyen:
        canh_bao.append("💡 CÂU 97 (Sở thệ bất nhập nhưng bằng loại): Chú ý! Quẻ KHÔNG HIỆN LÊN Thê Tài. Nếu khách hỏi Tiền bạc/Tình duyên thì đừng vội hoảng bảo họ mất hết, hãy bình tĩnh tìm 'Loại Thần' của nó ẩn ngầm ở Độn Can hoặc trốn dưới mâm Địa Bàn.")

    # CÂU 98: Phi chiếm hiện loại vật ngôn chi
    # Lý thuyết: Khách không hỏi, nhưng quẻ nổi lên Huyền Vũ (Ăn trộm, ngoại tình). Quy tắc "Im lặng là vàng".
    if "Huyền Vũ" in [tuong_so, tuong_trung, tuong_mat]:
        canh_bao.append("💡 CÂU 98 (Phi chiếm hiện loại vật ngôn chi): Quẻ bất ngờ nổi lên sao Huyền Vũ (Ăn trộm, lừa gạt, ngoại tình). Lời răn của cổ nhân: Nếu khách KHÔNG HỎI về mất đồ hay chuyện phòng the thì tuyệt đối KHÔNG ĐƯỢC bép xép nói leo kẻo chuốc vạ thị phi vào thân.")

    # CÂU 99: Thường vấn bất ứng phùng cát tượng
    # Lý thuyết: Quẻ Sinh khắc cực đẹp, nhưng lại có sự mâu thuẫn cốt lõi (Lục xung). Việc phi thực tế.
    if la_sinh(k1_t, k1_d) and la_sinh(k3_t, k3_d) and is_luc_xung(k1_t, k3_t):
        canh_bao.append("💡 CÂU 99 (Thường vấn bất ứng phùng cát tượng): Quẻ có Tương Sinh cực đẹp nhưng lại xen lẫn Lục Xung. Cẩn thận bẫy: Nếu câu hỏi/tham vọng của khách hàng là phi thực tế (ảo tưởng), thì quẻ có hiển thị đẹp đến mấy rốt cục cũng vô dụng, thất bại.")

    # CÂU 100: Dĩ tai hung đào phản vô nghi
    # Lý thuyết: Cú chốt của Tất Pháp Phú - Đỉnh cao của Đạo gia. Tứ Khóa Khắc toàn tập. Vật cực tất phản.
    toan_khac = la_khac(k1_t, k1_d) and la_khac(k2_t, k2_d) and la_khac(k3_t, k3_d) and la_khac(k4_t, k4_d)
    if toan_khac:
        canh_bao.append("✅ CÂU 100 (Dĩ tai hung đào phản vô nghi): Tứ Khóa toàn Khắc, hung hiểm tột cùng! Tuy nhiên 'Vật Cực Tất Phản'. Sự việc đã trải qua tột cùng kiếp nạn, đã chạm đáy nỗi đau rồi thì vòng quay lật ngược lại: Mọi sóng gió sẽ tự tắt, thái bình chắc chắn sẽ đến! Cứ vững tâm bước tiếp.")

    return canh_bao