import mysql.connector
import argparse

def connection(host, port, user, password, database):
    print(f"Connecting to {host}:{port} with user={user} and password={password}")
    try:
        cnx = mysql.connector.connect(
            host=host,
            port=int(port),  # Use the mapped port
            user=user,
            password=password,
            database=database
        )
        return cnx
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
def create_table(cursor):
    try:
        cursor.execute("""
        CREATE TABLE addresses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Kenh TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            ID_dau_vao INT,
            Ma_KH_dau_vao TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            Doi_tac_ban_kenh_dau_vao TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            HD_dau_vao TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            Nha_cung_cap TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            Goi_cuoc VARCHAR(255),
            Cuoc_thang DECIMAL(15, 2),
            Diem_dau TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            Diem_cuoi TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            Chi_nhanh TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            Chi_nhanh_ky_dau_ra TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            Don_vi_ky_dau_ra TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            ID_dau_ra VARCHAR(255),
            Ma_KH_dau_ra TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            Doi_tac_ban_kenh_dau_ra TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            Ten_KH TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            Hop_dong_dau_ra TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            Loai_dich_vu TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            Dia_Chi TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            Ngay_nghiem_thu_thuc_te TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            Trang_thai_thue_bao_dau_ra TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            Dia_ban TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci   
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        """)
        print("Table 'addresses' created successfully or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Adding command line arguments
    parser.add_argument("--host", default="127.0.0.1", help="Host IP of server to connect mysql server")
    parser.add_argument("--port", default=3306, type=int, help="Port of server to connect mysql server")
    parser.add_argument("--user", default="root", help="User to connect mysql server normally is root")
    parser.add_argument("--password", default="kien123", help="Password to connect mysql server")
    parser.add_argument("--database", default="address_db_1", help="Database to connect mysql server")

    args = parser.parse_args()

    # Establish the connection
    mydb = connection(args.host, args.port, args.user, args.password, args.database)

    if mydb:
        print("Connection successful!")
        cursor = mydb.cursor()
        
        # Create the table
        create_table(cursor)
        
        # Commit the changes (in case of any other changes)
        mydb.commit()

        # Close the connection
        cursor.close()
        mydb.close()
    else:
        print("Failed to connect to MySQL.")