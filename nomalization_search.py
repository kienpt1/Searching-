import pandas as pd 
from createtable import create_table
import re

def normalization_vnword(text: str) -> str:

    text = re.sub(r'(à|á|ạ|ả|ã|â|ầ|ấ|ậ|ẩ|ẫ|ă|ằ|ắ|ặ|ẳ|ẵ)', 'a', text)
    text = re.sub(r'(è|é|ẹ|ẻ|ẽ|ê|ề|ế|ệ|ể|ễ)', 'e', text)
    text = re.sub(r'(ì|í|ị|ỉ|ĩ)', 'i', text)
    text = re.sub(r'(ò|ó|ọ|ỏ|õ|ô|ồ|ố|ộ|ổ|ỗ|ơ|ờ|ớ|ợ|ở|ỡ)', 'o', text)
    text = re.sub(r'(ù|ú|ụ|ủ|ũ|ư|ừ|ứ|ự|ử|ữ)', 'u', text)
    text = re.sub(r'(ỳ|ý|ỵ|ỷ|ỹ)', 'y', text)
    text = re.sub(r'(đ)', 'd', text)
    text = re.sub(r'[^a-z0-9-\s]', '', text, flags=re.IGNORECASE)  # Remove special characters
    text = re.sub(r'[\s]+', '', text)  # Replace spaces with hyphens
    
    return text.lower().rstrip()