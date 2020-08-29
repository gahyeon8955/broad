const listElement = document.querySelector(".list");
const soboro = document.querySelector(".jsSoboro");
const rollcake = document.querySelector(".jsRollcake");
const makarong = document.querySelector(".jsMakarong");
const cookie = document.querySelector(".jsCookie");
let pickedData;

const listInfoHTML = (
  pk,
  index,
  name,
  subName,
  address,
  totalRating,
  reviewCount
) => {
  return `
<a href="/bakery/${pk}" class="list_store">
  <div class="store_rank">${index}</div>
  <div class="store_detail">
      <div class="detail_top">
          <span class="top_name">${name}</span>
      </div>
      <div class="detail_explain">${subName.substr(0, 25)}</div>
      <div class="detail_address">${address}</div>
  </div>
  <div class="store_review">
      <div class="review_score">
          <span class="score_star">★</span>
          <span class="score_number">${
            totalRating != 0 ? totalRating.toFixed(1) : "&nbsp;&nbsp;-"
          }</span>
      </div>
      <div class="review_number">
          <span class="review_count">리뷰 ${reviewCount}</span>
      </div>
  </div>
</a>
`;
};

const addInfo = (JSONData) => {
  const listStoreElement = document.querySelectorAll(".list_store");
  for (const i of listStoreElement) {
    i.remove();
  }
  for (let i in JSONData) {
    listElement.insertAdjacentHTML(
      "beforeend",
      listInfoHTML(
        JSONData[i].pk,
        parseInt(i) + 1,
        JSONData[i].fields.name,
        JSONData[i].fields.sub_name,
        JSONData[i].fields.address,
        JSONData[i].fields.temp_total_rating,
        JSONData[i].fields.temp_review_count
      )
    );
  }
};

const clickCategory = async (bread) => {
  let eng_bread;
  if (bread === "소보로빵") {
    eng_bread = "soboro";
    if (soboro.classList.contains("opacity_1")) {
    } else {
      rollcake.classList.remove("opacity_1");
      makarong.classList.remove("opacity_1");
      cookie.classList.remove("opacity_1");
      soboro.classList.add("opacity_1");
    }
  } else if (bread === "롤케이크") {
    eng_bread = "rollcake";
    if (rollcake.classList.contains("opacity_1")) {
    } else {
      soboro.classList.remove("opacity_1");
      makarong.classList.remove("opacity_1");
      cookie.classList.remove("opacity_1");
      rollcake.classList.add("opacity_1");
    }
  } else if (bread === "마카롱") {
    eng_bread = "makarong";
    if (makarong.classList.contains("opacity_1")) {
    } else {
      rollcake.classList.remove("opacity_1");
      soboro.classList.remove("opacity_1");
      cookie.classList.remove("opacity_1");
      makarong.classList.add("opacity_1");
    }
  } else if (bread === "쿠키") {
    eng_bread = "cookie";
    if (cookie.classList.contains("opacity_1")) {
    } else {
      rollcake.classList.remove("opacity_1");
      makarong.classList.remove("opacity_1");
      soboro.classList.remove("opacity_1");
      cookie.classList.add("opacity_1");
    }
  }

  try {
    const get = await $.getJSON(
      `http://127.0.0.1:8000/bakery/${eng_bread}-data/`,
      (data) => {
        pickedData = data;
      }
    );
    const setting = await addInfo(pickedData);
  } catch {
  } finally {
  }
};

$.getJSON(`http://127.0.0.1:8000/bakery/soboro-data/`, (data) => {
  addInfo(data);
});
