// Gets all the objects with te class "caret"
var toggler = document.getElementsByClassName("caret");
var i;

for (i = 0; i < toggler.length; i++) {
  // Adds a click listener to the elements with the class "caret".
  toggler[i].addEventListener("click", function() {
    // When clicked it will change the classes "nested" and "caret" to "active_nest" and "caret-down" respectively.
    this.parentElement.querySelector(".nested").classList.toggle("active_nest");
    this.classList.toggle("caret-down");
  });
}