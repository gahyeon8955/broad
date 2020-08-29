const header = document.querySelector("header");
let currentRegion;
let bakeryListData;
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
<a href="/bakery/${pk}/" class="list_store">
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
</a>
`;
};

const setBakeryListData = () => {
  if (bakeryListData.result === "none") {
  } else {
    for (const i in bakeryListData.obj) {
      console.log(bakeryListData.obj[i].pk);
      console.log(bakeryListData.obj[i].fields.name);
      console.log(bakeryListData.obj[i].fields.sub_name);
      console.log(bakeryListData.obj[i].fields.address);
      console.log(bakeryListData.counts.rating[i]);
      console.log(bakeryListData.counts.review[i]);
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
  content.classList.add("set_block");
  currentRegion = regionSelect.value;
  header.innerHTML = headerHTML(currentRegion);
  content.innerHTML = `
<div class="list jsList"></div>
  `;
  ListElement = document.querySelector(".jsList");
  ajaxCallData(currentRegion);
};
