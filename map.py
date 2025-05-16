import folium
import os
from branca.element import Template, MacroElement

# ✅ 지도 생성 (경북 중심)
gyeongbuk_center = [36.575, 128.505]
m = folium.Map(location=gyeongbuk_center, zoom_start=9)

# ✅ 경북대 상주캠퍼스 마커
folium.Marker(
    location=[36.4104, 128.1608],
    popup='경북대학교 상주캠퍼스',
    icon=folium.Icon(color='blue', icon='university', prefix='fa')
).add_to(m)

# ✅ 왼쪽 드롭다운 UI 템플릿
dropdown_html = """
{% macro html(this, kwargs) %}

<div style="position: fixed; 
            top: 13px; left: 80px; z-index: 9999; 
            background-color: white; 
            padding: 10px; 
            border: 2px solid gray; 
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
            margin-right: 20px;">

    <label for="citySelect"><b>경북 시 선택:</b></label><br>
    <select id="citySelect" onchange="alert(this.value)" style="width: 160px;">
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

{% endmacro %}
"""
dropdown = MacroElement()
dropdown._template = Template(dropdown_html)
m.get_root().add_child(dropdown)

# ✅ 왼쪽 재난 버튼 UI 템플릿
disaster_html = """
{% macro html(this, kwargs) %}

<style>
  .disaster-btn {
    padding: 7px 24px;
    font-size: 16px;
    border: none;
    background: white;
    border-radius: 20px;
    box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.2);
    font-weight: bold;
    cursor: pointer;
    transition: color 0.2s ease;
  }

  .disaster-btn:hover {
    color: royalblue;
  }
</style>

<div style="position: fixed;
            top: 15px;
            left: 300px;
            z-index: 9999;
            display: flex;
            gap: 24px;">

  <button onclick="alert('호우')" class="disaster-btn">🌧️ 호우</button>
  <button onclick="alert('산불')" class="disaster-btn">🔥 산불</button>
  <button onclick="alert('지진')" class="disaster-btn">💥 지진</button>
  <button onclick="alert('미세먼지')" class="disaster-btn">😷 미세먼지</button>

</div>

{% endmacro %}
"""
disaster_buttons = MacroElement()
disaster_buttons._template = Template(disaster_html)
m.get_root().add_child(disaster_buttons)

# ✅ 사용자 Downloads 폴더에 저장
download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
save_path = os.path.join(download_dir, "gyeongbuk_map.html")
m.save(save_path)

print(f"✅ 지도 저장 완료! 위치: {save_path}")
