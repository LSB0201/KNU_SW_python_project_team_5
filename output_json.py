import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from db_connection import get_connection
from env_loader import TABLE_MAPPING

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')

# Flask 앱 생성
app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path="",
    template_folder=FRONTEND_DIR
)
CORS(app)

# HTML 서빙
@app.route("/")
def serve_main():
    return render_template("map.html")

# API
@app.route("/api/mapping", methods=["POST"])
def get_mapping_data():
    data = request.json
    region = data.get("region")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    print("검색 요청 도착:", region, start_date, end_date)

    like_region = "%" if region == "전체" else f"%{region}%"

    query = f"""
        SELECT 
            wildfire_latitude, wildfire_longitude,
            fire_station_latitude, fire_station_longitude,
            wildfire_location, occurred_at,
            fire_station_name, fire_station_phone
        FROM {TABLE_MAPPING}
        WHERE wildfire_location LIKE %s
          AND occurred_at BETWEEN %s AND %s
    """

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (like_region, start_date, end_date))
        result = cursor.fetchall()
        print(f"결과 데이터 수: {len(result)}")
        return jsonify(result)

    except Exception as e:
        print("오류 발생:", str(e))
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# 실행
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
