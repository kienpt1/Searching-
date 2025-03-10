from fastapi import FastAPI, File, UploadFile, HTTPException, Query
import pandas as pd 
from createtable import create_table
from decimal import Decimal
import mysql.connector
import uvicorn
import io
import sys
sys.stdout.reconfigure(encoding='utf-8')
app = FastAPI()

def connect_to_mysql(host: str = 'localhost', port: int = 3306, user: str = 'root', password: str = 'kien123', database: str = 'address_db'):
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
    
def create_table(cursor):
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `addresses` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `dia_chi` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            `loai_dich_vu` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            `cuoc_thang` DECIMAL(15, 2),
            `id_dau_vao` INT
        )
        """)
        print("Table 'addresses' created successfully or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

def address_exists(dia_chi, loai_dich_vu, cursor):
    query = "SELECT COUNT(*) FROM addresses WHERE dia_chi = %s AND loai_dich_vu = %s"
    cursor.execute(query, (dia_chi, loai_dich_vu))
    count = cursor.fetchone()[0]
    return count > 0  # Return True if exists, False otherwise


def insert_address(dia_chi, loai_dich_vu, cuoc_thang, id_dau_vao, cursor, mydb):
    try:
        # Check if record already exists
        if address_exists(dia_chi, loai_dich_vu, cursor):
            print(f"Skipping duplicate entry: {dia_chi}, {loai_dich_vu}")
            return
        
        sql = """INSERT INTO addresses (dia_chi, loai_dich_vu, cuoc_thang, id_dau_vao) 
                 VALUES (%s, %s, %s, %s)"""
        values = (dia_chi, loai_dich_vu, cuoc_thang, id_dau_vao)

        cursor.execute(sql, values)
        mydb.commit()
        print(f"Inserted ID: {cursor.lastrowid}")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")

def delete_all_duplicates(cursor, mydb):
    delete_query = """
        DELETE a
        FROM addresses a
        JOIN (
            SELECT MIN(id) AS keep_id, dia_chi, loai_dich_vu, id_dau_vao, cuoc_thang
            FROM addresses
            GROUP BY dia_chi, loai_dich_vu, id_dau_vao , cuoc_thang
        ) b ON a.dia_chi = b.dia_chi 
             AND a.loai_dich_vu = b.loai_dich_vu 
             AND a.id_dau_vao = b.id_dau_vao
             AND a.cuoc_thang = b.cuoc_thang
        WHERE a.id > b.keep_id;
    """
    
    cursor.execute(delete_query)
    mydb.commit()
    print("Duplicate records deleted.")


@app.post("/insert")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    # df = pd.read_excel(io.BytesIO(contents))
    # print(f"Data read from Excel: {df}")
    # # Data Cleaning
    # df["Cước tháng"] = pd.to_numeric(df["Cước tháng"], errors='coerce').fillna(0)
    # df["Cước tháng"] = df["Cước tháng"].apply(lambda x: max(min(x, 999999999999.99), 0))
    df = pd.read_excel(io.BytesIO(contents))
    
    df = pd.read_excel("Sl kênh hiện hữu năm 2024.xlsx")

    # Clean 'Cước tháng' column to ensure valid numbers and replace NaN with a default value (0 or any valid value)
    df["Cước tháng"] = pd.to_numeric(df["Cước tháng"], errors='coerce')  # Convert invalid values to NaN
    df["Cước tháng"] = df["Cước tháng"].fillna(0)  # Replace NaN values with 0

    # Cap 'Cước tháng' values that exceed a reasonable value, e.g., 999999999999.99 (DECIMAL(15, 2))
    max_value = 999999999999.99
    df["Cước tháng"] = df["Cước tháng"].apply(lambda x: min(x, max_value))  # Cap values at the max allowed

    # Ensure that no negative values exist in 'Cước tháng'
    df["Cước tháng"] = df["Cước tháng"].apply(lambda x: max(x, 0))  # Ensure that the values are not negative


    
    mysql_connection = connect_to_mysql()
    cursor = mysql_connection.cursor()
    create_table(cursor)
    for _, row in df.iterrows():
        insert_address(row['Địa chỉ'], row['Loại dịch vụ'], row['Cước tháng'], row.get('ID đầu vào', None), cursor, mysql_connection)
    
    cursor.close()
    mysql_connection.close()
    return {"message": "Data has been successfully inserted into MySQL."}

@app.delete("/delete-duplicates")
def remove_duplicates():
    mysql_connection = connect_to_mysql()
    cursor = mysql_connection.cursor()
    
    delete_all_duplicates(cursor, mysql_connection)
    
    cursor.close()
    mysql_connection.close()
    return {"message": "Duplicate records deleted successfully."}

@app.get("/search")
def search_by_input(
    # thong_tin_can_tim: str = Query(..., description="Fields to search for, e.g., id_dau_vao, cuoc_thang, dia_chi"),
    Truong_thong_tin: str = Query(..., description="Field to match against, e.g., id_dau_vao, cuoc_thang, dia_chi. loai_dich_vu"),
    Tu_khoa: str = Query(..., description="Keyword to search for")
):
    mysql_connection = connect_to_mysql()
    cursor = mysql_connection.cursor()
    
    try:
        query = f"SELECT loai_dich_vu,cuoc_thang,dia_chi,id_dau_vao FROM addresses WHERE {Truong_thong_tin} LIKE %s"
        cursor.execute(query, (f"%{Tu_khoa}%",))
        results = cursor.fetchall()
        
        total_bill = Decimal('0.00')
        list_service = ["IL", "RAC", "LL", "P2P", "TSL", "FH", "KDC", "IPLC", "IPC", "MPLS", "SDWAN", "BW", "EoSDH", "TTB", "DDOS"]
        service_count = {service: 0 for service in list_service}
        rows_list = []
        
        if results:
            for row in results:
                rows_list.append(row)
                if row[0] in list_service:
                    service_count[row[0]] += 1
                total_bill += row[1]
            
            return {
                "results": rows_list,
                "total_bill": str(total_bill),
                "service_count": service_count
            }
        else:
            return {"message": f"No records found for search value: {tu_khoa}"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error searching records: {err}")
    finally:
        cursor.close()
        mysql_connection.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
