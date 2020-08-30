const backDetailToMap = () => {
  body.classList.remove("overflow_none", "height_auto");
  detailContent.remove();
  content.classList.remove("set_none");
  document.querySelector("header").innerHTML = mapHeader;
};
