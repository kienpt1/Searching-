from fastapi import FastAPI, File, UploadFile, HTTPException, Query
import pandas as pd 
from createtable import create_table
from addex import address_exists
from insert import insert_address
from delete import delete_all_duplicates
from decimal import Decimal
import mysql.connector
import uvicorn
import io
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')
app = FastAPI()

def connect_to_mysql(host: str = 'localhost', port: int = 3306, user: str = 'root', password: str = 'kien123', database: str = 'address_db_1'):
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        return connection
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"MySQL connection error: {e}")
    
def auto_format_number(number):
    # Convert number to string, but only take the integer part by splitting at the decimal point
    number_str = str(int(number))  # This will remove the decimal part
    
    # Get the length of the number
    length = len(number_str)

    # Define the patterns based on the length of the number
    patterns = {
        4: [1, 3, 2],
        5: [2, 3, 2],
        6: [3, 3, 2],
        7: [1, 3, 3, 2],
        8: [2, 3, 3, 2],
        9: [3, 3, 3, 2],
        10: [1, 3, 3, 3, 2],
        11: [2, 3, 3, 3, 2],
        12: [3, 3, 3, 3, 2],
        13: [1, 3, 3, 3, 3, 2],
        14: [2, 3, 3, 3, 3, 2],
        15: [3, 3, 3, 3, 3, 2],
        16: [1, 3, 3, 3, 3, 3, 2],
    }
    
    # Check if the length of the number matches one of the patterns
    if length not in patterns:
        return "Invalid number"
    
    # Get the pattern for this number
    parts = patterns[length]
    
    # Split the number into parts based on the pattern
    formatted = []
    start = 0
    for part in parts:
        formatted.append(number_str[start:start + part])
        start += part

    # Join the formatted parts with dots
    formatted_number = ".".join(formatted)

    return formatted_number

@app.delete("/Drop_full_table")

async def drop_table():
    mysql_connection = connect_to_mysql()
    cursor = mysql_connection.cursor()
    drop_query = """
        DROP TABLE addresses;
    """
    cursor.execute(drop_query)
    cursor.close()
    mysql_connection.close()
    return {"message": "Table has been dropped."}


@app.post("/insert")

async def upload_file(file: UploadFile = File(...)):
    columns_needed = [0, 1, 2, 3, 5, 7, 8, 9, 19, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 37, 38, 39, 51]
    contents = await file.read()
    df = pd.read_excel(io.BytesIO(contents), header=None, usecols=columns_needed, engine='openpyxl')
    
    df = pd.read_excel("/home/kien/Project/Search/Sl kênh hiện hữu năm 2024 .xlsx", header=None, usecols=columns_needed, engine='openpyxl')

    df.rename(columns={
                        0: "Kenh",
                        1: "ID_dau_vao",
                        2: "Ma_KH_dau_vao",
                        3: "Doi_tac_ban_kenh_dau_vao",
                        5: "HD_dau_vao",
                        7: "Nha_cung_cap",
                        8: "Goi_cuoc",
                        9: "Cuoc_thang",
                        19: "Diem_dau",
                        24: "Diem_cuoi",
                        26: "Chi_nhanh",
                        27: "Chi_nhanh_ky_dau_ra",
                        28: "Don_vi_ky_dau_ra",
                        29: "ID_dau_ra",
                        30: "Ma_KH_dau_ra",
                        31: "Doi_tac_ban_kenh_dau_ra",
                        32: "Ten_KH",
                        33: "Hop_dong_dau_ra",
                        34: "Loai_dich_vu",
                        37: "Dia_Chi",
                        38: "Ngay_nghiem_thu_thuc_te",
                        39: "Trang_thai_thue_bao_dau_ra",
                        51: "Dia_ban"
                    }, inplace=True)
    
    df["Cuoc_thang"] = pd.to_numeric(df["Cuoc_thang"], errors='coerce')  # Convert invalid values to NaN
    df["Cuoc_thang"] = df["Cuoc_thang"].fillna(0)  # Replace NaN values with 0

    max_value = 999999999999
    df["Cuoc_thang"] = df["Cuoc_thang"].apply(lambda x: min(x, max_value))  # Cap values at the max allowed
  
    df["Cuoc_thang"] = df["Cuoc_thang"].apply(lambda x: max(x, 0))  # Ensure that the values are not negative


    
    mysql_connection = connect_to_mysql()
    cursor = mysql_connection.cursor()
    create_table(cursor)
    for _, row in df.iterrows():
       insert_address(
                        row["Kenh"], 
                        row["ID_dau_vao"], 
                        row["Ma_KH_dau_vao"], 
                        row["Doi_tac_ban_kenh_dau_vao"], 
                        row["HD_dau_vao"], 
                        row["Nha_cung_cap"], 
                        row["Goi_cuoc"], 
                        row["Cuoc_thang"], 
                        row["Diem_dau"], 
                        row["Diem_cuoi"], 
                        row["Chi_nhanh"], 
                        row["Chi_nhanh_ky_dau_ra"], 
                        row["Don_vi_ky_dau_ra"],  # Corrected to use the column name as a string
                        row["ID_dau_ra"], 
                        row["Ma_KH_dau_ra"], 
                        row["Doi_tac_ban_kenh_dau_ra"], 
                        row["Ten_KH"], 
                        row["Hop_dong_dau_ra"], 
                        row["Loai_dich_vu"], 
                        row["Dia_Chi"], 
                        row["Ngay_nghiem_thu_thuc_te"], 
                        row["Trang_thai_thue_bao_dau_ra"], 
                        row["Dia_ban"], 
                        cursor, 
                        mysql_connection
                    )

    cursor.close()
    mysql_connection.close()
    return {"message": "Data has been successfully inserted into MySQL."}

