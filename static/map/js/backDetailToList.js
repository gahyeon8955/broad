const backDetailToList = () => {
  detailContent.remove();
  newContent.classList.replace("set_none", "set_block");
  document.querySelector("header").innerHTML = listHeader;
};
