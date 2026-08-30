import re
from datetime import date, timedelta
import streamlit as st
st.set_page_config(
    page_title="Đăng ký vay vốn mua xe",
    page_icon="🚗",
    layout="centered"
)
# CHÈN VÀO ĐÂY (Ngay trên tiêu đề):
st.image("logo.jpg")

st.title("🚗 ĐƠN ĐĂNG KÝ VAY VỐN MUA XE")
st.write("Vui lòng điền đầy đủ thông tin đề nghị vay vốn dưới đây.")

TODAY = date.today()
MIN_BIRTH_DATE = TODAY.replace(year=TODAY.year - 100)  # giới hạn 100 tuổi
MAX_BIRTH_DATE = TODAY.replace(year=TODAY.year - 18)   # phải đủ 18 tuổi
DEFAULT_BIRTH_DATE = TODAY.replace(year=TODAY.year - 25)

with st.form("form_vay_mua_xe"):

    # 1. Thông tin cá nhân
    st.subheader("1. Thông tin cá nhân")
    ho_ten = st.text_input("Họ và tên *")

    col1, col2 = st.columns(2)
    with col1:
        ngay_sinh = st.date_input(
            "Ngày sinh *",
            value=DEFAULT_BIRTH_DATE,
            min_value=MIN_BIRTH_DATE,
            max_value=MAX_BIRTH_DATE,
            format="DD/MM/YYYY"
        )
        gioi_tinh = st.radio("Giới tính", ["Nam", "Nữ"], horizontal=True)
        so_cccd = st.text_input("Số CCCD/Hộ chiếu *")
    with col2:
        so_dien_thoai = st.text_input("Số điện thoại *")
        email = st.text_input("Email")
        tin_trang_hon_nhan = st.selectbox(
            "Tình trạng hôn nhân",
            ["Độc thân", "Đã kết hôn", "Đã ly hôn"]
        )

    dia_chi = st.text_area("Địa chỉ hiện tại *", height=80)

    # 2. Công việc & Thu nhập
    st.subheader("2. Thông tin công việc & Thu nhập")
    col3, col4 = st.columns(2)
    with col3:
        ten_cong_ty = st.text_input("Tên cơ quan/Công ty")
        chuc_vu = st.text_input("Vị trí/Chức vụ")
    with col4:
        thu_nhap = st.number_input("Thu nhập hàng tháng (VNĐ) *", min_value=0, step=1000000, format="%d")
        chi_phi = st.number_input("Chi phí sinh hoạt hàng tháng (VNĐ)", min_value=0, step=1000000, format="%d")

    # 3. Thông tin xe dự định mua
    st.subheader("3. Thông tin xe dự định mua")
    col5, col6 = st.columns(2)
    with col5:
        tinh_trang_xe = st.selectbox("Tình trạng xe", ["Xe mới 100%", "Xe đã qua sử dụng"])
        hang_dong_xe = st.text_input("Hãng xe & Dòng xe (ví dụ: Toyota Camry) *")
    with col6:
        gia_tri_xe = st.number_input("Giá trị xe theo hợp đồng/báo giá (VNĐ) *", min_value=0, step=10000000, format="%d")
        muc_dich = st.selectbox("Mục đích sử dụng", ["Cá nhân / Gia đình", "Kinh doanh vận tải / Cho thuê"])

    # 4. Nhu cầu khoản vay
    st.subheader("4. Thông tin khoản vay đề xuất")
    col7, col8 = st.columns(2)
    with col7:
        so_tien_vay = st.number_input("Số tiền đề nghị vay (VNĐ) *", min_value=0, step=10000000, format="%d")
        thoi_gian_vay = st.selectbox("Thời gian vay (tháng)", [12, 24, 36, 48, 60, 72, 84], index=4)
    with col8:
        tai_san_dam_bao = st.selectbox(
            "Tài sản bảo đảm",
            ["Chính chiếc xe dự định mua", "Bất động sản", "Sổ tiết kiệm", "Tài sản khác"]
        )

    submit = st.form_submit_button("Gửi đơn đăng ký vay")

if submit:
    errors = []

    # Bắt buộc nhập
    if not ho_ten.strip():
        errors.append("Vui lòng nhập Họ và tên.")
    if not dia_chi.strip():
        errors.append("Vui lòng nhập Địa chỉ hiện tại.")
    if not hang_dong_xe.strip():
        errors.append("Vui lòng nhập Hãng xe & Dòng xe.")

    # Validate CCCD: 9 hoặc 12 chữ số (CCCD/CMND) — không ràng buộc hộ chiếu vì đa dạng ký tự
    if not so_cccd.strip():
        errors.append("Vui lòng nhập Số CCCD/Hộ chiếu.")
    elif so_cccd.isdigit() and len(so_cccd) not in (9, 12):
        errors.append("Số CCCD/CMND phải gồm 9 hoặc 12 chữ số.")

    # Validate số điện thoại Việt Nam: 10 số, bắt đầu bằng 0
    if not so_dien_thoai.strip():
        errors.append("Vui lòng nhập Số điện thoại.")
    elif not re.fullmatch(r"0\d{9}", so_dien_thoai.strip()):
        errors.append("Số điện thoại không hợp lệ (phải gồm 10 chữ số, bắt đầu bằng 0).")

    # Validate email nếu có nhập
    if email.strip() and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()):
        errors.append("Email không hợp lệ.")

    # Validate thu nhập, giá trị xe, số tiền vay phải > 0
    if thu_nhap <= 0:
        errors.append("Thu nhập hàng tháng phải lớn hơn 0.")
    if gia_tri_xe <= 0:
        errors.append("Giá trị xe phải lớn hơn 0.")
    if so_tien_vay <= 0:
        errors.append("Số tiền đề nghị vay phải lớn hơn 0.")

    # Validate số tiền vay không vượt quá giá trị xe (và tối đa 80% giá trị xe)
    if gia_tri_xe > 0 and so_tien_vay > 0:
        if so_tien_vay > gia_tri_xe:
            errors.append("Số tiền đề nghị vay không được vượt quá giá trị xe.")
        elif so_tien_vay > 0.8 * gia_tri_xe:
            errors.append("Số tiền đề nghị vay không được vượt quá 80% giá trị xe.")

    if errors:
        for err in errors:
            st.error(err)
    else:
        st.success("Gửi hồ sơ đăng ký vay thành công! Nhân viên sẽ sớm liên hệ lại với bạn.")

        st.write("### Thông tin hồ sơ đã đăng ký")

        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**Họ tên:**", ho_ten)
            st.write("**Ngày sinh:**", ngay_sinh.strftime("%d/%m/%Y"))
            st.write("**Số CCCD:**", so_cccd)
            st.write("**Số điện thoại:**", so_dien_thoai)
            st.write("**Địa chỉ:**", dia_chi)
            st.write("**Thu nhập hàng tháng:**", f"{thu_nhap:,.0f} VNĐ")

        with col_b:
            st.write("**Loại xe:**", f"{tinh_trang_xe} - {hang_dong_xe}")
            st.write("**Giá trị xe:**", f"{gia_tri_xe:,.0f} VNĐ")
            st.write("**Số tiền vay đề xuất:**", f"{so_tien_vay:,.0f} VNĐ")
            st.write("**Thời hạn vay:**", f"{thoi_gian_vay} tháng")
            st.write("**Tài sản bảo đảm:**", tai_san_dam_bao)
            st.write("**Mục đích:**", muc_dich)
