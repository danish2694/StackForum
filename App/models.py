from djongo import models
from django import forms
from django.utils import timezone
import pytz
import uuid
from django.urls import reverse
# from djangotoolbox.fields import ListField

class Tags(models.Model):
	# _id = models.ObjectIdField()
	tag = models.CharField(max_length=50,blank=True)
	class Meta:
		abstract = True

class UserDetail(models.Model):
	class params:
		db = 'default'
	UserId = models.CharField(max_length=50,default='',blank=True)
	FirstName = models.CharField(max_length=50,default='',blank=True)
	LastName = models.CharField(max_length=50,default='',blank=True)
	Phone = models.CharField(max_length=10,default='',blank=True)
	Age = models.IntegerField(blank=True)
	Password = models.CharField(max_length=100,default='',blank=True)
	Email = models.EmailField(blank=True)
	SecurityQuestion = models.CharField(max_length=150,default='',blank=True)
	SecurityAnswer = models.CharField(max_length=500,default='',blank=True)
	profilePic = models.ImageField(upload_to='media', default='media/user.png')
	# Categories = models.ListCharField(
	# 	base_field = models.CharField(max_length=50, blank=True),
	# 	max_length = (100*100)
	# )
	# Categories = models.ArrayField(model_container=Tags,model_form_class=None)
	MALE = 'M'
	FEMALE = 'F'
	OTHER = 'O'
	GENDER_CHOICES = [
	    (MALE, 'Male'),
	    (FEMALE, 'Female'),
	    (OTHER, 'Other')
	    ]
	Gender = models.CharField(max_length=1,default='',choices=GENDER_CHOICES)

	def __str__(self):
		return self.UserId
	# 	return f'{self.FirstName} {self.LastName}'

class QuestionVotes(models.Model):
	class params:
		db = 'second'
	questionId = models.CharField(max_length=100,blank=True)
	userId = models.CharField(max_length=50)
	voteType = models.IntegerField(blank=True)		# -1 for down 1 for up

class AnswerVotes(models.Model):
	class params:
		db = 'second'
	answerId = models.CharField(max_length=100,blank=True)
	userId = models.CharField(max_length=50)
	voteType = models.IntegerField(blank=True)		# -1 for down 1 for up

class Answers(models.Model):
	class params:
		db = 'default'
	# questionId = models.CharField(max_length=50)
	# question = models.ForeignKey(Questions,on_delete=models.CASCADE)
	answerId = models.CharField(max_length=100,default='', unique=True)
	answer = models.TextField(blank=True)
	totalVotes = models.IntegerField(blank=True)
	date = models.DateTimeField(default=timezone.now(),blank=True,editable=True)
	User = models.CharField(max_length=50,blank=True,default='')
	# User = models.ForeignKey(UserDetail,on_delete=models.CASCADE)
	class Meta:
		abstract = True

class AnswersForm(forms.ModelForm):
	class Meta:
		model = Answers
		fields = (
            '__all__'
        )

class Questions(models.Model):
	class params:
		db = 'default'
	questionId = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)
	question = models.TextField()
	answers = models.ArrayField(
        model_container=Answers,
		model_form_class=AnswersForm
    )
	totalVotes = models.IntegerField(default=0,blank=True)
	date = models.DateTimeField(auto_now_add=True, blank=True)
	Views = models.IntegerField(default=0)
	User = models.ForeignKey(UserDetail,on_delete=models.CASCADE,related_name='userinfo')
	objects = models.DjongoManager()
	def __str__(self):
		return str(self.questionId
)


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    class Meta:
        abstract = True

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = (
            'name', 'tagline'
        )

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    
    class Meta:
        abstract = True

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = (
            'name', 'email'
        )
        
class Entry(models.Model):
    blog = models.EmbeddedField(
        model_container=Blog,
        model_form_class=BlogForm
    )
    
    headline = models.CharField(max_length=255)    
    authors = models.ArrayField(
        model_container=Author,
        model_form_class=AuthorForm
    )
    
    objects = models.DjongoManager()