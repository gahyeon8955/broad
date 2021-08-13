let container = document.getElementById("map"); //지도를 담을 영역의 DOM
const mapInit = document.querySelector(".jsMapInit"); //첫 지도이미지 DOM
const regionSelectBox = document.querySelector(".jsRegionSelectBox"); //지역선택박스 DOM
const regionSelect = document.querySelector(".jsRegionSelect"); //지역선택 Select태그 DOM
const content = document.querySelector(".content");
const goToList = document.querySelector(".go_to_list");
let detailHeader;
let reviewBakeryName;
let bakeryPK;
var map;
let jinjuPolygon;
let marker;
let markers = [];
let overlay;
let overlayContent;
let bakeryName = "";
let address = "";
let imgUrl = "";
let pk = "";
let mylat;
let mylng;
let myname;
let myaddress;
let myphoto = "";
let positions = {};
let local;
let clusterer;

const addRegionSelect = (local) => {
  for (const city of regionData[local]) {
    regionSelect.insertAdjacentHTML(
      "beforeend",
      `
        <option value="${city[0]}">${city[0]}</option>
      `
    );
  }
};

const getRegionData = (region) => {
  $.ajax({
    type: "GET",
    url: getRegionDataUrl,
    data: { region },
    dataType: "json",
    success: (response) => {
      positions = response;
      setOverlayAndMarker();
    },
  });
};

const setOverlayAndMarker = () => {
  overlayContent = (pk, name, address, imgUrl) => {
    return `
  <div class="wrap">
        <div class="info">
            <div class="title">
                <div onclick="goPinToBakeryDetail(${pk})">${name}</div>
                <div style="background-image:url(${closeUrl})" class="close" onclick="closeOverlay()" title="닫기"></div>
            </div>
            <div onclick="goPinToBakeryDetail(${pk})" class="body">
                <div class="img">
                    <img src="${imgUrl}" width="73" height="70">
               </div>
                <div class="desc">
                    <div class="ellipsis">${address}</div>
                </div>
            </div>
        </div>
    </div>
    `;
  };
  clusterer = new kakao.maps.MarkerClusterer({
    map: map, // 마커들을 클러스터로 관리하고 표시할 지도 객체
    averageCenter: true, // 클러스터에 포함된 마커들의 평균 위치를 클러스터 마커 위치로 설정
    minLevel: 10, // 클러스터 할 최소 지도 레벨
  });

  // 마커 위에 커스텀오버레이를 표시합니다
  // 마커를 중심으로 커스텀 오버레이를 표시하기위해 CSS를 이용해 위치를 설정했습니다

  // 마커 이미지의 이미지 주소입니다
  var imageSrc = "/static/map/img/maker.png";
  for (const i in positions) {
    // 마커 이미지의 이미지 크기 입니다
    var imageSize = new kakao.maps.Size(24, 35);

    // 마커 이미지를 생성합니다
    var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);

    // 빵집 정보관련 데이터
    let mylat = positions[i].bakery[0].fields.lat;
    let mylng = positions[i].bakery[0].fields.lng;
    let mypk = positions[i].bakery[0].pk;
    let myname = positions[i].bakery[0].fields.name;
    let myaddress = positions[i].bakery[0].fields.address;
    try {
      // myphoto = `https://broadbucket.s3.amazonaws.com/${positions[i].photos[0].fields.photo}`;
      myphoto = `/media/${positions[i].photos[0].fields.photo}`;
    } catch (error) {
      // myphoto = `https://broadbucket.s3.amazonaws.com/bakery/image/logo_default.png`;
      myphoto = `/media/bakery/image/logo_default.png`;
    }

    // 마커를 생성합니다
    marker = new kakao.maps.Marker({
      map: map, // 마커를 표시할 지도
      position: new kakao.maps.LatLng(mylat, mylng), // 마커를 표시할 위치
      image: markerImage, // 마커 이미지
      clickable: true, // 마커를 클릭했을 때 지도의 클릭 이벤트가 발생하지 않도록 설정합니다
    });
    markers.push(marker);

    // 마커를 클릭했을 때 커스텀 오버레이를 표시합니다
    kakao.maps.event.addListener(
      marker,
      "click",
      addClosureOverlay(marker, mypk, myname, myaddress, myphoto)
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
    myname = "";
    myaddress = "";
    myphoto = "";
  }
  // 클러스터러에 마커들을 추가합니다
  clusterer.addMarkers(markers);
};

