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
        CREATE TABLE IF NOT EXISTS `addresses` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `dia_chi` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            `loai_dich_vu` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            `cuoc_thang` DECIMAL(15, 2),
            `id_dau_vao` INT
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
    parser.add_argument("--database", default="address_db", help="Database to connect mysql server")

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