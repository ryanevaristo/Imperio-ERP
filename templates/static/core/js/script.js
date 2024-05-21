function adjustSidebar() {
  var sidebar = document.getElementById('sidebar');
  var overlay = document.querySelector(".overlay");
  
  if (window.innerWidth > 700) {
    sidebar.classList.add("expand");
  } else {
    sidebar.classList.remove("expand");
    overlay.style.display = "block";
  }
}

// Call the function immediately on page load
adjustSidebar();

// Also call the function on window resize
window.addEventListener('resize', adjustSidebar);

const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});


