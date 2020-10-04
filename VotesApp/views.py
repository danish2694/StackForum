# from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from App.models import *
from django.db.models import Case, Value, When

@property
def loggedUser(request):
	if request.session.has_key('user'):
		return request.session['user']
	else:
		return None

@csrf_exempt
def vote(request):	
	questionId = request.POST.get('questionId')
	action = request.POST.get('action')

	question_posted_by = Questions.objects.get(questionId=questionId).User.UserId
	score_of_person_voting = UserDetail.objects.get(UserId=loggedUser(request)).Score
	question_owner_score = Questions.objects.get(questionId=questionId).User.Score

	if question_posted_by == loggedUser(request):
		return JsonResponse({'Response':"You can't vote your own Question",'flag':False})
	elif score_of_person_voting < 10:
		return JsonResponse({'Response':"You don't have enough score!",'flag':False})
		
	if action == 'up':
		voteType = 1
		total_score_change = 10
	elif action == 'down':
		voteType = -1
		total_score_change = -10
	else:
		pass

	voteRecord = QuestionVotes.objects.using('second').filter(questionId=questionId,userId=loggedUser(request))

	upVoteRecord = voteRecord.using('second').filter(voteType=1)

	downVoteRecord = voteRecord.using('second').filter(voteType=-1)

	voteCount = Questions.objects.get(questionId=questionId).totalVotes

	if upVoteRecord and action == 'up':
		print('1')
		msg = 'Already Upvoted'; count = 0
		pass
	elif upVoteRecord and action == 'down':
		print('2')
		msg = 'You downvoted this question'; count = -1
		Questions.objects.filter(questionId=questionId).update(totalVotes=voteCount - 1)
		UserDetail.objects.filter(UserId=question_posted_by).update(Score = question_owner_score + total_score_change)


	elif downVoteRecord and action == 'down':
		print('3')
		msg = 'Already Downvoted'; count = 0
		pass
	elif downVoteRecord and action == 'up':
		print('4')
		msg = 'You upvoted this question'; count = 1
		Questions.objects.filter(questionId=questionId).update(totalVotes=voteCount + 1)
		UserDetail.objects.filter(UserId=question_posted_by).update(Score = question_owner_score +total_score_change)

	if voteRecord and action == 'up':
		QuestionVotes.objects.using('second').filter(questionId=questionId,userId=loggedUser(request)
		).update(voteType=Case(
			When(voteType=1, then=Value(1)),
			When(voteType=-1,then=Value(1)),
		))
		
	elif voteRecord and action == 'down':
		QuestionVotes.objects.using('second').filter(questionId=questionId,userId=loggedUser(request)
		).update(voteType=Case(
			When(voteType=1, then=Value(-1)),
			When(voteType=-1,then=Value(-1)),
		))
		
	else:
		QuestionVotes(questionId=questionId,userId=loggedUser(request),voteType=voteType).save(using='second')
		Questions.objects.filter(questionId=questionId).update(totalVotes = voteCount + voteType)
		msg = 'You ' + action + 'voted this question'; count = voteType
		UserDetail.objects.filter(UserId=question_posted_by).update(Score = question_owner_score +total_score_change)
	outcome = {'Response':msg,'count':count,'action':action}

	return JsonResponse(outcome)

@csrf_exempt
def answervote(request):
	questionid = request.POST.get('questionId')
	answerid = request.POST.get('answerId')
	action = request.POST.get('action')	
	
	score_of_person_voting = UserDetail.objects.get(UserId=loggedUser(request)).Score
	
	questionObj = Questions.objects.get(questionId=questionid)	

	allAnswers = questionObj.answers
	for ans in allAnswers:
		if str(ans['answerId']) == answerid:	
			voteCount =  ans['totalVotes']
			answer_posted_by = ans['User']
			answer_owner_score = UserDetail.objects.get(UserId=answer_posted_by).Score
			break
	
	if answer_posted_by == loggedUser(request):
		return JsonResponse({'Response':"You can't vote your own Answer",'flag':False})
	elif score_of_person_voting < 10:
		return JsonResponse({'Response':"You don't have enough score!",'flag':False})

	if action == 'up':
		voteType = 1
		total_score_change = 10
	elif action == 'down':
		voteType = -1
		total_score_change = -10
	else:
		pass

	voteRecord = AnswerVotes.objects.using('second').filter(answerId=answerid,userId=loggedUser(request))
	
	upVoteRecord = voteRecord.using('second').filter(voteType=1)
	
	downVoteRecord = voteRecord.using('second').filter(voteType=-1)
	
	
	if upVoteRecord and action == 'up':
		print('1')
		msg = 'Already Upvoted'; count = 0
		pass
	
	elif upVoteRecord and action == 'down':
		print('2')
		msg = 'You downvoted this answer'; count = -1
		ans['totalVotes'] -= 1				
		questionObj.save()
		UserDetail.objects.filter(UserId=answer_posted_by).update(Score = answer_owner_score + total_score_change)
	
	elif downVoteRecord and action == 'down':
		print('3')
		msg = 'Already Downvoted'; count = 0
		pass
	
	elif downVoteRecord and action == 'up':
		print('4')
		msg = 'You upvoted this answer'; count = 1
		ans['totalVotes'] += 1
		
		questionObj.save()
		UserDetail.objects.filter(UserId=answer_posted_by).update(Score = answer_owner_score + total_score_change)

	if voteRecord and action == 'up':
		AnswerVotes.objects.using('second').filter(answerId=answerid,userId=loggedUser(request)
		).update(voteType=Case(
			When(voteType=1, then=Value(1)),
			When(voteType=-1,then=Value(1)),
		))
		
	elif voteRecord and action == 'down':
		AnswerVotes.objects.using('second').filter(answerId=answerid,userId=loggedUser(request)
		).update(voteType=Case(
			When(voteType=1, then=Value(-1)),
			When(voteType=-1,then=Value(-1)),
		))
		
	else:
		AnswerVotes(answerId=answerid,userId=loggedUser(request),voteType=voteType).save(using='second')
		
		ans['totalVotes'] += voteType
		
		questionObj.save()
		msg = 'You ' + action + 'voted this question'; count = voteType
		UserDetail.objects.filter(UserId=answer_posted_by).update(Score = answer_owner_score +total_score_change)
	return JsonResponse({'Response':msg,'count':count,'action':action})