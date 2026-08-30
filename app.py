import re
import json
import base64
import requests
from datetime import date, datetime
import streamlit as st

st.set_page_config(
    page_title="Đăng ký vay vốn mua xe",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 ĐƠN ĐĂNG KÝ VAY VỐN MUA XE")
st.write("Vui lòng điền đầy đủ thông tin đề nghị vay vốn dưới đây.")

TODAY = date.today()
MIN_BIRTH_DATE = TODAY.replace(year=TODAY.year - 100)
MAX_BIRTH_DATE = TODAY.replace(year=TODAY.year - 18)
DEFAULT_BIRTH_DATE = TODAY.replace(year=TODAY.year - 25)

def save_to_github(data):
    try:
        token = st.secrets["GITHUB_TOKEN"]
        repo = st.secrets["GITHUB_REPO"]
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"submissions/don_vay_{timestamp}.json"
        url = f"https://api.github.com/repos/{repo}/contents/{filename}"

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }

        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        content_encoded = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")

        payload = {
            "message": f"Thêm đơn vay từ {data.get('ho_ten')}",
            "content": content_encoded
        }

        res = requests.put(url, headers=headers, json=payload)
        return res.status_code in [200, 201]
    except Exception as e:
        st.error(f"Lỗi kết nối GitHub: {e}")
        return False

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

    if not ho_ten.strip():
        errors.append("Vui lòng nhập Họ và tên.")
    if not dia_chi.strip():
        errors.append("Vui lòng nhập Địa chỉ hiện tại.")
    if not hang_dong_xe.strip():
        errors.append("Vui lòng nhập Hãng xe & Dòng xe.")

    if not so_cccd.strip():
        errors.append("Vui lòng nhập Số CCCD/Hộ chiếu.")
    elif so_cccd.isdigit() and len(so_cccd) not in (9, 12):
        errors.append("Số CCCD/CMND phải gồm 9 hoặc 12 chữ số.")

    if not so_dien_thoai.strip():
        errors.append("Vui lòng nhập Số điện thoại.")
    elif not re.fullmatch(r"0\d{9}", so_dien_thoai.strip()):
        errors.append("Số điện thoại không hợp lệ (phải gồm 10 chữ số, bắt đầu bằng 0).")

    if email.strip() and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()):
        errors.append("Email không hợp lệ.")

    if thu_nhap <= 0:
        errors.append("Thu nhập hàng tháng phải lớn hơn 0.")
    if gia_tri_xe <= 0:
        errors.append("Giá trị xe phải lớn hơn 0.")
    if so_tien_vay <= 0:
        errors.append("Số tiền đề nghị vay phải lớn hơn 0.")

    if gia_tri_xe > 0 and so_tien_vay > 0:
        if so_tien_vay > gia_tri_xe:
            errors.append("Số tiền đề nghị vay không được vượt quá giá trị xe.")
        elif so_tien_vay > 0.8 * gia_tri_xe:
            errors.append("Số tiền đề nghị vay không được vượt quá 80% giá trị xe.")

    if errors:
        for err in errors:
            st.error(err)
    else:
        record = {
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ho_ten": ho_ten.strip(),
            "ngay_sinh": ngay_sinh.strftime("%Y-%m-%d"),
            "gioi_tinh": gioi_tinh,
            "so_cccd": so_cccd.strip(),
            "so_dien_thoai": so_dien_thoai.strip(),
            "email": email.strip(),
            "tin_trang_hon_nhan": tin_trang_hon_nhan,
            "dia_chi": dia_chi.strip(),
            "ten_cong_ty": ten_cong_ty.strip(),
            "chuc_vu": chuc_vu.strip(),
            "thu_nhap": thu_nhap,
            "chi_phi": chi_phi,
            "tinh_trang_xe": tinh_trang_xe,
            "hang_dong_xe": hang_dong_xe.strip(),
            "gia_tri_xe": gia_tri_xe,
            "muc_dich": muc_dich,
            "so_tien_vay": so_tien_vay,
            "thoi_gian_vay": thoi_gian_vay,
            "tai_san_dam_bao": tai_san_dam_bao
        }

        if save_to_github(record):
            st.success("Gửi hồ sơ đăng ký vay thành công! Hệ thống đã lưu dữ liệu.")
        else:
            st.warning("Đơn đăng ký được gửi nhưng không thể lưu tự động lên GitHub. Vui lòng liên hệ hỗ trợ.")
