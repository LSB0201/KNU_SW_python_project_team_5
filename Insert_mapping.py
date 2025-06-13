import mysql.connector
from geopy.distance import geodesic

# DB 연결
from db_connection import get_connection
from env_loader import TABLE_FIRE_STATION, TABLE_WILDFIRE, TABLE_MAPPING

conn = get_connection()
cursor = conn.cursor(dictionary=True)

# wildfire 테이블에서 산불 데이터 가져오기
cursor.execute(f"SELECT * FROM {TABLE_WILDFIRE}")
wildfires = cursor.fetchall()

for fire in wildfires:
    fire_id = fire['id']
    fire_region = fire['region']
    fire_coords = (fire['latitude'], fire['longitude'])

    # 같은 지역(region)의 소방서만 필터링
    cursor.execute(f"SELECT * FROM {TABLE_FIRE_STATION} WHERE region = %s", (fire_region,))
    stations = cursor.fetchall()

    if not stations:
        print(f"[!] 지역 '{fire_region}' 에 해당하는 소방서가 없습니다. 산불 ID: {fire_id}")
        continue

    # 가장 가까운 소방서 찾기
    nearest = min(
        stations,
        key=lambda s: geodesic(fire_coords, (s['latitude'], s['longitude'])).meters
    )

    # 결과 저장 (중복 방지를 위해 REPLACE 사용 권장)
    cursor.execute(f"""
        REPLACE INTO {TABLE_MAPPING} (
            wildfire_id, wildfire_location, occurred_at,
            wildfire_latitude, wildfire_longitude,
            fire_station_id, fire_station_name,
            fire_station_latitude, fire_station_longitude
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        fire_id,
        fire['location'],
        fire['occurred_at'],
        fire['latitude'],
        fire['longitude'],
        nearest['id'],
        nearest['name'],
        nearest['latitude'],
        nearest['longitude']
    ))

conn.commit()
conn.close()
