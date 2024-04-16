const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});


$document.ready(function(){
  $.ajax({
      url: "{% url 'financeiro:total_despesas' %}",
      type: 'GET',
      success: function(response){
          console.log(response)
      }
  });
});
