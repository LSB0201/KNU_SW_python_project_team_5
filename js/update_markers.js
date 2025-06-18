async function updateMapMarkers(region, startDate, endDate) {
  // 아무 값도 입력되지 않았을 때 경고
  if ((!region || region === "시/군 선택") && !startDate && !endDate) {
    alert("지역 또는 날짜를 선택해 주세요.");
    return;
  }

  const requestBody = {};

  // '전체'도 서버로 전달 (서버가 이를 인식해야 함)
  if (region && region !== "시/군 선택") {
    requestBody.region = region;
  }
  if (startDate) requestBody.start_date = startDate;
  if (endDate) requestBody.end_date = endDate;

  try {
    const response = await fetch("/api/mapping", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      throw new Error("서버 응답 오류");
    }

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
}
