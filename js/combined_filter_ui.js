document.getElementById('search-btn').addEventListener('click', async () => {
  const region = document.getElementById('citySelect').value;
  const startDate = document.getElementById('start-date').value;
  const endDate = document.getElementById('end-date').value;
  if (!region || !startDate || !endDate) {
    alert('모든 항목을 선택해 주세요.');
    return;
  }
  const requestBody = { region, start_date: startDate, end_date: endDate };
  try {
    const response = await fetch("http://127.0.0.1:5000/api/mapping", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody)
    });
    const data = await response.json();
    if (data.error) {
      alert("서버 오류: " + data.error);
      return;
    }
    if (typeof renderMarkers === "function") {
      renderMarkers(data);
    } else {
      console.warn("renderMarkers 함수가 정의되어 있지 않습니다.");
    }
  } catch (err) {
    console.error("요청 실패:", err);
    alert("데이터를 가져오는 중 오류가 발생했습니다.");
  }
});
