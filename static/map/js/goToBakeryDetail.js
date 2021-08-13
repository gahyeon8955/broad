let listHeader;
let detailData;

const setBakeryReviews = () => {
  const reviewBoxs = document.querySelector(".bakery_review_smallbox");
  for (const i in detailData.reviews) {
    reviewBoxs.insertAdjacentHTML(
      "beforeend",
      `
        <div class="bakery_review_detail">
            <div class="bakery_review_detail_topbox">
                <div class="bakery_review_profileimg"><img src="${
                  detailData.reviews[i].user_img
                }"></div>
                <div class="bakery_review_id_box">
                    <div class="bakery_review_id">${
                      detailData.reviews[i].user_nickname
                    }</div>
                    <div class="bakery_review_time">${
                      detailData.reviews[i].created_date
                    }</div>
                </div>
                <div class="bakery_review_star">${detailData.reviews[
                  i
                ].user_rating.toFixed(1)}</div>
            </div>
            <div class="bakery_review_comment">${
              detailData.reviews[i].body
            }</div>
        </div>
        `
    );
  }
};

const setBakeryMenus = () => {
  const menuBox = document.querySelector(".bakery_menu_detail_box");
  for (const i in detailData.menus) {
    let price = detailData.menus[i].fields.row_price;
    let strPrice = String(price);
    if (price >= 100000) {
      price = `${strPrice.substring(0, 3)},${strPrice.substring(3, 6)}`;
    } else if (price >= 10000) {
      price = `${strPrice.substring(0, 2)},${strPrice.substring(2, 5)}`;
    } else if (price >= 1000) {
      price = `${strPrice.substring(0, 1)},${strPrice.substring(1, 4)}`;
    }
    menuBox.insertAdjacentHTML(
      "beforeend",
      `
      <div class="bakery_menu_detail1">
        <div class="bakery_menu_name">${detailData.menus[i].fields.name}</div>
        <div class="bakery_menu_price">${price}</div>
      </div>
      `
    );
  }
};

const setBakeryImages = () => {
  const imgBoxs = document.querySelector(".bakery_bread_image_box");
  for (const i in detailData.photos) {
    imgBoxs.insertAdjacentHTML(
      "beforeend",
      `
        <img class="bakery_bread_image" src="/media/${detailData.photos[i].fields.photo}">
      `
    );
  }
};

const setDetailHeader = () => {
  document.querySelector("header").innerHTML = `
    <div class="header__wrapper">
      <div class="header__leftbox">
          <img onclick="backDetailToList()" class="left_arrow" src="${arrowSrc}"
              alt="left_arrow icon">
      </div>
      <div class="header__midbox">
          <span class="header__title">${detailData.bakery.fields.name}</span>
      </div>
      <div class="header__rightbox">
      </div>
    </div>
    `;
};

const setDetailHTML = () => {
  return `
<div class="content detailContent set_block set_base_content_padding">
    <!-- 가게 대표 빵 이미지 사진들 -->
    <div class="bakery_bread_image_box">
    </div>

    <div class="bakery_information_box">
        <div class="bakery_box">
            <!-- 가게 로고 -->
            <img class="bakery_trademark_detail" src="/media/${
              detailData.bakery.fields.logo
            }">
            <!-- 가게 이름, 정보, 평점 -->
            <div class="bakery_name_box">
                <div class="bakery_name_and_star">
                    <div class="bakery_name">${
                      detailData.bakery.fields.name
                    }</div>
                    <div class="bakery_star">${
                      detailData.total_rating != 0
                        ? detailData.total_rating.toFixed(1)
                        : "&nbsp;&nbsp;-"
                    }</div>
                </div>
                <div class="bakery_number">${
                  detailData.bakery.fields.phone_number
                }</div>
                <div class="bakery_business_hours">${
                  detailData.bakery.fields.business_hour
                }</div>
            </div>
            <!-- 찜 -->
            <div class="bakery_like">
                <img onclick="clickLike()" class="bakery_like_img jsLike" src="${
                  detailData.is_liked === true ? heartSrc : whiteHeartSrc
                }">
            </div>
        </div>

        <!-- 가게 위치 박스 -->
        <div class="bakery_location_box">
            <div id="detailMap" class="bakery_location"></div>
            <div class="bakery_location_address">${
              detailData.bakery.fields.address
            }</div>
        </div>

        <!-- 가게 메뉴 박스 -->
        <div class="bakery_menu_box">
            <div class="bakery_menu">대표메뉴</div>
            <div class="bakery_menu_detail_box">
            </div>
        </div>

        <!-- 가게 리뷰 박스 -->
        <div class="bakery_review_bigbox">
            <div class="review_write_box">
                <div class="review_left_box">
                    <div class="bakery_review">리뷰</div>
                    <div class="bakery_review_count">${
                      detailData.review_count
                    }</div>
                </div>
                <a onclick="goDetailToReviews(
                  ${detailData.bakery.pk},
                  ${detailData.review_count})">
                    <div class="bakery_review_write">리뷰 더보기</div>
                </a>
            </div>
            <div class="bakery_review_smallbox">
            </div>
        </div>

    </div>
</div>
`;
};

const ajaxCallDetailData = (pk) => {
  bakeryPK = pk;
  $.ajax({
    type: "GET",
    url: getBakeryDetailDataUrl,
    data: { pk },
    dataType: "json",
    success: (response) => {
      detailData = response;
      reviewBakeryName = detailData.bakery.fields.name;
      newContent.insertAdjacentHTML("beforebegin", setDetailHTML());
      listHeader = document.querySelector("header").innerHTML;
      detailContent = document.querySelector(".detailContent");
      setDetailHeader();
      detailHeader = document.querySelector("header").innerHTML;
      setBakeryImages();
      setBakeryMenus();
      setBakeryReviews();
      mapLat = detailData.bakery.fields.lat;
      mapLng = detailData.bakery.fields.lng;
      bakeryDetailMap();
    },
  });
};

const goToBakeryDetail = (pk) => {
  overlay.setMap(null);
  newContent.classList.replace("set_block", "set_none");
  ajaxCallDetailData(pk);
};
