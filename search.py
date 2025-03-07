import mysql.connector
import numpy as np 
import argparse as arg
# Function to connect to MySQL database
def connect_to_mysql(host, port, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None

# Function to search for "Bình Dương" in the database
def search_binh_duong(cursor):
    try:
        cursor.execute("SELECT loai_dich_vu,cuoc_thang,dia_chi FROM addresses WHERE dia_chi LIKE '%Phường Bình Hòa Thị xã Thuận An tỉnh Bình Dương%'")
        results = cursor.fetchall()
        
        # service = []
        # emty_service = {}

        total_bill=[]   
        List_service = ["IL","RAC","LL","P2P","TSL","FH","KDC","IPLC","IPC","MPLS","SDWAN","BW","EoSDH","TTB","DDOS"]
        service_count = {service: 0 for service in List_service}
        if results:
            print("Search results:")
            for row in results:
                print(row)
                #row[0].append(service)
                if row[0] in List_service:
                    # print(f"service found:{row[0]}")
                    service_count[row[0]] += 1
                # for service,count in service_count.items():
                #     print(f"{service}: {count}")                
                total_bill=+row[1]       
            print(f"Total bill:{total_bill}")
            print(f"Service count:{service_count}")
        else:
            print("No records found for 'Phường Bình Hòa Thị xã Thuận An tỉnh Bình Dương'.")
    except mysql.connector.Error as err:
        print(f"Error searching records: {err}")

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
    
    # Perform search
    search_binh_duong(cursor)
    
    # Close MySQL connection
    cursor.close()
    mysql_connection.close()
    print("MySQL connection is closed.")
else:
    print("Failed to connect to MySQL.")
