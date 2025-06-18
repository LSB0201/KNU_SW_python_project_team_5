// 전역 변수 선언
let map;
let markers = [];
let polylines = [];

//  지도 초기화: DOM이 모두 로드된 후 실행
window.onload = () => {
  map = L.map('map').setView([36.0, 128.4], 9); // 경북 중심

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);
};

// 🔥 산불 아이콘
const wildfireIcon = L.divIcon({
  html: '🔥',
  className: 'wildfire-icon',
  iconSize: [40, 40],
  iconAnchor: [20, 20]
});

// 🚒 소방서 아이콘
const fireStationIcon = L.divIcon({
  html: '🚒',
  className: 'firestation-icon',
  iconSize: [40, 40],
  iconAnchor: [20, 20]
});


// 기존 마커/선 제거 함수
function clearMap() {
  markers.forEach(m => map.removeLayer(m));
  polylines.forEach(p => map.removeLayer(p));
  markers = [];
  polylines = [];
}

// 🔄 마커 렌더링 함수 (필터 검색 결과 후 호출)
function renderMarkers(data) {
  clearMap();

  data.forEach(item => {
    const {
      wildfire_latitude,
      wildfire_longitude,
      fire_station_latitude,
      fire_station_longitude,
      wildfire_location,
      occurred_at,
      fire_station_name,
      fire_station_phone
    } = item;

    // 🔥 산불 마커
    const wildfireMarker = L.marker([wildfire_latitude, wildfire_longitude], {
      icon: wildfireIcon
    }).addTo(map);
    wildfireMarker.bindPopup(`<b>🔥 화재 발생:</b><br>${wildfire_location}<br><b>🕒</b> ${occurred_at}`);

    // 🚒 소방서 마커
    const fireStationMarker = L.marker([fire_station_latitude, fire_station_longitude], {
      icon: fireStationIcon
    }).addTo(map);

    fireStationMarker.bindPopup(`
      <b>🚒 소방서:</b><br>${fire_station_name}<br>
      <b>📞:</b> ${fire_station_phone}
    `);

    // 저장
    markers.push(wildfireMarker, fireStationMarker);

    // 🔗 점선 연결 (산불 마커 클릭 시)
    wildfireMarker.on('click', () => {
      polylines.forEach(p => map.removeLayer(p));
      polylines = [];

      const line = L.polyline([
        [wildfire_latitude, wildfire_longitude],
        [fire_station_latitude, fire_station_longitude]
      ], {
        color: 'blue',
        dashArray: '5, 10',
        weight: 2
      }).addTo(map);

      polylines.push(line);
    });
  });

  // 데이터 있으면 첫 위치로 이동
  if (data.length > 0) {
    map.setView([data[0].wildfire_latitude, data[0].wildfire_longitude], 12);
  }
}
