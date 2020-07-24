function openCity(evt, cityName) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
  }


  function openCity1(evt, cityName) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent1");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks1");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
  }

// $(document).on('submit','#myform',function (e) {
$("#questionbtn").on('click',function(e){
  $("#question").empty();
  questionValue = document.getElementById('question').value;

  $.ajax({
        method:'POST',
        url:'/askaquestion/',

        data:{
          questionValue:questionValue,
        },
        success:function(e){
          
        },
        error:function(e){
          console.log("Fail");
        }
    });

});


function votes(val){
  var res = val.split("--");
  console.log(res);
  $.ajax({
    method:'POST',
    url:'/vote/',

    data:{
      questionId : res[1],
      action : res[0],
    },
    success:function(e){
      
    },
    error:function(e){
      console.log("Fail");
    }
});
}

	