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

def address_exists(Kenh, ID_dau_vao, Ma_KH_dau_vao, Doi_tac_ban_kenh_dau_vao, HD_dau_vao, 
                   Nha_cung_cap, Goi_cuoc, Cuoc_thang, Diem_dau, Diem_cuoi, Chi_nhanh, 
                   Chi_nhanh_ky_dau_ra, Don_vi_ky_dau_ra, ID_dau_ra, Ma_KH_dau_ra, Doi_tac_ban_kenh_dau_ra, 
                   Ten_KH, Hop_dong_dau_ra, Loai_dich_vu, Dia_Chi, Ngay_nghiem_thu_thuc_te, 
                   Trang_thai_thue_bao_dau_ra, Dia_ban, cursor):
    query = """
            SELECT COUNT(*) FROM addresses WHERE 
                Kenh = %s AND 
                ID_dau_vao = %s AND 
                Ma_KH_dau_vao = %s AND 
                Doi_tac_ban_kenh_dau_vao = %s AND 
                HD_dau_vao = %s AND 
                Nha_cung_cap = %s AND 
                Goi_cuoc = %s AND 
                Cuoc_thang = %s AND 
                Diem_dau = %s AND 
                Diem_cuoi = %s AND 
                Chi_nhanh = %s AND 
                Chi_nhanh_ky_dau_ra = %s AND 
                Don_vi_ky_dau_ra = %s AND
                ID_dau_ra = %s AND 
                Ma_KH_dau_ra = %s AND 
                Doi_tac_ban_kenh_dau_ra = %s AND 
                Ten_KH = %s AND 
                Hop_dong_dau_ra = %s AND 
                Loai_dich_vu = %s AND 
                Dia_Chi = %s AND 
                Ngay_nghiem_thu_thuc_te = %s AND 
                Trang_thai_thue_bao_dau_ra = %s AND 
                Dia_ban = %s
            """
    
    # Execute the query with the parameters passed to the function
    cursor.execute(query, (Kenh, ID_dau_vao, Ma_KH_dau_vao, Doi_tac_ban_kenh_dau_vao, HD_dau_vao,
                           Nha_cung_cap, Goi_cuoc, Cuoc_thang, Diem_dau, Diem_cuoi, Chi_nhanh,
                           Chi_nhanh_ky_dau_ra, Don_vi_ky_dau_ra , ID_dau_ra, Ma_KH_dau_ra, Doi_tac_ban_kenh_dau_ra,
                           Ten_KH, Hop_dong_dau_ra, Loai_dich_vu, Dia_Chi, Ngay_nghiem_thu_thuc_te,
                           Trang_thai_thue_bao_dau_ra, Dia_ban))
    
    # Fetch the result of the query (count of matching records)
    count = cursor.fetchone()[0]
    
    # Return True if the address exists, False otherwise
    return count > 0