import requests
import urllib3
import mysql.connector
from datetime import datetime
from env_loader import API_KEY, TABLE_WILDFIRE
from db_connection import get_connection

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://www.safetydata.go.kr/V2/api/DSSP-IF-10346"
serviceKey = API_KEY #산불 재난 API 키 입력

all_data = []
page = 1
num_of_rows = 1000

while True:
    payloads = {
        "serviceKey": serviceKey,
        "returnType": "json",
        "pageNo": str(page),
        "numOfRows": str(num_of_rows),
        "startDt": "20250101",
    }

    response = requests.get(url, params=payloads, verify=False)
    try:
        data = response.json()
    except ValueError:
        print(f"JSON 파싱 오류 발생: page {page}")
        break

    items = data.get("body", [])
    if not items:
        break  # 더 이상 데이터가 없으면 종료

    all_data.extend(items)
    print(f"{page}페이지 처리 완료. 누적 데이터 수: {len(all_data)}")
    page += 1

# 경상북도 필터링 (시도 코드: 47)
gyeongsangbukdo_data = [
    item for item in all_data
    if (item.get("STDG_CTPV_CD") or "").strip() == "47"
]

print(f"\n경상북도 전체 데이터 개수: {len(gyeongsangbukdo_data)}")

def extract_region(address: str) -> str:
    """주소에서 시 또는 군 추출 (ex. '경산시', '상주시')"""
    try:
        parts = address.split()
        for part in parts:
            if part.endswith("시") or part.endswith("군"):
                return part
    except:
        return ""
    return ""

try:
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = f"""
        INSERT INTO {TABLE_WILDFIRE} (location, occurred_at, latitude, longitude, region)
        VALUES (%s, %s, %s, %s, %s)
    """

    for item in gyeongsangbukdo_data:
        dt_str = item["FRSTFR_GNT_DT"].split('.')[0]
        occurred_at = datetime.strptime(dt_str, "%Y/%m/%d %H:%M:%S")

        location = item.get("FRSTFR_DCLR_ADDR", "")
        latitude = float(item.get("FRSTFR_PSTN_YCRD", 0))
        longitude = float(item.get("FRSTFR_PSTN_XCRD", 0))
        region = extract_region(location)

        cursor.execute(insert_query, (location, occurred_at, latitude, longitude, region))

    conn.commit()
    print("DB에 데이터 저장 완료.")

except mysql.connector.Error as err:
    print(f"DB 오류 발생: {err}")

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
