from fastapi import FastAPI, File, UploadFile, HTTPException, Query
import pandas as pd 
from createtable import create_table
from decimal import Decimal
import mysql.connector
import uvicorn
import io
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')
def delete_all_duplicates(cursor, mydb):
    delete_query = """
        DELETE a
        FROM addresses a
        JOIN (
            SELECT MIN(id) AS keep_id, Kenh, ID_dau_vao, Ma_KH_dau_vao, Doi_tac_ban_kenh_dau_vao, HD_dau_vao,
                   Nha_cung_cap, Goi_cuoc, Cuoc_thang, Diem_dau, Diem_cuoi, Chi_nhanh, Chi_nhanh_ky_dau_ra,Don_vi_ky_dau_ra,
                   ID_dau_ra, Ma_KH_dau_ra, Doi_tac_ban_kenh_dau_ra, Ten_KH, Hop_dong_dau_ra,
                   Loai_dich_vu, Dia_Chi, Ngay_nghiem_thu_thuc_te, Trang_thai_thue_bao_dau_ra, Dia_ban
            FROM addresses
            GROUP BY Kenh, ID_dau_vao, Ma_KH_dau_vao, Doi_tac_ban_kenh_dau_vao, HD_dau_vao,
                     Nha_cung_cap, Goi_cuoc, Cuoc_thang, Diem_dau, Diem_cuoi, Chi_nhanh, Chi_nhanh_ky_dau_ra,Don_vi_ky_dau_ra,
                     ID_dau_ra, Ma_KH_dau_ra, Doi_tac_ban_kenh_dau_ra, Ten_KH, Hop_dong_dau_ra,
                     Loai_dich_vu, Dia_Chi, Ngay_nghiem_thu_thuc_te, Trang_thai_thue_bao_dau_ra, Dia_ban
        ) b ON a.Kenh = b.Kenh 
             AND a.ID_dau_vao = b.ID_dau_vao 
             AND a.Ma_KH_dau_vao = b.Ma_KH_dau_vao
             AND a.Doi_tac_ban_kenh_dau_vao = b.Doi_tac_ban_kenh_dau_vao
             AND a.HD_dau_vao = b.HD_dau_vao
             AND a.Nha_cung_cap = b.Nha_cung_cap
             AND a.Goi_cuoc = b.Goi_cuoc
             AND a.Cuoc_thang = b.Cuoc_thang
             AND a.Diem_dau = b.Diem_dau
             AND a.Diem_cuoi = b.Diem_cuoi
             AND a.Chi_nhanh = b.Chi_nhanh
             AND a.Chi_nhanh_ky_dau_ra = b.Chi_nhanh_ky_dau_ra
             AND a.Don_vi_ky_dau_ra = b.Don_vi_ky_dau_ra
             AND a.ID_dau_ra = b.ID_dau_ra
             AND a.Ma_KH_dau_ra = b.Ma_KH_dau_ra
             AND a.Doi_tac_ban_kenh_dau_ra = b.Doi_tac_ban_kenh_dau_ra
             AND a.Ten_KH = b.Ten_KH
             AND a.Hop_dong_dau_ra = b.Hop_dong_dau_ra
             AND a.Loai_dich_vu = b.Loai_dich_vu
             AND a.Dia_Chi = b.Dia_Chi
             AND a.Ngay_nghiem_thu_thuc_te = b.Ngay_nghiem_thu_thuc_te
             AND a.Trang_thai_thue_bao_dau_ra = b.Trang_thai_thue_bao_dau_ra
             AND a.Dia_ban = b.Dia_ban
        WHERE a.id > b.keep_id;
    """
    
    cursor.execute(delete_query)
    mydb.commit()
    print("Duplicate records deleted.")