@app.delete("/delete-duplicates")

async def remove_duplicates():
    mysql_connection = connect_to_mysql()
    cursor = mysql_connection.cursor()
    
    delete_all_duplicates(cursor, mysql_connection)
    
    cursor.close()
    mysql_connection.close()
    return {"message": "Duplicate records deleted successfully."}

@app.get("/search")

async def search_by_input(
    Truong_thong_tin: str = Query(..., description="Field to match against, e.g., ID_dau_vao, Cuoc_thang, Dia_Chi, Loai_dich_vu"),
    Tu_khoa: str = Query(..., description="Keyword to search for")
):  
    allowed_columns = [
        "Kenh", "ID_dau_vao", "Ma_KH_dau_vao", "Doi_tac_ban_kenh_dau_vao",
        "HD_dau_vao", "Nha_cung_cap", "Goi_cuoc", "Cuoc_thang", "Diem_dau",
        "Diem_cuoi", "Chi_nhanh", "Chi_nhanh_ky_dau_ra", "Don_vi_ky_dau_ra",
        "ID_dau_ra", "Ma_KH_dau_ra", "Doi_tac_ban_kenh_dau_ra", "Ten_KH",
        "Hop_dong_dau_ra", "Loai_dich_vu", "Dia_Chi", "Ngay_nghiem_thu_thuc_te",
        "Trang_thai_thue_bao_dau_ra", "Dia_ban"
    ]

    if Truong_thong_tin not in allowed_columns:
        raise HTTPException(status_code=400, detail=f"Invalid column name: {Truong_thong_tin}")

    mysql_connection = connect_to_mysql()
    cursor = mysql_connection.cursor()

    try:
        if Truong_thong_tin in ["Cuoc_thang", "ID_dau_vao"]:
            # Ensure Tu_khoa is numeric
            if not Tu_khoa.isdigit():
                raise HTTPException(status_code=400, detail=f"{Truong_thong_tin} must be a number")

            query = f"""
                SELECT Kenh, ID_dau_vao, Ma_KH_dau_vao, Doi_tac_ban_kenh_dau_vao,
                       HD_dau_vao, Nha_cung_cap, Goi_cuoc, Cuoc_thang, Diem_dau, Diem_cuoi, Chi_nhanh, 
                       Chi_nhanh_ky_dau_ra, Don_vi_ky_dau_ra, ID_dau_ra, Ma_KH_dau_ra, Doi_tac_ban_kenh_dau_ra, 
                       Ten_KH, Hop_dong_dau_ra, Loai_dich_vu, Dia_Chi, Ngay_nghiem_thu_thuc_te, 
                       Trang_thai_thue_bao_dau_ra, Dia_ban 
                FROM addresses 
                WHERE {Truong_thong_tin} = %s;
            """
            cursor.execute(query, (int(Tu_khoa),))

        else:
            query = f"""
                SELECT Kenh, ID_dau_vao, Ma_KH_dau_vao, Doi_tac_ban_kenh_dau_vao,
                       HD_dau_vao, Nha_cung_cap, Goi_cuoc, Cuoc_thang, Diem_dau, Diem_cuoi, Chi_nhanh, 
                       Chi_nhanh_ky_dau_ra, Don_vi_ky_dau_ra, ID_dau_ra, Ma_KH_dau_ra, Doi_tac_ban_kenh_dau_ra, 
                       Ten_KH, Hop_dong_dau_ra, Loai_dich_vu, Dia_Chi, Ngay_nghiem_thu_thuc_te, 
                       Trang_thai_thue_bao_dau_ra, Dia_ban 
                FROM addresses 
                WHERE {Truong_thong_tin} LIKE %s;
            """
            cursor.execute(query, (f"%{Tu_khoa}%",))

        results = cursor.fetchall()
        # print(results)
        total_bill = Decimal('0')
        list_service = ["IL", "RAC", "LL", "P2P", "TSL", "FH", "KDC", "IPLC", "IPC", "MPLS", "SDWAN", "BW", "EoSDH", "TTB", "DDOS"]
        service_count = {service: 0 for service in list_service}
        rows_list = []
        if results:
            for row in results:
                rows_list.append(row)
                if row[18] in list_service:
                    service_count[row[18]] += 1
                try:
                    total_bill += row[7]
                except Exception:
                    pass  # Skip if conversion fails

            return {
                "results": rows_list,
                "total_bill": str(auto_format_number(total_bill)),
                "service_count": service_count
            }
        else:
            return {"message": f"No records found for {Truong_thong_tin} = {Tu_khoa}"}

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error searching records: {err}")

    finally:
        cursor.close()
        mysql_connection.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
