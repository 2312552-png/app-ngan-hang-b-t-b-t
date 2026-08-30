import pandas as pd
import streamlit as st
from database import get_connection

st.set_page_config(
    page_title="Quản lý hồ sơ vay mua xe",
    page_icon="🚗",
    layout="wide"
)

# Khởi tạo session state duy trì đăng nhập
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

# Giao diện bảng điều khiển sau khi đăng nhập thành công
else:
    # Nút đăng xuất ở thanh bên
    with st.sidebar:
        st.write(f"👋 **Xin chào, {USERNAME}**")
        if st.button("Đăng xuất"):
            st.session_state.logged_in = False
            st.rerun()

    st.title("🚗 QUẢN LÝ HỒ SƠ ĐĂNG KÝ VAY VỐN MUA XE")

    try:
        conn = get_connection()
        
        # Bảng dữ liệu lưu thông tin đăng ký vay mua xe
        sql = """
        SELECT *
        FROM dangky_vay_mua_xe
        ORDER BY id DESC
        """
        df = pd.read_sql(sql, conn)
        conn.close()

        st.subheader("📋 Danh sách hồ sơ đề nghị vay")

        if df.empty:
            st.info("Chưa có hồ sơ đăng ký nào trong hệ thống.")
        else:
            # Tự động định dạng lại các cột tiền tệ và ngày tháng hiển thị
            st.dataframe(
                df,
                use_container_width=True,
                column_config={
                    "thu_nhap": st.column_config.NumberColumn("Thu nhập (VNĐ)", format="%d VNĐ"),
                    "chi_phi": st.column_config.NumberColumn("Chi phí (VNĐ)", format="%d VNĐ"),
                    "gia_tri_xe": st.column_config.NumberColumn("Giá trị xe (VNĐ)", format="%d VNĐ"),
                    "so_tien_vay": st.column_config.NumberColumn("Số tiền vay (VNĐ)", format="%d VNĐ"),
                    "ngay_sinh": st.column_config.DateColumn("Ngày sinh", format="DD/MM/YYYY"),
                    "created_at": st.column_config.DatetimeColumn("Thời gian gửi", format="DD/MM/YYYY HH:mm")
                }
            )
            
    except Exception as e:
        st.error(f"Lỗi kết nối cơ sở dữ liệu: {e}")