const jsonAsync = async (region) => {
  try {
    if (region.includes("광역시")) {
      const getPolygonJson = await // 폴리곤 JSON 처리하는 부분
      $.getJSON("/static/map/js/sidoPolygon.json", function (data) {
        datas = data;
        jinjuPolygon = data.features.find((n) => {
          return n.properties.CTP_KOR_NM == region;
        }).geometry.coordinates[0];
      });
    } else {
      const getPolygonJson = await // 폴리곤 JSON 처리하는 부분
      $.getJSON("/static/map/js/regionPolygon.json", function (data) {
        datas = data;
        jinjuPolygon = data.features.find((n) => {
          return n.properties.SIG_KOR_NM == region;
        }).geometry.coordinates[0];
      });
    }
    const v1 = await setPath(jinjuPolygon);
    const v2 = await setPolygonAndAdd();
    const v3 = await setMouseInOut();
    const v4 = await getRegionData(region); // region에 해당되는 빵집데이터 갖고오기
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
const startMap = (event) => {
  body.classList.remove("set_fixed");
  content.classList.add("set_base_content_padding");
  mapInit.classList.add("set_none"); //첫 지도이미지 display:none 추가
  regionSelectBox.classList.replace("set_none", "set_flex"); //지역선택박스 none -> block으로 변경
  regionSelectBox.classList.add("set_z-index_6"); //지역선택박스 Kakao map 위로 오게 설정
  goToList.classList.remove("set_none");
  local = event.target.alt;
  addRegionSelect(event.target.alt); // select태그들이 추가되도록
  map = new kakao.maps.Map(container, options); //지도 생성 및 객체 리턴
  map.setCenter(
    new kakao.maps.LatLng(
      regionData[event.target.alt][0][1],
      regionData[event.target.alt][0][2]
    )
  );
  if (needSetLevelUpLocals.includes(local)) {
    map.setLevel(9);
  }
  jsonAsync(regionSelect.value);
};

// 클릭시 커스텀 오버레이 화면에 표시
const addClosureOverlay = (marker, mypk, myname, myaddress, myphoto) => {
  overlay = new kakao.maps.CustomOverlay({
    content: overlayContent(pk, name, address, imgUrl),
    map: map,
    position: null,
  });
  return () => {
    overlay.setPosition(marker.getPosition());
    overlay.setContent(overlayContent(mypk, myname, myaddress, myphoto));
    overlay.setMap(map);
  };
};

// 커스텀 오버레이를 닫기 위해 호출되는 함수입니다
function closeOverlay() {
  overlay.setMap(null);
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
  clusterer.removeMarkers(markers);
  markers = [];
  let regionSelectedValue = regionSelect.value;
  setCenter(
    regionData[local][regionSelect.selectedIndex][1],
    regionData[local][regionSelect.selectedIndex][2]
  );
  polygonPath = [];
  polygon.setMap(null);
  for (let i in markers) {
    markers[i].setMap(null);
  }

  changePolygon(regionSelectedValue);
  overlay.setMap(null);
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
    if (region.includes("광역시")) {
      const getPolygonJson = await // 폴리곤 JSON 처리하는 부분
      $.getJSON("/static/map/js/sidoPolygon.json", function (data) {
        datas = data;
        jinjuPolygon = data.features.find((n) => {
          return n.properties.CTP_KOR_NM == region;
        }).geometry.coordinates[0];
      });
    } else {
      const getPolygonJson = await // 폴리곤 JSON 처리하는 부분
      $.getJSON("/static/map/js/regionPolygon.json", function (data) {
        datas = data;
        jinjuPolygon = data.features.find((n) => {
          return n.properties.SIG_KOR_NM == region;
        }).geometry.coordinates[0];
      });
    }
    setPath(jinjuPolygon);
    const v1 = await delete polygon;
    const v2 = await setPolygonAndAdd();
    const v3 = await setMouseInOut();
    const v4 = await getRegionData(region); // region에 해당되는 빵집데이터 갖고오기
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
  body.classList.add("set_fixed");
  delete map;
  delete polygon;
  for (let i in markers) {
    markers[i].setMap(null);
  }
  goToList.classList.add("set_none"); // 빵집리스트로이동하기 제거
  mapInit.classList.remove("set_none"); //첫 지도이미지 display:none 추가
  regionSelectBox.classList.replace("set_flex", "set_none"); //지역선택박스 none -> block으로 변경
  regionSelectBox.classList.remove("set_z-index_6"); //지역선택박스 Kakao map 위로 오게 설정
  container.remove(); // map셋팅 삭제를 위해 div map element 제거
  regionSelect.innerHTML = "";
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
  clusterer.removeMarkers(markers);
  markers = [];
  regionSelect.value = regionSelect.firstElementChild.innerText;
};
