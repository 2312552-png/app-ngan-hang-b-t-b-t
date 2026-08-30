CREATE DATABASE company1
USE company1;
CREATE TABLE vay_von_nganhang_butbut (
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Thông tin cá nhân (Người vay)
    ho_ten VARCHAR(100) NOT NULL,
    ngay_sinh DATE,
    gioi_tinh VARCHAR(10),
    so_cccd VARCHAR(20) NOT NULL,
    ngay_cap_cccd DATE,
    noi_cap_cccd VARCHAR(100),
    dia_chi_thuong_tru VARCHAR(255),
    dia_chi_tam_tru VARCHAR(255),
    so_dien_thoai VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    tinh_trang_hon_nhan VARCHAR(50),
    
    -- Thông tin công việc
    ten_cong_ty VARCHAR(150),
    dia_chi_cong_ty VARCHAR(255),
    chuc_vu VARCHAR(100),
    loai_hop_dong_lao_dong VARCHAR(100),
    thoi_gian_cong_tac VARCHAR(50),
    
    -- Thông tin tài chính & Thu nhập
    nguon_thu_nhap_chinh VARCHAR(100),
    tong_thu_nhap_hang_thang DECIMAL(15, 2),
    chi_phi_sinh_hoat_hang_thang DECIMAL(15, 2),
    nghia_vu_tai_chinh_hien_tai TEXT,
    
    -- Thông tin xe dự định mua
    tinh_trang_xe VARCHAR(50), -- Xe mới 100% / Xe đã qua sử dụng
    hang_xe VARCHAR(50),
    dong_xe VARCHAR(50),
    nam_san_xuat INT,
    dung_tich_xilanh VARCHAR(50),
    gia_tri_xe DECIMAL(15, 2),
    muc_dich_su_dung_xe VARCHAR(100),
    
    -- Thông tin khoản vay đề xuất
    so_tien_vay_de_nghi DECIMAL(15, 2),
    thoi_gian_vay_thang INT,
    tai_san_bao_dam TEXT,
    
    -- Thông tin người hôn phối / Người đồng vay (nếu có)
    ho_ten_nguoi_dong_vay VARCHAR(100),
    so_cccd_nguoi_dong_vay VARCHAR(20),
    sdt_nguoi_dong_vay VARCHAR(20),
    thu_nhap_nguoi_dong_vay DECIMAL(15, 2),
    
    -- Thời gian
    ngay_vay_von TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);