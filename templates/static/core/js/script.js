const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});


$(document).ready(function() {
  // messages timeout for 10 sec 
  setTimeout(function() {
      $('.message alert alert-danger').fadeOut('slow');
  }, 10000); // <-- time in milliseconds, 1000 =  1 sec

  // delete message
  $('.del-msg').live('click',function(){
      $('.del-msg').parent().attr('style', 'display:none;');
  })
});