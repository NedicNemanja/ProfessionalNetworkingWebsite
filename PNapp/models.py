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
	phone = models.CharField(max_length=17)
	#Maybe requires the Pillow library https://pillow.readthedocs.io/en/latest/
	#Additional info The default form widget for this field is a ClearableFileInput.
	profile_photo = models.ImageField()
	company = models.CharField(128)
	position = models.CharField(256)

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

class Applicants(models.Model):
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
