const bakeryDetailMap = () => {
  const detailMapContainer = document.getElementById("detailMap"); // 지도를 표시할 div
  const detailMapOption = {
    center: new kakao.maps.LatLng(mapLat, mapLng), // 지도의 중심좌표
    level: 8, // 지도의 확대 레벨
    disableDoubleClick: true,
  };

  // 지도를 표시할 div와  지도 옵션으로  지도를 생성합니다
  const detailMap = new kakao.maps.Map(detailMapContainer, detailMapOption);
  detailMap.setDraggable(false);
  detailMap.setZoomable(false);

  // 마커가 표시될 위치입니다
  const detailMapMarkerPosition = new kakao.maps.LatLng(mapLat, mapLng);

  // 마커 이미지 src
  var detailMapImageSrc = "/static/map/img/maker.png";

  // 마커 이미지의 이미지 크기 입니다
  const detailMapImageSize = new kakao.maps.Size(24, 35);

  // 마커 이미지를 생성합니다
  const detailMapMarkerImage = new kakao.maps.MarkerImage(
    detailMapImageSrc,
    detailMapImageSize
  );

  // 마커를 생성합니다
  const detailMapMarker = new kakao.maps.Marker({
    position: detailMapMarkerPosition,
    image: detailMapMarkerImage,
    clickable: false,
  });

  // 마커가 지도 위에 표시되도록 설정합니다
  detailMapMarker.setMap(detailMap);
};
