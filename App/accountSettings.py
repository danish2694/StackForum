from .models import *
from django.contrib.auth.hashers import make_password, check_password

def registerNewAccount(**kwargs):
    fName = kwargs['fName']
    lName = kwargs['lName']
    userId = fName + lName + str(uuid.uuid4().hex)[:10]
    
    email = kwargs['email']
    mobile = kwargs['mobile']
    age = kwargs['age']
    password = kwargs['password']
    confirmPassword = kwargs['confirmPassword']
    gender = kwargs['gender']
    securityQuestion = kwargs['securityQuestion']
    securityAnswer = kwargs['securityAnswer']


    if UserDetail.objects.filter(Email=kwargs['email']):
        message = (f"Account Already Present with {email} !!")
        return message
        
    else:
        UserDetail(UserId=userId,FirstName=fName,LastName=lName,Password=make_password(password),
        SecurityQuestion=securityQuestion,SecurityAnswer=securityAnswer,Gender=gender,Email=email).save()
        message = (f"Welcome Aboard: {fName} {lName} !!")
        return message

def loginToAccount(**kwargs):
    email = kwargs['email']
    password = kwargs['password']
    try:
        loginValidate = UserDetail.objects.get(Email=email)
        encryptPass = loginValidate.Password
    except:
        return False
        
    if check_password(password,encryptPass) == True:
        return str(loginValidate.UserId)
    
    else:
        return False
        