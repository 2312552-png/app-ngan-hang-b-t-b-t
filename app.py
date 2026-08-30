import streamlit as st

st.set_page_config(
    page_title="Đăng ký vay vốn mua xe",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 ĐƠN ĐĂNG KÝ VAY VỐN MUA XE")
st.write("Vui lòng điền đầy đủ thông tin đề nghị vay vốn dưới đây.")

with st.form("form_vay_mua_xe"):

    # 1. Thông tin cá nhân
    st.subheader("1. Thông tin cá nhân")
    ho_ten = st.text_input("Họ và tên *")
    
    col1, col2 = st.columns(2)
    with col1:
        ngay_sinh = st.date_input("Ngày sinh", format="DD/MM/YYYY")
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
        thu_nhap = st.number_input("Thu nhập hàng tháng (VNĐ)", min_value=0, step=1000000, format="%d")
        chi_phi = st.number_input("Chi phí sinh hoạt hàng tháng (VNĐ)", min_value=0, step=1000000, format="%d")

    # 3. Thông tin khoản vay
    st.subheader("3. Thông tin khoản vay")
    so_tien_vay = st.number_input("Số tiền muốn vay (VNĐ)", min_value=0, step=10000000, format="%d")
    thoi_gian_vay = st.slider("Thời hạn vay (tháng)", min_value=6, max_value=84, value=36, step=6)

    submitted = st.form_submit_button("Gửi đơn đăng ký")
    if submitted:
        if not ho_ten or not so_cccd or not so_dien_thoai or not dia_chi:
            st.error("Vui lòng điền đầy đủ các thông tin bắt buộc (*)")
        else:
            st.success("Đăng ký thành công! Chúng tôi sẽ liên hệ với bạn sớm nhất.")
 giờ muốn nhét hình ảnh vào dòng nào
