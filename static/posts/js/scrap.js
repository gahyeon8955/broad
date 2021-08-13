const scrap = document.querySelector(".jsScrap");
const scrapImg = document.querySelector(".jsScrapImg");
const scrapText = document.querySelector(".jsScraptext");

const changeScrapDB = () => {
  $.ajax({
    type: "POST",
    url: ajaxScrapUrl,
    data: { pk: postPK, csrfmiddlewaretoken: csrf },
    dataType: "json",
  });
};

const clickScrap = () => {
  if (scrapImg.src === "http://127.0.0.1:8000/static/posts/img/star.png") {
    scrapImg.src = "http://127.0.0.1:8000/static/posts/img/white_star.png";
    scrapText.classList.remove("text-color-gold");
    scrap.classList.remove("border-color-gold");
  } else {
    scrapImg.src = "http://127.0.0.1:8000/static/posts/img/star.png";
    scrapText.classList.add("text-color-gold");
    scrap.classList.add("border-color-gold");
  }
  changeScrapDB();
};
