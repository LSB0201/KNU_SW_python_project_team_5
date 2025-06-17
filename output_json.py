from flask import Flask, request, jsonify, send_from_directory
from db_connection import get_connection
from env_loader import TABLE_MAPPING
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔹 정적 HTML 파일(map.html) 서빙
@app.route('/')
def serve_main():
    return send_from_directory('../frontend', 'map.html')

# 🔹 JS 파일(js/*.js) 서빙
@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('../frontend/js', filename)

# 🔹 API: 필터 조건에 따라 DB에서 산불 + 소방서 정보 조회
@app.route("/api/mapping", methods=["POST"])
def get_mapping_data():
    data = request.json
    region = data.get("region")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    # 디버깅용 로그 출력
    print("검색 요청 도착:", region, start_date, end_date)

    like_region = "%" if region == "전체" else f"%{region}%"

    query = f"""
        SELECT 
            wildfire_latitude, wildfire_longitude,
            fire_station_latitude, fire_station_longitude,
            wildfire_location, occurred_at,
            fire_station_name
        FROM {TABLE_MAPPING}
        WHERE wildfire_location LIKE %s
          AND occurred_at BETWEEN %s AND %s
    """

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (like_region, start_date, end_date))
        result = cursor.fetchall()

        print(f"결과 데이터 수: {len(result)}")  # 디버깅용 출력
        return jsonify(result)

    except Exception as e:
        print("오류 발생:", str(e))
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
