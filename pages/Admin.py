import pandas as pd
import streamlit as st
from database import get_connection

st.set_page_config(
    page_title="Trang quản trị - Hồ sơ vay mua xe",
    page_icon="🚗",
    layout="wide"
)

# Khởi tạo session state duy trì trạng thái đăng nhập
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Tài khoản quản trị
USERNAME = "admin"
PASSWORD = "123456"

# Giao diện khi chưa đăng nhập
if not st.session_state.logged_in:
    st.title("🔐 ĐĂNG NHẬP QUẢN TRỊ VAY MUA XE")
    
    with st.form("login_form"):
        username = st.text_input("Tên đăng nhập")
        password = st.text_input("Mật khẩu", type="password")
        login_btn = st.form_submit_button("Đăng nhập")

        if login_btn:
            if username == USERNAME and password == PASSWORD:
                st.session_state.logged_in = True
                st.success("Đăng nhập thành công!")
                st.rerun()
            else:
                st.error("Sai tên đăng nhập hoặc mật khẩu.")

# Giao diện sau khi đăng nhập thành công
else:
    # Thanh điều hướng sidebar
    with st.sidebar:
        st.write(f"👋 **Xin chào, {USERNAME}**")
        if st.button("Đăng xuất"):
            st.session_state.logged_in = False
            st.rerun()

    st.title("🚗 QUẢN LÝ HỒ SƠ ĐĂNG KÝ VAY VỐN MUA XE")

    try:
        conn = get_connection()
        
        # Truy vấn lấy dữ liệu từ bảng vay_von_nganhang_butbut
        sql = """
        SELECT *
        FROM vay_von_nganhang_butbut
        ORDER BY id DESC
        """
        df = pd.read_sql(sql, conn)
        conn.close()

        if df.empty:
            st.info("Chưa có hồ sơ đăng ký nào trong hệ thống.")
        else:
            # Thống kê tổng quan nhanh
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Tổng số hồ sơ tiếp nhận", len(df))
            with col2:
                tong_tien = df["so_tien_vay_de_nghi"].sum() if "so_tien_vay_de_nghi" in df.columns else 0
                st.metric("Tổng nhu cầu tiền vay đề nghị", f"{tong_tien:,.0f} VNĐ")

            st.subheader("📋 Danh sách chi tiết hồ sơ")

            # Định dạng các cột hiển thị trong bảng
            st.dataframe(
                df,
                use_container_width=True,
                column_config={
                    "id": "ID",
                    "ho_ten": "Họ và tên",
                    "ngay_sinh": st.column_config.DateColumn("Ngày sinh", format="DD/MM/YYYY"),
                    "ngay_cap_cccd": st.column_config.DateColumn("Ngày cấp CCCD", format="DD/MM/YYYY"),
                    "tong_thu_nhap_hang_thang": st.column_config.NumberColumn("Tổng thu nhập (VNĐ)", format="%d VNĐ"),
                    "chi_phi_sinh_hoat_hang_thang": st.column_config.NumberColumn("Chi phí sinh hoạt (VNĐ)", format="%d VNĐ"),
                    "gia_tri_xe": st.column_config.NumberColumn("Giá trị xe (VNĐ)", format="%d VNĐ"),
                    "so_tien_vay_de_nghi": st.column_config.NumberColumn("Tiền vay đề nghị (VNĐ)", format="%d VNĐ"),
                    "thoi_gian_vay_thang": st.column_config.NumberColumn("Thời gian vay (Tháng)", format="%d tháng"),
                    "thu_nhap_nguoi_dong_vay": st.column_config.NumberColumn("Thu nhập người đồng vay (VNĐ)", format="%d VNĐ"),
                    "ngay_vay_von": st.column_config.DatetimeColumn("Thời gian đăng ký", format="DD/MM/YYYY HH:mm")
                }
            )

    except Exception as e:
        st.error(f"Lỗi kết nối cơ sở dữ liệu: {e}")
