from django.db import models
from django.utils import timezone

class User(models.Model):
	"""docstring for User"""
	"""def __init__(self, arg):
					super(User, self).__init__()
					self.arg = arg"""
	email = models.EmailField(primary_key=True)
	password = models.CharField(max_length=128)
	name = models.CharField(max_length=64)
	surname = models.CharField(max_length=64)
	phone = models.CharField(max_length=17, blank=True)
	#Maybe requires the Pillow library https://pillow.readthedocs.io/en/latest/
	#Additional info The default form widget for this field is a ClearableFileInput.
	#Maybe requires upload_to arg to be set
	#Maybe also add blank=True?
	profile_photo = models.ImageField()
	university = models.CharField(max_length=128, blank=True)
	degree_subject = models.CharField(max_length=128, blank=True)
	company = models.CharField(max_length=128, blank=True)
	position = models.CharField(max_length=256, blank=True)

	def __str__(self):
		return self.email

class Connection(models.Model):
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	receiver = models.ForeignKey(User, on_delete=models.CASCADE)
	accepted = models.BooleanField(default=False)

	def __str__(self):
		return self.connection_creator#Here maybe return also receiver?

class Advertisment(models.Model):
	creator = models.ForeignKey(User, on_delete=CASCADE)
	description = models.TextField()

	def __str__(self):
		return self.creator#Again maybe also the descript?

class Applicant(models.Model):
	user = models.ForeignKey(User, on_delete=CASCADE)
	advertisment = models.ForeignKey(Advertisment, on_delete=CASCADE)
	ACCEPTED = 'ACCEPTED'
	PENDING = 'PENDING'
	REJECTED = 'REJECTED'
	ADVERTISMENT_STATUS_CHOICES = (
		(ACCEPTED, 'Accepted'),
		(PENDING, 'Pending'),
		(REJECTED, 'Rejected'))
	status = models.CharField(
        choices=ADVERTISMENT_STATUS_CHOICES,
        default=PENDING
    )

    def __str__(self):
    	return self.user#Again ..

class Message(models.Model):
	sender = models.ForeignKey(User)
	receiver = models.ForeignKey(User)
	text = models.CharField()
	creation_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.text

class Post(models.Model):
	creator = models.ForeignKey(User, on_delete=CASCADE)
	creation_date = models.DateTimeField(auto_now=True)
	text = models.CharField()

class Comment(models.Model):
	creator = models.ForeignKey(User, on_delete=CASCADE)
	post_id = models.ForeignKey(Post, on_delete=CASCADE)
	text = models.CharField()
	creation_date = models.DateTimeField(auto_now=True)

class Interest(models.Model):
	creator = models.ForeignKey(User, on_delete=CASCADE)
	post_id = models.ForeignKey(Post, on_delete=CASCADE)
	creation_date = models.DateTimeField(auto_now=True)
