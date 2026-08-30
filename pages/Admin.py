import pandas as pd
import streamlit as st
from database import get_connection

st.set_page_config(page_title="Quản trị - Vay vốn mua xe", page_icon="🔐")

st.title("🔐 QUẢN TRỊ HỒ SƠ VAY VỐN MUA XE")

# --------------------------
# Tài khoản quản trị
# --------------------------
USERNAME = "admin"
PASSWORD = "123456"

# --------------------------
# Đăng nhập
# --------------------------
username = st.text_input("Tên đăng nhập")
password = st.text_input("Mật khẩu", type="password")
login = st.button("Đăng nhập")

# --------------------------
# Kiểm tra đăng nhập & Hiển thị dữ liệu
# --------------------------
if login:
    if username == USERNAME and password == PASSWORD:
        st.success("Đăng nhập thành công!")

        conn = get_connection()

        # Truy vấn dữ liệu từ bảng đăng ký vay xe thay vì đăng ký du lịch
        sql = """
        SELECT *
        FROM dangky_vay_xe
        ORDER BY id DESC
        """

        df = pd.read_sql(sql, conn)
        conn.close()

        st.subheader("📋 Danh sách hồ sơ đăng ký vay vốn")

        st.dataframe(df, use_container_width=True)

    else:
        st.error("Sai tên đăng nhập hoặc mật khẩu.")
