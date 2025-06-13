import pandas as pd
import mysql.connector

# 1) 엑셀 파일 경로 지정
excel_path = "fire_station_with_coords.xlsx"

# 2) 엑셀 읽기
df = pd.read_excel(excel_path)

# 3) DB 연결 정보
from db_connection import get_connection
from env_loader import TABLE_FIRE_STATION

conn = get_connection()
cursor = conn.cursor()

# 4) region 추출 함수
def extract_region(address: str) -> str:
    try:
        parts = address.split()
        for part in parts:
            if part.endswith("시") or part.endswith("군"):
                return part
    except:
        return ""
    return ""

# 5) insert 쿼리 (region 포함)
insert_query = f"""
INSERT INTO {TABLE_FIRE_STATION} (location, name, phone, latitude, longitude, region)
VALUES (%s, %s, %s, %s, %s, %s)
"""

# 6) 데이터 반복 처리해서 DB 저장
for idx, row in df.iterrows():
    location = row['주소']
    name = row['119안전센터명']
    phone = row['전화번호']
    latitude = row['위도']
    longitude = row['경도']
    region = extract_region(location)

    cursor.execute(insert_query, (location, name, phone, latitude, longitude, region))

# 7) 변경사항 커밋 및 종료
conn.commit()
cursor.close()
conn.close()

print("소방서 데이터가 DB에 저장되었습니다.")
