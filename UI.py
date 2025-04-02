
import streamlit as st
import pandas as pd
import re 
import requests
import pyperclip
import sys
from io import BytesIO
sys.stdout.reconfigure(encoding='utf-8')
API_URL = "http://127.0.0.1:8000/search"

st.title("Tra cứu dữ liệu")

mapping_dict = {
    "Đếm số kênh (1)": "Kenh",
    "ID đầu vào": "ID_dau_vao",
    "Mã KH đầu vào": "Ma_KH_dau_vao",
    "Đối tác bán kênh đầu vào": "Doi_tac_ban_kenh_dau_vao",
    "HĐ đầu vào": "HD_dau_vao",
    "Nhà cung cấp": "Nha_cung_cap",
    "Gói cước (đầu vào)": "Goi_cuoc",
    "Cước tháng": "Cuoc_thang",
    "Điểm đầu": "Diem_dau",
    "Điểm cuối": "Diem_cuoi",
    "Chi nhánh lắp đặt": "Chi_nhanh",
    "Chi nhánh ký đầu ra": "Chi_nhanh_ky_dau_ra",
    "Đơn vị kí đầu ra": "Don_vi_ky_dau_ra",
    "ID đầu ra": "ID_dau_ra",
    "Mã KH đầu ra": "Ma_KH_dau_ra",
    "Đối tác bán kênh đầu ra": "Doi_tac_ban_kenh_dau_ra",
    "Tên KH": "Ten_KH",
    "Hợp đồng đầu ra": "Hop_dong_dau_ra",
    "Loại dịch vụ": "Loai_dich_vu",
    "Địa chỉ": "Dia_Chi",
    "Ngày nghiêm thu thực tế": "Ngay_nghiem_thu_thuc_te",
    "Trạng thái thuê bao đầu ra": "Trang_thai_thue_bao_dau_ra",
    "Địa bàn": "Dia_ban"
}

truong_thong_tin = st.selectbox(
    "Chọn trường thông tin để tìm kiếm:",
    [
    "Đếm số kênh (1)", "ID đầu vào", "Mã KH đầu vào", "Đối tác bán kênh đầu vào", "HĐ đầu vào",
    "Nhà cung cấp", "Gói cước (đầu vào)", "Cước tháng", "Điểm đầu", "Điểm cuối", "Chi nhánh lắp đặt", 
    "Chi nhánh ký đầu ra", "Đơn vị kí đầu ra", "ID đầu ra", "Mã KH đầu ra", 
    "Đối tác bán kênh đầu ra", "Tên KH", "Hợp đồng đầu ra", "Loại dịch vụ", 
    "Địa chỉ", "Ngày nghiêm thu thực tế", "Trạng thái thuê bao đầu ra", "Địa bàn"
]
)
translated_field = mapping_dict.get(truong_thong_tin, truong_thong_tin)
def to_excel(df):
    # Create a BytesIO buffer to store the Excel file in memory
    buffer = BytesIO()
    # Write the DataFrame to the buffer (use openpyxl engine for .xlsx)
    df.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)  # Go to the beginning of the buffer
    return buffer

#tu_khoa = st.text_input("Nhập từ khóa tìm kiếm:")
tu_khoa = re.sub(r'\s+', ' ', st.text_input("Nhập từ khóa tìm kiếm:")).rstrip()
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if st.button("Tìm kiếm"): 
    if not tu_khoa:
        st.warning("Vui lòng nhập từ khóa.")
    else:
     
        params = {"Truong_thong_tin": translated_field, "Tu_khoa": tu_khoa}
        response = requests.get(API_URL, params=params)

        if response.status_code == 200:
            data = response.json()

            if "results" in data and data["results"]:
                df = pd.DataFrame(data["results"], columns=[
                "Đếm số kênh (1)", "ID đầu vào", "Mã KH đầu vào", "Đối tác bán kênh đầu vào", "HĐ đầu vào",
                "Nhà cung cấp", "Gói cước (đầu vào)", "Cước tháng", "Điểm đầu", "Điểm cuối", "Chi nhánh lắp đặt", 
                "Chi nhánh ký đầu ra", "Đơn vị kí đầu ra", "ID đầu ra", "Mã KH đầu ra", 
                "Đối tác bán kênh đầu ra", "Tên KH", "Hợp đồng đầu ra", "Loại dịch vụ", 
                "Địa chỉ", "Ngày nghiêm thu thực tế", "Trạng thái thuê bao đầu ra", "Địa bàn"
            ])
                            
         
                st.dataframe(df, use_container_width=True)  

                st.subheader("📌 Tổng tiền cước tháng")
                st.write(f"💰 **{data['total_bill']}**")

                st.subheader("📊 Số lượng từng loại dịch vụ")

                table_data = to_excel(df)
                st.download_button(
                    label="Download Excel",
                    data=table_data,
                    file_name="data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                                                
                service_count_df = pd.DataFrame(
                    list(data["service_count"].items()), 
                    columns=["Loại dịch vụ", "Số lượng"]
                )
                
               
                st.bar_chart(service_count_df.set_index("Loại dịch vụ"))

            else:
                st.warning("Không tìm thấy dữ liệu phù hợp.")
        else:
            st.error(f"Lỗi API: {response.status_code}")

if uploaded_file:
    if st.button("Apply Data"):
        try: 
            files = {"file": uploaded_file.getvalue()}
            response = requests.post("http://127.0.0.1:8000/insert", files=files)
    
            if response.status_code == 200:
                st.success("Data uploaded and inserted into MySQL successfully!")
            else:
                st.error("Failed to insert data. Check FastAPI logs.")
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

if st.button("Delete Data"):
    response = requests.delete("http://127.0.0.1:8000/Drop_full_table")  # Call FastAPI endpoint
    
    if response.status_code == 200:
        st.success("✅ Table 'addresses' has been dropped successfully!")
    else:
        st.error(f"❌ Error: {response.json().get('error', 'Unknown error')}")
