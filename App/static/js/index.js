// function openCity(evt, cityName) {
//     // Declare all variables
//     var i, tabcontent, tablinks;
  
//     // Get all elements with class="tabcontent" and hide them
//     tabcontent = document.getElementsByClassName("tabcontent");
//     for (i = 0; i < tabcontent.length; i++) {
//       tabcontent[i].style.display = "none";
//     }
  
//     // Get all elements with class="tablinks" and remove the class "active"
//     tablinks = document.getElementsByClassName("tablinks");
//     for (i = 0; i < tablinks.length; i++) {
//       tablinks[i].className = tablinks[i].className.replace(" active", "");
//     }
  
//     // Show the current tab, and add an "active" class to the button that opened the tab
//     // document.getElementById(cityName).style.display = "block";
//     evt.currentTarget.className += " active";
//   }


  // function openCity1(evt, cityName) {
  //   // Declare all variables
  //   var i, tabcontent, tablinks;
  
  //   // Get all elements with class="tabcontent" and hide them
  //   tabcontent = document.getElementsByClassName("tabcontent1");
  //   for (i = 0; i < tabcontent.length; i++) {
  //     tabcontent[i].style.display = "none";
  //   }
  
  //   // Get all elements with class="tablinks" and remove the class "active"
  //   tablinks = document.getElementsByClassName("tablinks1");
  //   for (i = 0; i < tablinks.length; i++) {
  //     tablinks[i].className = tablinks[i].className.replace(" active", "");
  //   }
  
  //   // Show the current tab, and add an "active" class to the button that opened the tab
  //   document.getElementById(cityName).style.display = "block";
  //   evt.currentTarget.className += " active";
  // }

// For adding new question
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


//  for votes on questions
function votes(val){
  if (!is_flag().Result){
    alert('You need to login before voting')
  }
  else{
  var res = val.split("--");
  console.log(res);
  $.ajax({
    method:'POST',
    url:'/votes/vote/',

    data:{
      questionId : res[1],
      action : res[0],
    },
    success:function(e){
      if(!e.flag){
        alert(e.Response);
      }
      else{
      $('#'+res[1]).html(parseInt($('#'+res[1]).html()) + parseInt(e.count))
      alert(e.Response);
      }
      
    },
    error:function(e){
      console.log("Fail");
    }
});
  } // else ends
}

// for answer votes

$('.vote').on('click',function(e){
  if (!is_flag().Result){
    alert('You need to login before voting')
  }
  else{
  var answerId = $(this).attr("data-href");
    console.log($(this).attr("name"),answerId);

  $.ajax({
    method:'POST',
    url:'/votes/answervote/',
    data:{
      questionId:$(this).attr("data-value"),
      answerId:answerId,
      action:$(this).attr("name"),
    },
    success:function(e){
      if(!e.flag){
        alert(e.Response);
      }
      else{      
      $('#'+answerId).html(parseInt($('#'+answerId).html()) + parseInt(e.count))
      alert(e.Response);
      }
    },
    error:function(e){
      console.log('error')
    }
  })

 }
})


function is_flag(){
  var result = false;
  $.ajax({
    method:'POST',
    url:'/sessionval/',
    data:{},
    async: false,
    success:function(e){
      result = e;
    },
    error:function(e){
      console.log('error',e)
    }
  })
  return result;
}

// for validating question modal with session
$('#questionModalButton').on('click',function(e){
  // console.log(is_flag(result))
  if (!is_flag()){
    alert('Please Login to Continue!');
  }
  else{}
})
  

// for validating answer textarea // form submit only with some valid value
$('#answerbtn').on('click',function(e){
  
  if(!$('#answertext').val().replace(/\s/g, "").length){
    alert('Answer Cannot be Blank');
    e.preventDefault();
  }
  else{
    if (is_flag()){
    $('#answersubmit').submit();
    }
    else{ 
      alert('Please login before answering.')
      e.preventDefault();
    }
    
  }
})

// "Answer" button show and hide
$("#answertext").keyup(function(){
  if(!$(this).val().replace(/\s/g, "").length){
    document.getElementById('answerbtn1').style.display = 'none';
  console.log("blank");
  }
  else{
    console.log($(this).val());
    document.getElementById('answerbtn1').style.display = 'block';
  }
});

// $('.answer').on('click',function(e){
//   var v =  $(this).attr("data-href");
//   // console.log(v);
//   input = document.getElementById(v);
//   input.style.display = 'block';
// })

// console.log(v)
// $('#'+v).on('keypress',function(e){
//   answer = $(this).val()
//   if(e.which === 13){
    

//     event.preventDefault();
  
//     $.ajax({
//     method:'POST',
//     url: $(this).attr('action') ,
//     // url : '/postanswer/',
//     data: $(this).serialize(),
//     dataType : 'json',
//     success:function(e){
//       console.log(e)
//     },
//     error:function(e){
//       console.log("Fail");
//     }
//   });
//   }    
//   });