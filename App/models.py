from djongo import models
import uuid

class UserDetail(models.Model):
	class params:
		db = 'default'
	UserId = models.CharField(max_length=50,default='',blank=True)
	FirstName = models.CharField(max_length=50,default='',blank=True)
	LastName = models.CharField(max_length=50,default='',blank=True)
	Password = models.CharField(max_length=100,default='',blank=True)
	Email = models.EmailField(blank=True)
	SecurityQuestion = models.CharField(max_length=150,default='',blank=True)
	SecurityAnswer = models.CharField(max_length=500,default='',blank=True)
	profilePic = models.ImageField(upload_to='media', default='media/user.png')
    
	MALE = 'M'
	FEMALE = 'F'
	OTHER = 'O'
	GENDER_CHOICES = [
	    (MALE, 'Male'),
	    (FEMALE, 'Female'),
	    (OTHER, 'Other')
	    ]
	Gender = models.CharField(max_length=1,default='',choices=GENDER_CHOICES)

	# def __str__(self):
	# 	return f'{self.FirstName} {self.LastName}'

class Votes(models.Model):
	class params:
		db = 'second'
	questionId = models.CharField(max_length=100)
	userId = models.CharField(max_length=50)
	voteType = models.IntegerField(blank=True)		# -1 for down 1 for up
	

class Questions(models.Model):
	class params:
		db = 'default'
	userId = models.CharField(max_length=50)
	questionId = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)
	question = models.TextField()
	totalVotes = models.IntegerField(default=0,blank=True)
	date = models.DateTimeField(auto_now_add=True, blank=True)
	User = models.ForeignKey(UserDetail,on_delete=models.CASCADE,related_name='user')
	

	def __str__(self):
		return self.userId


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    class Meta:
        abstract = True

class Entry(models.Model):
    _id = models.ObjectIdField()
    blog = models.EmbeddedField(
        model_container=Blog
    )
    
    headline = models.CharField(max_length=255)    
    objects = models.DjongoManager()


# 	Book.objects.aggregate(
# ...     price_diff=Max('price', output_field=FloatField()) - Avg('price'))