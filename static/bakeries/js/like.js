const like = document.querySelector(".jsLike");

const changeLikeDB = () => {
  $.ajax({
    type: "POST",
    url: ajaxLikeUrl,
    data: { pk: bakeryPK, csrfmiddlewaretoken: csrf },
    dataType: "json",
  });
};

const clickLike = () => {
  if (like.src === "http://127.0.0.1:8000/static/bakeries/img/heart.png") {
    like.src = "http://127.0.0.1:8000/static/bakeries/img/white_heart.png";
  } else {
    like.src = "http://127.0.0.1:8000/static/bakeries/img/heart.png";
  }
  changeLikeDB();
};
