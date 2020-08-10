const container = document.getElementById("map"); //지도를 담을 영역의 DOM
const mapInit = document.querySelector(".jsMapInit"); //첫 지도이미지 DOM
const regionSelectBox = document.querySelector(".jsRegionSelectBox"); //지역선택박스 DOM
const regionSelect = document.querySelector(".jsRegionSelect"); //지역선택 Select태그 DOM
var map;
let jinjuPolygon;

const jsonAsync = async (region) => {
  try {
    const getPolygonJson = await // 폴리곤 JSON 처리하는 부분
    $.getJSON("/static/map/js/regionPolygon.json", function (data) {
      jinjuPolygon = data.features.find((n) => {
        return n.properties.SIG_KOR_NM == region;
      }).geometry.coordinates[0];
    });
    const v1 = await setPath(jinjuPolygon);
    const v2 = await setPolygonAndAdd();
    const v3 = await setMouseInOut();
  } catch (error) {
  } finally {
  }
};

let options = {
  //지도를 생성할 때 필요한 기본 옵션
  center: new kakao.maps.LatLng(35.205392, 128.1267993), //지도의 중심좌표.
  level: 10, //지도의 레벨(확대, 축소 정도)
};

// 제일처음 시작되는 함수로, map_init에서 지역이 클릭되면 카카오맵이 호출됨
const startMap = () => {
  mapInit.classList.add("set_none"); //첫 지도이미지 display:none 추가
  regionSelectBox.classList.replace("set_none", "set_block"); //지역선택박스 none -> block으로 변경
  regionSelectBox.classList.add("set_z-index_6"); //지역선택박스 Kakao map 위로 오게 설정
  map = new kakao.maps.Map(container, options); //지도 생성 및 객체 리턴
  jsonAsync("진주시");
};

// 지역별 중심좌표를 모아놓은 객체
const regionCoordinate = {
  진주시: [35.205392, 128.1267993],
  김해시: [35.247945, 128.8513805],
};

// 중심좌표를 변경하는 함수
function setCenter(lat, lng) {
  // 이동할 위도 경도 위치를 생성합니다
  var moveLatLon = new kakao.maps.LatLng(lat, lng);
  // 지도 중심을 이동 시킵니다
  map.setCenter(moveLatLon);
}

// select박스에서 지역이 변경될시 호출되는 함수
const changeRegion = () => {
  let regionSelectedValue = regionSelect.value;
  setCenter(
    regionCoordinate[regionSelectedValue][0],
    regionCoordinate[regionSelectedValue][1]
  );
  polygonPath = [];
  polygon.setMap(null);
  changePolygon(regionSelectedValue);
};

// 다각형을 구성하는 좌표 배열입니다. 이 좌표들을 이어서 다각형을 표시합니다
let polygonPath = [];
let polygon = null;

// 다각형 좌표 셋팅하는 함수
const setPath = (data) => {
  for (let coords of data) {
    polygonPath.push(new kakao.maps.LatLng(coords[1], coords[0]));
  }
};
const setPolygonAndAdd = () => {
  // 지도에 표시할 다각형을 생성합니다
  polygon = new kakao.maps.Polygon({
    path: polygonPath, // 그려질 다각형의 좌표 배열입니다
    strokeWeight: 1, // 선의 두께입니다
    strokeColor: "#5D2C1D", // 선의 색깔입니다
    strokeOpacity: 1, // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
    strokeStyle: "solid", // 선의 스타일입니다
    fillColor: "#fff6ed", // 채우기 색깔입니다
    fillOpacity: 0.7, // 채우기 불투명도 입니다
  });

  // 지도에 다각형을 표시합니다
  polygon.setMap(map);
};

const changePolygon = async (region) => {
  try {
    const getPolygonJson = await // 폴리곤 JSON 처리하는 부분
    $.getJSON("/static/map/js/regionPolygon.json", function (data) {
      jinjuPolygon = data.features.find((n) => {
        return n.properties.SIG_KOR_NM == region;
      }).geometry.coordinates[0];
      setPath(jinjuPolygon);
    });
    const v1 = await delete polygon;
    const v2 = await setPolygonAndAdd();
    const v3 = await setMouseInOut();
  } catch {
  } finally {
  }
};

const setMouseInOut = () => {
  // 다각형에 마우스오버 이벤트가 발생했을 때 변경할 채우기 옵션입니다
  var mouseoverOption = {
    fillColor: "#5D2C1D", // 채우기 색깔입니다
    fillOpacity: 0.8, // 채우기 불투명도 입니다
  };

  // 다각형에 마우스아웃 이벤트가 발생했을 때 변경할 채우기 옵션입니다
  var mouseoutOption = {
    fillColor: "#fff6ed", // 채우기 색깔입니다
    fillOpacity: 0.7, // 채우기 불투명도 입니다
  };

  // 다각형에 마우스오버 이벤트를 등록합니다
  kakao.maps.event.addListener(polygon, "mouseover", function () {
    // 다각형의 채우기 옵션을 변경합니다
    polygon.setOptions(mouseoverOption);
  });

  kakao.maps.event.addListener(polygon, "mouseout", function () {
    // 다각형의 채우기 옵션을 변경합니다
    polygon.setOptions(mouseoutOption);
  });
};
