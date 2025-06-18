 <h1 align="center">🔥 여기 불났숲!!</h1>
<p align="center"><strong>Team 5 - KNU SW Project</strong></p>

> 산불 발생 위치에 따라 가장 가까운 소방서를 자동으로 매핑하고, 지도 기반 시각화 기능을 제공하는 Python 기반 프로젝트입니다.

---
## 프로젝트 소개
- 🗓️**프로젝트 기간**
  <br> 2025/5/18 ~ 2025/6/19 (총 한달)


-  **팀원 소개 및 기여(역할)**
  <p>
  <a href="https://github.com/LSB0201/KNU_SW_python_project_team_5/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=LSB0201/KNU_SW_python_project_team_5" style="zoom: 100%;"/>
</a>


|    팀원    |                      기여                       |
| :--------: | :---------------------------------------------: |
| **LSB0201** |   내용 넣으삼 |
| **pastarobber** |  내용 넣으삼  |
| **Gang-Choo** |  내용 넣으삼  |

</p>
<br>

  
## 📌 프로젝트 개요

- ⏱️ **산불 API 데이터를 주기적으로 수집** → 매일 오전 3시
- 💾 **라즈베리파이에 데이터 저장**
- 🌐 **Tailscale VPN**을 통해 외부에서도 접속 가능
- 🗺️ **Folium 지도 시각화**를 통해 산불 ↔ 소방서 위치를 직관적으로 표현
- 🧱 추후 확장을 고려한 **모듈화 구조**

---

## 🖥️ 시스템 구성

| 구성 요소       | 설명 |
|----------------|------|
| 데이터 수집     | 산불 API, 소방서 엑셀 파일 |
| 데이터 저장     | 라즈베리파이에 설치된 MySQL DB |
| 서버           | Flask 기반 REST API |
| 접속 방식      | [Tailscale](https://tailscale.com) VPN |
| 시각화         | Folium + HTML + JS 지도 렌더링 |

<details>
<summary>🛡️ 왜 Tailscale VPN을 사용했나요?</summary>
<br>
같은 와이파이(KNU-WiFi5)라도 서브넷이 달라 사설 IP 상 통신 불가.  
AWS를 사용하지 않고도 **외부에서 안전하게 서버 접근**하기 위한 선택.
</details>


## 🧩 디렉토리 구조

```
KNU_SW_python_project_team_5/
├── main/                      # 앱 실행 및 통합 제어
├── frontend/                 # 사용자 UI
│   ├── map.html              # 지도 시각화 메인 페이지
│   └── js/
│       ├── combined_filter_ui.js
│       └── marker_filter_script.js
├── backend/                  # Flask 서버 + DB 연동
│   ├── .env
│   ├── db_connection.py
│   ├── Insert_fire_station.py
│   ├── Insert_mapping.py
│   ├── Insert_wildfire.py
│   └── output_json.py
├── venv/                     # Python 가상환경
```

## ⚙️ 개발 환경

- **OS**: Raspberry Pi OS
- **언어**: Python 3.12.6
- **DB**: MySQL (MariaDB)
- **VPN**: Tailscale
- **Frontend**: HTML + JS + Folium
- **Backend**: Flask
- **환경 변수 관리**: `.env` + `python-dotenv`

<details>
<summary>📦 주요 라이브러리 목록</summary>
<br>

- 'pandas', 'folium', 'geopy', 'mysql-connector-python', 'openpyxl'  
- 'flask', 'flask-cors', 'python-dotenv', 'branca', 'pymysql'
</details>

---

## 🗄️ 데이터베이스 테이블 구조

<details>
<summary>📋 fire_station</summary>

sql
CREATE TABLE fire_station_test (
  id INT AUTO_INCREMENT PRIMARY KEY,
  location VARCHAR(255),
  name VARCHAR(100),
  phone VARCHAR(30),
  latitude DOUBLE,
  longitude DOUBLE,
  region VARCHAR(50)
);
</details> <details> <summary>📋 wildfire</summary>
CREATE TABLE wildfire (
  id INT AUTO_INCREMENT PRIMARY KEY,
  location VARCHAR(255),
  occurred_at DATETIME,
  latitude DOUBLE,
  longitude DOUBLE,
  region VARCHAR(50)
);
</details><details> <summary>📋 mapping_test</summary>
CREATE TABLE mapping_test (
  wildfire_id INT PRIMARY KEY,
  wildfire_location VARCHAR(255),
  occurred_at DATETIME,
  wildfire_latitude DOUBLE,
  wildfire_longitude DOUBLE,
  fire_station_id INT,
  fire_station_name VARCHAR(100),
  fire_station_latitude DOUBLE,
  fire_station_longitude DOUBLE
);
</details>
cd C:\Python_Code\KNU_SW_python_project_team_5

# 가상환경 생성 (이미 생성 완료)
python -m venv venv

# 터미널에서 실행 권한 설정 (임시)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 가상환경 실행
.\venv\Scripts\Activate.ps1
팀원 소개
이름	역할
이성배	프론트엔드와 API 명세 정의 및 통신 구현
이미림	Folium 지도 시각화 및 산불-소방서 매핑 구현
추강민	서버 백그라운드 등록, 데이터 파싱 및 저장
📚 참고 자료
🔥 공공데이터포털 - 산불정보

🌐 Tailscale VPN

📖 Folium 공식 문서

🚧 본 프로젝트는 교육 목적의 데모용으로 제작되었으며, 상용 배포되지 않았습니다.
⚠️ 실시간 재난 대응에는 사용하지 마세요.
