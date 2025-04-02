from createtable import create_table
import mysql.connector
import sys

sys.stdout.reconfigure(encoding='utf-8')

def insert_address(Kenh, ID_dau_vao, Ma_KH_dau_vao, Doi_tac_ban_kenh_dau_vao, HD_dau_vao,
                   Nha_cung_cap, Goi_cuoc, Cuoc_thang, Diem_dau, Diem_cuoi, Chi_nhanh, Chi_nhanh_ky_dau_ra,
                   Don_vi_ky_dau_ra, ID_dau_ra, Ma_KH_dau_ra, Doi_tac_ban_kenh_dau_ra, Ten_KH, Hop_dong_dau_ra,
                   Loai_dich_vu, Dia_Chi, Ngay_nghiem_thu_thuc_te, Trang_thai_thue_bao_dau_ra,
                   Dia_ban, cursor, mydb):
    print(Don_vi_ky_dau_ra)
    # Convert None values to empty strings to prevent errors
    def sanitize(value):
        return str(value).strip() if value is not None else ""

    Kenh = sanitize(Kenh)
    ID_dau_vao = sanitize(ID_dau_vao)
    Ma_KH_dau_vao = sanitize(Ma_KH_dau_vao)
    Doi_tac_ban_kenh_dau_vao = sanitize(Doi_tac_ban_kenh_dau_vao)
    HD_dau_vao = sanitize(HD_dau_vao)
    Nha_cung_cap = sanitize(Nha_cung_cap)
    Goi_cuoc = sanitize(Goi_cuoc)
    Cuoc_thang = sanitize(Cuoc_thang)
    Diem_dau = sanitize(Diem_dau)
    Diem_cuoi = sanitize(Diem_cuoi)
    Chi_nhanh = sanitize(Chi_nhanh)
    Chi_nhanh_ky_dau_ra = sanitize(Chi_nhanh_ky_dau_ra)
    Don_vi_ky_dau_ra= sanitize(Don_vi_ky_dau_ra)
    ID_dau_ra = sanitize(ID_dau_ra)
    Ma_KH_dau_ra = sanitize(Ma_KH_dau_ra)
    Doi_tac_ban_kenh_dau_ra = sanitize(Doi_tac_ban_kenh_dau_ra)
    Ten_KH = sanitize(Ten_KH)
    Hop_dong_dau_ra = sanitize(Hop_dong_dau_ra)
    Loai_dich_vu = sanitize(Loai_dich_vu)
    Dia_Chi = sanitize(Dia_Chi)
    Ngay_nghiem_thu_thuc_te = sanitize(Ngay_nghiem_thu_thuc_te)
    Trang_thai_thue_bao_dau_ra = sanitize(Trang_thai_thue_bao_dau_ra)
    Dia_ban = sanitize(Dia_ban)

    try:
        sql = """
                INSERT INTO addresses (
                    Kenh,
                    ID_dau_vao,
                    Ma_KH_dau_vao,
                    Doi_tac_ban_kenh_dau_vao,
                    HD_dau_vao,
                    Nha_cung_cap,
                    Goi_cuoc,
                    Cuoc_thang,
                    Diem_dau,
                    Diem_cuoi,
                    Chi_nhanh,
                    Chi_nhanh_ky_dau_ra,
                    Don_vi_ky_dau_ra,
                    ID_dau_ra,
                    Ma_KH_dau_ra,
                    Doi_tac_ban_kenh_dau_ra,
                    Ten_KH,
                    Hop_dong_dau_ra,
                    Loai_dich_vu,
                    Dia_Chi,
                    Ngay_nghiem_thu_thuc_te,
                    Trang_thai_thue_bao_dau_ra,
                    Dia_ban
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """
        

        values = (Kenh, ID_dau_vao, Ma_KH_dau_vao, Doi_tac_ban_kenh_dau_vao, HD_dau_vao,
                  Nha_cung_cap, Goi_cuoc, Cuoc_thang, Diem_dau, Diem_cuoi, Chi_nhanh, Chi_nhanh_ky_dau_ra,
                  Don_vi_ky_dau_ra,ID_dau_ra, Ma_KH_dau_ra, Doi_tac_ban_kenh_dau_ra, Ten_KH, Hop_dong_dau_ra,
                  Loai_dich_vu, Dia_Chi, Ngay_nghiem_thu_thuc_te, Trang_thai_thue_bao_dau_ra,
                  Dia_ban)

        cursor.execute(sql, values)
        mydb.commit()
        print(f"✅ Inserted/Updated ID_dau_vao: {ID_dau_vao}")

    except mysql.connector.Error as err:
        print(f"❌ Error inserting data: {err}")