let reviewsData;
let reviewsContent;
let oneReviewPK;

const setReviewsHeader = () => {
  document.querySelector("header").innerHTML = `
<div class="header__wrapper">
    <div class="header__leftbox">
        <img onclick="backReviewsToDetail()" class="left_arrow" src="${arrowSrc}"
            alt="left_arrow icon">
    </div>
    <div class="header__midbox">
        <span class="header__title">${reviewBakeryName}</span>
    </div>
    <div class="header__rightbox">
    </div>
</div>
`;
};

const StartDeleteReview = (pk) => {
  oneReviewPK = pk;
  return deleteReview(event);
};

const setReviews = () => {
  for (const i in reviewsData.reviews) {
    reviewsContent.insertAdjacentHTML(
      "beforeend",
      `
      <div class="bakery_review_detail">
        <div class="bakery_review_detail_topbox">
            <div class="bakery_review_left">
                <div class="bakery_review_profileimg"><img src="${
                  reviewsData.photos[i]
                }"></div>
                <div class="bakery_review_id_box">
                    <div class="bakery_review_id">${
                      reviewsData.nicknames[i]
                    }</div>
                    <div class="bakery_review_time">${
                      reviewsData.created_date[i]
                    }</div>
                </div>
                <div class="bakery_review_star">${reviewsData.reviews[
                  i
                ].fields.rating.toFixed(1)}</div>
            </div>
            ${
              reviewsData.is_equal_writer_and_login[i] === true
                ? `<img onclick="StartDeleteReview(${reviewsData.reviews[i].pk})" class="delete_trash_icon" src="${trashSrc}" alt="쓰레기통 아이콘">`
                : ``
            }
        </div>
        <div class="bakery_review_comment">${
          reviewsData.reviews[i].fields.body
        }</div>
      </div>
      `
    );
  }
};

const setReviewWriteBox = (review_count) => {
  reviewsContent.innerHTML = `
    <div class="review_write_box">
        <div class="review_left_box">
            <div class="bakery_review">리뷰</div>
            <div class="bakery_review_count">${review_count}</div>
        </div>
        <a href="/bakery/review-write/${pk}/">
            <div class="bakery_review_write">리뷰 작성하기</div>
        </a>
    </div>
    `;
};

const ajaxCallReviewsData = (pk, review_count) => {
  $.ajax({
    type: "GET",
    url: getBakeryDetailReviewsDataUrl,
    data: { pk },
    dataType: "json",
    success: (response) => {
      reviewsData = response;
      setReviewWriteBox(review_count);
      setReviews();
      setReviewsHeader();
    },
  });
};

const goDetailToReviews = (pk, review_count) => {
  console.log(pk, "리뷰도착");
  detailContent.classList.replace("set_block", "set_none");
  detailContent.insertAdjacentHTML(
    "beforebegin",
    `
    <div class="content reviewsContent set_block"></div>
    `
  );
  reviewsContent = document.querySelector(".reviewsContent");
  ajaxCallReviewsData(pk, review_count);
};
