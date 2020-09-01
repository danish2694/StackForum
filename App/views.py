from django.shortcuts import render
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from django.db.models import Count
from .models import *
from . import accountSettings
from django.contrib.auth.hashers import make_password, check_password
import uuid
from django.contrib import messages

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
			
			email = request.POST.get('email')
			mobile = request.POST.get('mobile')
			age = request.POST.get('age')
			password = request.POST.get('password')
			confirmPassword = request.POST.get('confirmPassword')
			gender = request.POST.get('gender')[0]
			securityQuestion = request.POST.get('securityQuestion')
			securityAnswer = request.POST.get('securityAnswer')

			account_register_report = accountSettings.registerNewAccount(
				fName=fName,lName=lName,email=email,mobile=mobile,age=age,password=password,confirmPassword=confirmPassword,
				gender=gender,securityQuestion=securityQuestion,securityAnswer=securityAnswer
			)
			messages.success(request,account_register_report)
			return render(request,'registerAccount.html')
		else:
			return render(request,'registerAccount.html')

def login(request):
	if request.method == 'POST':
		email = request.POST.get("email")
		password = request.POST.get("password")
		login_status = accountSettings.loginToAccount(
			email=email,password=password
		)
		if not login_status:
			return render(request,'signin.html',{'message':'Please Check Your Email and Password'})
		else:
			request.session['user'] = login_status
			return HttpResponseRedirect('/')
		
	else:
		if request.session.has_key('user'):
			return HttpResponseRedirect('/')
		else:
			return render(request,'signin.html')

def logout(request):
	if request.session.has_key('user'):
		del request.session['user']
		return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/')

@csrf_exempt
def askaquestion(request):
	questionVal = request.POST.get('questionValue')
	user = UserDetail.objects.get(UserId=request.session['user'])
	Questions(question=questionVal,User=user).save()
	return JsonResponse({'Result':'Success'})

def answer(request,id):
	questionData = Questions.objects.get(questionId=id)
	AllAnswers = questionData.answers
	params = {'AllAnswers':AllAnswers,'questionData':questionData}
	return render(request,'answers.html',params)
	
@csrf_exempt
def postanswer(request):
	qid = request.POST.get('questionId')
	answer = request.POST.get('answer')
	answerId = uuid.uuid4()
	questionObj = Questions.objects.get(questionId=qid)
	if not questionObj.answers:
		questionObj.answers = [{
		'answerId':answerId,'answer':answer,
		'totalVotes':0,'date':datetime.datetime.now(),'User':request.session['user']
		}]
	else:
		questionObj.answers.append({
			'answerId':answerId,'answer':answer,
			'totalVotes':0,'date':datetime.datetime.now(),'User':request.session['user']
		})
	questionObj.save()
	
	return HttpResponseRedirect('/answer/'+qid+'/')