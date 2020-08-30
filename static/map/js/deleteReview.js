const deleteReview = (event) => {
  event.target.parentElement.parentElement.remove();
  $.ajax({
    type: "POST",
    url: deleteReviewUrl,
    data: { pk: oneReviewPK, csrfmiddlewaretoken: csrf },
    dataType: "json",
    success: (response) => {},
  });
};
