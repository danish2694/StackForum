function validateform(){  
    var pass=document.myform.password.value;
    var cpass=document.myform.confirmPassword.value;
    // alert(pass+cpass);
    
    if (pass!=cpass){  
      alert("Passwords do not match"); 
    return false;  
    }
    
  }


