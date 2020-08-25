const like = document.querySelector(".jsLike");
let bakeryPK;

const changeLikeDB = () => {
  $.ajax({
    type: "POST",
    url: ajaxLikeUrl,
    data: { pk: bakeryPK, csrfmiddlewaretoken: csrf },
    dataType: "json",
  });
};

const clickLike = (event) => {
  const listBox = event.target.parentElement.parentElement.parentElement;
  bakeryPK = listBox.id;
  changeLikeDB();
  listBox.remove();
};
