const header = document.querySelector("header");
const footer = document.querySelector("footer");
let newContent;
let currentRegion;
let bakeryListData;
let beforeHeader;

const headerHTML = (cr) => {
  return `
<div class="header__wrapper">
    <div class="header__leftbox">
        <img onclick="backListToMap()" class="left_arrow" src="${arrowSrc}"
            alt="left_arrow icon">
    </div>
    <div class="header__midbox">
        <span class="header__title">${cr} 빵집</span>
    </div>
    <div class="header__rightbox">
    </div>
</div>
`;
};

const htmlTagSet = (
  pk,
  index,
  name,
  sub_name,
  address,
  total_rating,
  review_count
) => {
  return `
<div onclick="goToBakeryDetail(${pk})" class="list_store">
    <div class="store_rank">${parseInt(index) + 1} </div>
    <div class="store_detail">
        <div class="detail_top">
            <span class="top_name">${name}</span>
        </div>
        <div class="detail_explain">${sub_name}</div>
        <div class="detail_address">${address}</div>
    </div>
    <div class="store_review">
        <div class="review_score">
            <span class="score_star">★</span>
            <span class="score_number"><span class="jsCount">${
              total_rating != 0 ? total_rating.toFixed(1) : "&nbsp;&nbsp;-"
            }</span></span>
        </div>
        <div class="review_number">
            <span class="review_count">리뷰 ${review_count}</span>
        </div>
    </div>
</div>
`;
};

const setBakeryListData = () => {
  if (bakeryListData.result === "none") {
  } else {
    for (const i in bakeryListData.obj) {
      ListElement.insertAdjacentHTML(
        "beforeend",
        htmlTagSet(
          bakeryListData.obj[i].pk,
          i,
          bakeryListData.obj[i].fields.name,
          bakeryListData.obj[i].fields.sub_name,
          bakeryListData.obj[i].fields.address,
          bakeryListData.counts.rating[i],
          bakeryListData.counts.review[i]
        )
      );
    }
  }
};

const ajaxCallData = (currentRegion) => {
  $.ajax({
    type: "GET",
    url: getBakeryListDataUrl,
    data: { region: currentRegion },
    dataType: "json",
    success: (response) => {
      bakeryListData = response;
      return setBakeryListData();
    },
  });
};

const clickGoToList = () => {
  body.classList.add("height_auto", "overflow_none");
  content.classList.add("set_none");
  currentRegion = regionSelect.value;
  beforeHeader = header.innerHTML;
  header.innerHTML = headerHTML(currentRegion);
  content.insertAdjacentHTML(
    "beforebegin",
    `
    <div class="content newContent set_base_content_padding">
      <div class="list jsList">
      </div>
    </div>
    `
  );
  newContent = document.querySelector(".newContent");
  newContent.classList.add("set_block");
  ListElement = document.querySelector(".jsList");
  ajaxCallData(currentRegion);
};
