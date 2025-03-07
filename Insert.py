import mysql.connector
import pandas as pd
# Addtion duplicat insert function 
# Deploy up on Web server 
# Function to connect to MySQL database
def connect_to_mysql(host, port, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            port=int(port),  # Use the mapped port
            user=user,
            password=password,
            database=database
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None

# Function to create the table if it doesn't exist
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

# Function to insert address data into the table
def insert_address(dia_chi, loai_dich_vu, cuoc_thang, id_dau_vao, cursor, mydb):
    try:aerr}")

# Read Excel data
df = pd.read_excel("Sl kênh hiện hữu năm 2024.xlsx")

# Clean 'Cước tháng' column to ensure valid numbers and replace NaN with a default value (0 or any valid value)
df["Cước tháng"] = pd.to_numeric(df["Cước tháng"], errors='coerce')  # Convert invalid values to NaN
df["Cước tháng"] = df["Cước tháng"].fillna(0)  # Replace NaN values with 0

# Cap 'Cước tháng' values that exceed a reasonable value, e.g., 999999999999.99 (DECIMAL(15, 2))
max_value = 999999999999.99
df["Cước tháng"] = df["Cước tháng"].apply(lambda x: min(x, max_value))  # Cap values at the max allowed

# Ensure that no negative values exist in 'Cước tháng'
df["Cước tháng"] = df["Cước tháng"].apply(lambda x: max(x, 0))  # Ensure that the values are not negative

# Connect to MySQL database
host = 'localhost'  # MySQL host
port = 3306        # MySQL port
user = 'root'       # MySQL username
password = 'kien123'  # MySQL password
database = 'address_db'  # MySQL database name

# Establish MySQL connection
mysql_connection = connect_to_mysql(host, port, user, password, database)

if mysql_connection:
    cursor = mysql_connection.cursor()

    # Create table if it doesn't exist
    create_table(cursor)

    # Insert data from the DataFrame into the MySQL database
    for index, row in df.iterrows():
        insert_address(row['Địa chỉ'], row['Loại dịch vụ'], row['Cước tháng'], row.get('ID đầu vào', None), cursor, mysql_connection)

    print("Data has been successfully inserted into MySQL.")
    
    # Close MySQL connection
    cursor.close()
    mysql_connection.close()
    print("MySQL connection is closed.")
else:
    print("Failed to connect to MySQL.")
