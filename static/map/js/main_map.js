let container = document.getElementById("map"); //지도를 담을 영역의 DOM
const mapInit = document.querySelector(".jsMapInit"); //첫 지도이미지 DOM
const regionSelectBox = document.querySelector(".jsRegionSelectBox"); //지역선택박스 DOM
const regionSelect = document.querySelector(".jsRegionSelect"); //지역선택 Select태그 DOM
const content = document.querySelector(".content");
var map;
let jinjuPolygon;
let marker;
let markers = [];

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
  regionSelectBox.classList.replace("set_none", "set_flex"); //지역선택박스 none -> block으로 변경
  regionSelectBox.classList.add("set_z-index_6"); //지역선택박스 Kakao map 위로 오게 설정
  map = new kakao.maps.Map(container, options); //지도 생성 및 객체 리턴
  jsonAsync("진주시");
  var positions = [
    {
      title: "수복빵집",
      latlng: new kakao.maps.LatLng(35.1966287, 128.01815868),
    },
    {
      title: "베이커리925",
      latlng: new kakao.maps.LatLng(35.23564072, 128.1033207),
    },
    {
      title: "장동근과자점",
      latlng: new kakao.maps.LatLng(35.21796814, 128.2341212325),
    },
    {
      title: "양우연케익하우스",
      latlng: new kakao.maps.LatLng(35.1796763, 128.07333617),
    },
    {
      title: "뚜레쥬르 진주호탄점",
      latlng: new kakao.maps.LatLng(35.1631501, 128.213512432),
    },
    {
      title: "이용규베커라이",
      latlng: new kakao.maps.LatLng(35.1692635, 128.2734668392),
    },
  ];

  // 마커 이미지의 이미지 주소입니다
  var imageSrc = "/static/map/img/maker.png";

  for (var i = 0; i < positions.length; i++) {
    // 마커 이미지의 이미지 크기 입니다
    var imageSize = new kakao.maps.Size(24, 35);

    // 마커 이미지를 생성합니다
    var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);

    // 마커를 생성합니다
    marker = new kakao.maps.Marker({
      map: map, // 마커를 표시할 지도
      position: positions[i].latlng, // 마커를 표시할 위치
      image: markerImage, // 마커 이미지
      clickable: true, // 마커를 클릭했을 때 지도의 클릭 이벤트가 발생하지 않도록 설정합니다
    });
    markers.push(marker);

    // 마커를 클릭했을 때 마커 위에 표시할 인포윈도우를 생성합니다
    var iwContent = `<div style="padding:5px; ">${positions[i].title}</div>`, // 인포윈도우에 표출될 내용으로 HTML 문자열이나 document element가 가능합니다
      iwRemoveable = true; // removeable 속성을 ture 로 설정하면 인포윈도우를 닫을 수 있는 x버튼이 표시됩니다

    // 인포윈도우를 생성합니다
    infowindow_list.push("");

    infowindow_list[i] = new kakao.maps.InfoWindow({
      content: iwContent,
      removable: iwRemoveable,
    });

    // 마커에 클릭이벤트를 등록합니다
    kakao.maps.event.addListener(
      marker,
      "click",
      clickListener(map, marker, infowindow_list[i])
    );
    let mouseoverOption = {
      fillColor: "#5D2C1D", // 채우기 색깔입니다
      fillOpacity: 0.8, // 채우기 불투명도 입니다
    };
    // 마커에 마우스오버 이벤트를 등록합니다
    kakao.maps.event.addListener(marker, "mouseover", function () {
      // 다각형의 채우기 옵션을 변경합니다
      polygon.setOptions(mouseoverOption);
    });
  }
};

let infowindow_list = [];

// 이전에 띄워져있던 인포윈도우들을 모두 닫는 함수
const closeAllInfowindow = () => {
  for (let x = 0; x < infowindow_list.length; x++) {
    infowindow_list[x].close();
  }
};

// 인포윈도우를 표시하는 클로저를 만드는 함수입니다
function clickListener(map, marker, infowindow) {
  return function () {
    closeAllInfowindow();
    infowindow.open(map, marker);
  };
}

// 지역별 중심좌표를 모아놓은 객체
const regionCoordinate = {
  진주시: [35.205392, 128.1267993],
  사천시: [34.969495, 128.0409305],
  김해시: [35.247945, 128.8513805],
  밀양시: [35.4919987, 128.7380404],
  양산시: [35.340795, 128.9964805],
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
  for (let i in markers) {
    markers[i].setMap(null);
  }

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
  let mouseoverOption = {
    fillColor: "#5D2C1D", // 채우기 색깔입니다
    fillOpacity: 0.8, // 채우기 불투명도 입니다
  };

  // 다각형에 마우스아웃 이벤트가 발생했을 때 변경할 채우기 옵션입니다
  let mouseoutOption = {
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

// 지역선택으로 돌아가는 뒤로가기버튼 눌렀을때 실행됨
const clickRegionBack = () => {
  delete map;
  delete polygon;
  for (let i in markers) {
    markers[i].setMap(null);
  }
  mapInit.classList.remove("set_none"); //첫 지도이미지 display:none 추가
  regionSelectBox.classList.replace("set_flex", "set_none"); //지역선택박스 none -> block으로 변경
  regionSelectBox.classList.remove("set_z-index_6"); //지역선택박스 Kakao map 위로 오게 설정
  container.remove(); // map셋팅 삭제를 위해 div map element 제거
  content.insertAdjacentHTML(
    // div map 새로 element 추가
    "afterbegin",
    `
    <div id="map"></div>
    `
  );
  container = document.getElementById("map"); //새로생긴 div map의 DOM
  polygonPath = [];
  polygon.setMap(null);
};
