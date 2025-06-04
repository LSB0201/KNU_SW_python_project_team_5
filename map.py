import os
import pandas as pd
import mysql.connector
import pymysql
import folium
import json
from db_config import db_config
from branca.element import Template, MacroElement

### ✅ [1] 엑셀 → MySQL 삽입

excel_path = r'C:\Users\이미림\Desktop\python_project\경상북도_화재_정보.xlsx'
df = pd.read_excel(excel_path)

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
print("✅ 엑셀 데이터 DB 삽입 완료")

### ✅ [2] DB → 지도 시각화 (folium + 드롭다운 필터링)

# DB에서 불러오기
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

# 지도 생성
m = folium.Map(location=[35.4, 128.2], zoom_start=8.3)
map_id = m.get_name()

# 마커 JSON 생성
marker_data = []
for _, row in df.iterrows():
    marker_data.append({
        "address": row["address"],
        "lat": row["latitude"],
        "lng": row["longitude"],
        "time": str(row["report_time"])
    })
marker_json = json.dumps(marker_data, ensure_ascii=False)

# 드롭다운 UI
dropdown_html = """{% macro html(this, kwargs) %}
<div style="position: fixed; top: 13px; left: 80px; z-index: 9999; background-color: white; padding: 10px; border: 2px solid gray; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);">
    <label for="citySelect"><b>경북 시/군 선택:</b></label><br>
    <select id="citySelect" style="width: 160px;">
        <option value="" disabled selected hidden>시/군 선택</option>
        <option value="전체">전체</option>
        <option value="경산시">경산시</option>
        <option value="경주시">경주시</option>
        <option value="구미시">구미시</option>
        <option value="김천시">김천시</option>
        <option value="문경시">문경시</option>
        <option value="상주시">상주시</option>
        <option value="안동시">안동시</option>
        <option value="영주시">영주시</option>
        <option value="영천시">영천시</option>
        <option value="포항시">포항시</option>
        <option value="의성군">의성군</option>
        <option value="칠곡군">칠곡군</option>
        <option value="청송군">청송군</option>
    </select>
</div>
{% endmacro %}"""
dropdown = MacroElement()
dropdown._template = Template(dropdown_html)
m.get_root().add_child(dropdown)

# 마커 필터링 스크립트
filter_script_html = """
{% macro html(this, kwargs) %}
<script>
  const markers = __MARKER_DATA__;
  let mapMarkers = [];

    const cityCenters = {
    "경산시": [35.825, 128.74],
    "경주시": [35.856, 129.224],
    "구미시": [36.12, 128.344],
    "김천시": [36.139, 128.113],
    "문경시": [36.594, 128.188],
    "상주시": [36.411, 128.158],
    "안동시": [36.568, 128.729],
    "영주시": [36.805, 128.623],
    "영천시": [35.973, 128.94],
    "포항시": [36.019, 129.343],
    "의성군": [36.354, 128.697],
    "칠곡군": [35.995, 128.41],
    "청송군": [36.435, 129.056]
  };

  function showMarkers(cityName) {
  mapMarkers.forEach(m => __MAP__.removeLayer(m));
  mapMarkers = [];

  // 전체 선택 시 바로 처리
  const filtered = cityName === "전체" || cityName === "" 
    ? markers 
    : markers.filter(data => data.address.includes(cityName));

  filtered.forEach(data => {
    const icon = L.divIcon({
      className: "",
      html: `<div style="
        background-color: white;
        border: 2px solid red;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        text-align: center;
        line-height: 40px;
        font-size: 22px;
        box-shadow: 1px 1px 5px rgba(255,0,0,0.5);
        user-select: none;
        pointer-events: auto;
        display: flex;
        align-items: center;
        justify-content: center;
      ">🔥</div>`
    });

    const marker = L.marker([data.lat, data.lng], { icon: icon })
      .addTo(__MAP__)
      .bindPopup(`🔥 화재 발생: ${data.address}<br>🕒 ${data.time}`);
    mapMarkers.push(marker);
  });

   // 지도 이동
    if (cityName && cityCenters[cityName]) {
      __MAP__.setView(cityCenters[cityName], 11);
    } else {
      __MAP__.setView([35.4, 128.2], 8.3);  // 전체 선택 시 초기 위치로
    }
}

  document.getElementById("citySelect").addEventListener("change", function(e) {
    const selected = e.target.value;
    showMarkers(selected);
  });

  showMarkers("");
</script>
{% endmacro %}
"""

filter_script_html = (
    filter_script_html
    .replace("__MARKER_DATA__", marker_json)
    .replace("__MAP__", map_id)
)
filter_script = MacroElement()
filter_script._template = Template(filter_script_html)
m.get_root().add_child(filter_script)

# 지도 저장
save_path = os.path.join(os.path.expanduser("~"), "Downloads", "gyeongbuk_map.html")
m.save(save_path)
print(f"✅ 지도 저장 완료: {save_path}")
