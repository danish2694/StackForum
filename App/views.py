from django.shortcuts import render
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from django.db.models import F, Q, Count
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
import uuid
from itertools import zip_longest
from App import votes
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Case, Value, When
import datetime

@csrf_exempt
def sessionval(request):
	if request.session.has_key('user'):
		return JsonResponse({'Result':True})
	else:
		return JsonResponse({'Result':False})
def recent(request):
	recentQuestions = Questions.objects.all().order_by('-date')
	params = {'AllQuestions':recentQuestions,'class_':'recent'}
	return render(request,'index.html',params)

def mostAnswered(request):
	mostAnswered = Questions.objects.annotate(count=Count('answers')).order_by('-count')
	params = {'AllQuestions':mostAnswered,'class_':'mostAnswered'}
	return render(request,'index.html',params)

def mostVisited(request):
	mostVisited = Questions.objects.annotate(count=Count('Views')).order_by('-count')
	params = {'AllQuestions':mostVisited,'class_':'mostVisited'}
	return render(request,'index.html',params)

def mostPopular(request):
	mostPopular = Questions.objects.all().order_by('-totalVotes','-Views')
	params = {'AllQuestions':mostPopular,'class_':'mostPopular'}
	return render(request,'index.html',params)

def index(request):
	recentQuestions = Questions.objects.all().order_by('-date')
	params = {'AllQuestions':recentQuestions,'class_':'recent'}
	return render(request,'index.html',params)
	

def register(request):
	if request.session.has_key('user'):
		return HttpResponseRedirect('/')
	else:
		if request.method == 'POST':
			fName = request.POST.get('fName')
			lName = request.POST.get('lName')
			userId = fName + lName + str(uuid.uuid4().hex)[:10]
			email = request.POST.get('email')
			mobile = request.POST.get('mobile')
			age = request.POST.get('age')
			password = request.POST.get('password')
			confirmPassword = request.POST.get('confirmPassword')
			gender = request.POST.get('gender')[0]
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
	# return HttpResponse('done')
	return render(request,'answers.html')


@csrf_exempt
def askaquestion(request):
	questionVal = request.POST.get('questionValue')
	user = UserDetail.objects.get(UserId=request.session['user'])
	Questions(question=questionVal,User=user).save()
	return JsonResponse({'Result':'Success'})

@csrf_exempt
def vote(request):	
	questionId = request.POST.get('questionId')
	action = request.POST.get('action')
	loggedUser = request.session['user']

	output = votes.questionVotes(questionId,action,loggedUser)
	
	return JsonResponse(output)

def answer(request,id):
	questionData = Questions.objects.get(questionId=id)
	AllAnswers = questionData.answers
	params = {'AllAnswers':AllAnswers,'questionData':questionData}
	return render(request,'answers.html',params)

@csrf_exempt
def answervote(request):
	questionid = request.POST.get('questionId')
	answerid = request.POST.get('answerId')
	action = request.POST.get('action')
	
	questionObj = Questions.objects.get(questionId=questionid)
	allAnswers = questionObj.answers
	for ans in allAnswers:
		if str(ans['answerId']) == answerid:
			voteCount =  ans['totalVotes']

	if action == 'up':
		voteType = 1
	elif action == 'down':
		voteType = -1
	else:
		pass

	voteRecord = AnswerVotes.objects.using('second').filter(answerId=answerid,userId=request.session['user'])
	
	upVoteRecord = voteRecord.using('second').filter(voteType=1)
	
	downVoteRecord = voteRecord.using('second').filter(voteType=-1)
	
	
	
	if upVoteRecord and action == 'up':
		print('1')
		msg = 'Already Upvoted'; count = 0
		pass
	
	elif upVoteRecord and action == 'down':
		print('2')
		msg = 'You downvoted this question'; count = -1
		ans['totalVotes'] -= 1
		print(questionObj)
		questionObj.save()
	
	elif downVoteRecord and action == 'down':
		print('3')
		msg = 'Already Downvoted'; count = 0
		pass
	
	elif downVoteRecord and action == 'up':
		print('4')
		msg = 'You upvoted this question'; count = 1
		ans['totalVotes'] += 1
		questionObj.save()

	if voteRecord and action == 'up':
		AnswerVotes.objects.using('second').filter(answerId=answerid,userId=request.session['user']
		).update(voteType=Case(
			When(voteType=1, then=Value(1)),
			When(voteType=-1,then=Value(1)),
		))
		
	elif voteRecord and action == 'down':
		AnswerVotes.objects.using('second').filter(answerId=answerid,userId=request.session['user']
		).update(voteType=Case(
			When(voteType=1, then=Value(-1)),
			When(voteType=-1,then=Value(-1)),
		))
		
	else:
		AnswerVotes(answerId=answerid,userId=request.session['user'],voteType=voteType).save(using='second')
		# Questions.objects.filter(questionId=questionId).update(totalVotes = voteCount + voteType)
		
		ans['totalVotes'] += voteType
		print(ans['totalVotes'] + voteType)
		print(questionObj)
		questionObj.save()
		msg = 'You ' + action + 'voted this question'; count = voteType
		
	return JsonResponse({'Response':msg,'count':count,'action':action})

	
@csrf_exempt
def postanswer(request):
	qid = request.POST.get('questionId')
	answer = request.POST.get('answer')
	answerId = uuid.uuid4()
	questionObj = Questions.objects.get(questionId=qid)
	questionObj.answers.append({
		'answerId':answerId,'answer':answer,
		'totalVotes':0,'date':datetime.datetime.now(),'User':request.session['user']
	})
	questionObj.save()
	
	return HttpResponseRedirect('/answer/'+qid+'/')