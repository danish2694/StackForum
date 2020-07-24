from django.shortcuts import render
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from django.db.models import F
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
import uuid

from django.views.decorators.csrf import csrf_exempt
from django.db.models import Case, Value, When

def index(request):
	if request.session.has_key('user'):
		AllQuestions = Questions.objects.all().order_by('-date')
		params = {'AllQuestions':AllQuestions}
		return render(request,'index.html',params)
	else:
		return HttpResponseRedirect('/login')


def register(request):
	if request.session.has_key('user'):
		return HttpResponseRedirect('/')
	else:
		if request.method == 'POST':
			fName = request.POST.get('fName')
			lName = request.POST.get('lName')
			userId = fName + lName + str(uuid.uuid4().hex)[:10]
			password = request.POST.get('password')
			confirmPassword = request.POST.get('confirmPassword')
			gender = request.POST.get('gender')[0]
			email = request.POST.get('email')
			securityQuestion = request.POST.get('securityQuestion')
			securityAnswer = request.POST.get('securityAnswer')

			if UserDetail.objects.filter(Email=email):
				messages.success(request,f"Account Already Present with {email} !!")
				return render(request,'registerAccount.html')
			else:
				UserDetail(UserId=userId,FirstName=fName,LastName=lName,Password=make_password(password),
				SecurityQuestion=securityQuestion,SecurityAnswer=securityAnswer,Gender=gender,Email=email).save()
				messages.success(request,f"Welcome Aboard: {fName} {lName} !!")
				return render(request,'registerAccount.html')
		else:
			return render(request,'registerAccount.html')

def login(request):
	if request.method == 'POST':
		email = request.POST.get("email")
		password = request.POST.get("password")
		try:
			loginValidate = UserDetail.objects.get(Email=email)
			encryptPass = loginValidate.Password
		except:
			return HttpResponseRedirect('/login')

		if check_password(password,encryptPass) == True:
			request.session['user'] = str(loginValidate.UserId)
			
			return HttpResponseRedirect('/')
		else:
			return render(request,'signin.html',{'message':'Please Check Your Email and Password'})
	else:
		if request.session.has_key('user'):
			return HttpResponseRedirect('/')
		else:
			return render(request,'signin.html')

def test(request):
	del request.session['user']
	return HttpResponse('done')


@csrf_exempt
def askaquestion(request):
	questionVal = request.POST.get('questionValue')
	user = UserDetail.objects.get(UserId=request.session['user'])
	Questions(userId=request.session['user'],question=questionVal,User=user).save()
	return JsonResponse({'Result':'Success'})

@csrf_exempt
def vote(request):
	questionId = request.POST.get('questionId')
	action = request.POST.get('action')
	if action == 'up':
		voteType = 1
	voteData = Questions.objects.get(questionId=questionId).voteDetails
	print(voteData)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	# elif action == 'down':
	# 	voteType = -1
	# else:
	# 	pass
	
	# if Votes.objects.using('second').filter(questionId=questionId,userId=userId).exists():
	# 	Votes.objects.using('second').filter(questionId=questionId,userId=request.session['user']
	# 	).update(voteType=Case(
	# 		When(voteType=1, then=Value(-1)),
	# 		When(voteType=-1,then=Value(1)),
	# 	)

	# else:
	# 	Votes(questionId=questionId,userId=request.session['user'],voteType=voteType).save(using='second')


	if action == 'up':
		vote, is_created = Votes.objects.get_or_create(questionId=questionId,userId=request.session['user'],voteType=1)
		if is_created:
			vote = Questions.objects.get(questionId=questionId).votes
			vote += 1
			Questions.objects.filter(questionId=questionId).update(votes=vote)

		# Questions.objects.filter(questionId=questionId).update(votes=F('votes') + 1)
	elif action == 'down':
		vote = Questions.objects.get(questionId=questionId).votes
		vote = vote - 1
		Questions.objects.filter(questionId=questionId).update(votes=vote)
		
	print(questionId,action)
	return HttpResponse('done')


