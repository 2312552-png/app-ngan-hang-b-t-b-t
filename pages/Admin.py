import json
import base64
import requests
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Hệ thống Quản lý Đơn Vay Mua Xe",
    page_icon="📊",
    layout="wide"
)

# Xử lý Đăng nhập Admin
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Đăng nhập Hệ thống Admin")
    password = st.text_input("Mật khẩu truy cập", type="password")
    if st.button("Đăng nhập"):
        admin_pass = st.secrets.get("ADMIN_PASSWORD", "admin123")
        if password == admin_pass:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Mật khẩu không chính xác.")
    st.stop()

st.title("📊 TRUNG TÂM QUẢN LÝ HỒ SƠ VAY MUA XE")

@st.cache_data(ttl=60)
def fetch_submissions_from_github():
    token = st.secrets.get("GITHUB_TOKEN")
    repo = st.secrets.get("GITHUB_REPO")
    url = f"https://api.github.com/repos/{repo}/contents/submissions"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return []

    files = res.json()
    records = []

    for file_info in files:
        if file_info.get("name", "").endswith(".json"):
            file_res = requests.get(file_info["download_url"], headers=headers)
            if file_res.status_code == 200:
                try:
                    records.append(file_res.json())
                except json.JSONDecodeError:
                    continue

    return records

if st.button("🔄 Cập nhật dữ liệu"):
    st.cache_data.clear()
    st.rerun()

data = fetch_submissions_from_github()

if not data:
    st.info("Chưa có hồ sơ nào được ghi nhận trên hệ thống.")
else:
    df = pd.DataFrame(data)

    # 1. Thống kê nhanh
    st.subheader("📈 Thống kê tổng quan")
    col1, col2, col3, col4 = st.columns(4)

    total_loans = len(df)
    total_amount = df["so_tien_vay"].sum() if "so_tien_vay" in df else 0
    avg_income = df["thu_nhap"].mean() if "thu_nhap" in df else 0
    avg_loan = df["so_tien_vay"].mean() if "so_tien_vay" in df else 0

    col1.metric("Tổng số đơn", f"{total_loans} đơn")
    col2.metric("Tổng tiền đề nghị vay", f"{total_amount:,.0f} VNĐ")
    col3.metric("Thu nhập TB", f"{avg_income:,.0f} VNĐ")
    col4.metric("Khoản vay TB", f"{avg_loan:,.0f} VNĐ")

    st.markdown("---")

    # 2. Bộ lọc
    st.subheader("🔍 Lọc & Tìm kiếm")
    col_search, col_filter = st.columns([2, 1])

    with col_search:
        search_query = st.text_input("Tìm kiếm theo Tên / Số CCCD / Số điện thoại")

    with col_filter:
        filter_xe = st.selectbox("Tình trạng xe", ["Tất cả"] + list(df["tinh_trang_xe"].unique()))

    filtered_df = df.copy()

    if search_query:
        q = search_query.lower()
        filtered_df = filtered_df[
            filtered_df["ho_ten"].str.lower().str.contains(q, na=False) |
            filtered_df["so_cccd"].str.contains(q, na=False) |
            filtered_df["so_dien_thoai"].str.contains(q, na=False)
        ]

    if filter_xe != "Tất cả":
        filtered_df = filtered_df[filtered_df["tinh_trang_xe"] == filter_xe]

    # 3. Đổi tên cột hiển thị bảng
    column_mapping = {
        "created_at": "Thời gian tạo",
        "ho_ten": "Họ và tên",
        "so_dien_thoai": "SĐT",
        "so_cccd": "Số CCCD",
        "email": "Email",
        "thu_nhap": "Thu nhập",
        "hang_dong_xe": "Hãng & Dòng xe",
        "gia_tri_xe": "Giá trị xe",
        "so_tien_vay": "Số tiền vay",
        "thoi_gian_vay": "Thời hạn (tháng)",
        "tai_san_dam_bao": "Tài sản đảm bảo"
    }

    display_cols = [c for c in column_mapping.keys() if c in filtered_df.columns]
    display_df = filtered_df[display_cols].rename(columns=column_mapping)

    st.dataframe(display_df, use_container_width=True)

    # 4. Xuất file CSV
    csv_data = filtered_df.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        label="📥 Tải xuống danh sách (CSV)",
        data=csv_data,
        file_name="danh_sach_don_vay_xe.csv",
        mime="text/csv"
    )
