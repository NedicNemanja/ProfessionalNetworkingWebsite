from django.db import models
from django.utils import timezone
import datetime

class User(models.Model):
	"""docstring for User"""
	"""def __init__(self, arg):
					super(User, self).__init__()
					self.arg = arg"""
	id = models.AutoField(primary_key=True)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=128)
	name = models.CharField(max_length=64)
	surname = models.CharField(max_length=64)
	#Maybe requires the Pillow library https://pillow.readthedocs.io/en/latest/
	#Additional info The default form widget for this field is a ClearableFileInput.
	#Maybe requires upload_to arg to be set
	#Maybe also add blank=True?
	phone = models.CharField(max_length=17, blank=True)
	profile_photo = models.ImageField(default='/profpics/user.png', upload_to='profpics/%Y/%m/%d/')
	university = models.CharField(max_length=128, blank=True)
	degree_subject = models.CharField(max_length=128, blank=True)
	company = models.CharField(max_length=128, blank=True)
	position = models.CharField(max_length=256, blank=True)

	def __str__(self):
		return self.email

	def autheniticate(self,password):
		return (self.password == password)

	def get_posts(self):
		group_of_interest = [self.email]
		posts = Post.objects.filter(creator__email__in= group_of_interest)
		return posts

class Connection(models.Model):
	#on deletion of a creator or a receiver the said field will be set to null
	creator = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name="CActive")
	#https://stackoverflow.com/questions/26955319/django-reverse-accessor-clashes
	receiver = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name="CPassive")
	accepted = models.BooleanField(default=False)

	def __str__(self):
		return str(self.creator)+" "+str(self.receiver)

class Advertisment(models.Model):
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	description = models.TextField()

	def __str__(self):
		return self.description#Again maybe also the descript?

class Applicant(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	advertisment = models.ForeignKey(Advertisment, on_delete=models.CASCADE)
	ACCEPTED = 'ACCEPTED'
	PENDING = 'PENDING'
	REJECTED = 'REJECTED'
	ADVERTISMENT_STATUS_CHOICES = (
		(ACCEPTED, 'Accepted'),
		(PENDING, 'Pending'),
		(REJECTED, 'Rejected'))
	status = models.CharField(
		max_length=512,
        choices=ADVERTISMENT_STATUS_CHOICES,
        default=PENDING
    )

	def __str__(self):
		return self.user

class Message(models.Model):
	#this could be SET_DEFAULT as well
	creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="MActive")
	#https://stackoverflow.com/questions/26955319/django-reverse-accessor-clashes
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="MPassive")
	text = models.CharField(max_length=512)
	creation_date = models.DateTimeField(editable=False)

	def __str__(self):
		return self.text

class Post(models.Model):
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	#maybe add editable = False in production level
	creation_date = models.DateTimeField()
	text = models.CharField(max_length=512)

	def __str__(self):
		return self.text

	def get_comments(self):
		comments = Comment.objects.filter(post_id=self.id)
		return comments

class Comment(models.Model):
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
	text = models.CharField(max_length=512)
	creation_date = models.DateTimeField()
	
	def __str__(self):
		return self.text

class Interest(models.Model):
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
	creation_date = models.DateTimeField(editable=False)
