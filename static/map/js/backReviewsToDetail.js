const backReviewsToDetail = () => {
  reviewsContent.remove();
  detailContent.classList.replace("set_none", "set_block");
  document.querySelector("header").innerHTML = detailHeader;
};
