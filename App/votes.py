from .models import *
from django.db.models import Case, Value, When
# from django.db.models import F, Q, Count

def questionVotes(questionId,action,loggedUser):
    questionId = questionId
    action = action
    if action == 'up':
        voteType = 1
    elif action == 'down':
        voteType = -1
    else:
        pass

    voteRecord = QuestionVotes.objects.using('second').filter(questionId=questionId,userId=loggedUser)

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

    elif downVoteRecord and action == 'down':
        print('3')
        msg = 'Already Downvoted'; count = 0
        pass
    elif downVoteRecord and action == 'up':
        print('4')
        msg = 'You upvoted this question'; count = 1
        Questions.objects.filter(questionId=questionId).update(totalVotes=voteCount + 1)

    if voteRecord and action == 'up':
        QuestionVotes.objects.using('second').filter(questionId=questionId,userId=loggedUser
        ).update(voteType=Case(
            When(voteType=1, then=Value(1)),
            When(voteType=-1,then=Value(1)),
        ))
        
    elif voteRecord and action == 'down':
        QuestionVotes.objects.using('second').filter(questionId=questionId,userId=loggedUser
        ).update(voteType=Case(
            When(voteType=1, then=Value(-1)),
            When(voteType=-1,then=Value(-1)),
        ))
        
    else:
        QuestionVotes(questionId=questionId,userId=loggedUser,voteType=voteType).save(using='second')
        Questions.objects.filter(questionId=questionId).update(totalVotes = voteCount + voteType)
        msg = 'You ' + action + 'voted this question'; count = voteType

    outcome = {'Response':msg,'count':count,'action':action}
    return outcome