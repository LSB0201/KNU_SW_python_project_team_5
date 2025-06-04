import os
import pandas as pd
import mysql.connector
import pymysql
import folium
import json
from db_config import db_config
from branca.element import Template, MacroElement

# [1] 엑셀 파일에서 DB로 삽입
excel_path = os.path.join("data", "경상북도_화재_정보.xlsx")
df = pd.read_excel(excel_path)
df.columns = df.columns.str.replace('\ufeff', '', regex=False).str.strip()
df = df.rename(columns={
    '발생일시': 'report_time',
    '신고주소': 'address',
    '위도': 'latitude',
    '경도': 'longitude'
})

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
insert_query = """
INSERT INTO fire_reports (report_time, address, latitude, longitude)
VALUES (%s, %s, %s, %s)
"""
for _, row in df.iterrows():
    cursor.execute(insert_query, (
        row['report_time'],
        row['address'],
        float(row['latitude']),
        float(row['longitude'])
    ))
conn.commit()
cursor.close()
conn.close()
print("엑셀 데이터 DB 삽입 완료")

# [2] DB에서 지도 데이터 로드
conn = pymysql.connect(
    host=db_config['host'],
    user=db_config['user'],
    password=db_config['password'],
    db=db_config['database'],
    port=db_config['port'],
    charset='utf8mb4'
)
sql = "SELECT report_time, address, latitude, longitude FROM fire_reports"
df = pd.read_sql(sql, conn)
conn.close()

# 마커 데이터 JSON으로 변환
marker_data = []
for _, row in df.iterrows():
    marker_data.append({
        "address": row["address"],
        "lat": row["latitude"],
        "lng": row["longitude"],
        "time": str(row["report_time"])
    })
marker_json = json.dumps(marker_data, ensure_ascii=False)

# 지도 생성
m = folium.Map(location=[35.4, 128.2], zoom_start=8.3)
map_id = m.get_name()

with open("combined_filter_ui.html", "r", encoding="utf-8") as f:
    filter_ui_html = f.read()
filter_ui = MacroElement()
filter_ui._template = Template(filter_ui_html)
m.get_root().add_child(filter_ui)

# 필터 스크립트 추가
with open("marker_filter_script.html", "r", encoding="utf-8") as f:
    filter_script_html = f.read()
filter_script_html = filter_script_html.replace("__MARKER_DATA__", marker_json).replace("__MAP__", map_id)
filter_script = MacroElement()
filter_script._template = Template(filter_script_html)
m.get_root().add_child(filter_script)

# 지도 저장
save_path = os.path.join(os.path.expanduser("~"), "Downloads", "gyeongbuk_map.html")
m.save(save_path)
print(f" ✅ 지도 저장 완료: {save_path}")
