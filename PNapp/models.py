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
	email_public = models.BooleanField(default=False)
	password = models.CharField(max_length=128)
	name = models.CharField(max_length=64)
	# Dont think thats needed
	#name_public = models.BooleanField(default=True)
	surname = models.CharField(max_length=64)
	#that neither
	#surname_public = models.BooleanField(default=True)
	#Maybe requires the Pillow library https://pillow.readthedocs.io/en/latest/
	#Additional info The default form widget for this field is a ClearableFileInput.
	#Maybe requires upload_to arg to be set
	#Maybe also add blank=True?
	phone = models.CharField(max_length=17, blank=True)
	phone_public = models.BooleanField(default=False)
	profile_photo = models.ImageField(default='/profpics/user.png', upload_to='profpics/%Y/%m/%d/')
	university = models.CharField(max_length=128, blank=True)
	university_public = models.BooleanField(default=False)
	degree_subject = models.CharField(max_length=128, blank=True)
	degree_subject_public = models.BooleanField(default=False)
	company = models.CharField(max_length=128, blank=True)
	company_public = models.BooleanField(default=False)
	position = models.CharField(max_length=256, blank=True)
	position_public = models.BooleanField(default=False)

	def __str__(self):
		return self.email

	def autheniticate(self,password):
		return (self.password == password)

	def get_posts(self):
		group_of_interest = [self.email]
		users_friends = User.get_users_friends(self)
		for f in users_friends:
			group_of_interest.append(f.email)
		posts = Post.objects.filter(creator__email__in= group_of_interest)
		ordered_posts = posts.order_by('-creation_date')
		return ordered_posts

	def get_users_posts(self):
		return Post.objects.filter(creator=self)

	def get_users_friends(self):
		accepted_connections = Connection.objects.filter(accepted=True)
		users_connections = accepted_connections.filter(creator=self) | accepted_connections.filter(receiver=self)
		users_friends = []
		for c in users_connections:
			if c.creator == self:
				users_friends.append(c.receiver)
			else:
				users_friends.append(c.creator)
		return users_friends

	def get_friends(self):
		friends=set()
		connections=Connection.objects.filter(creator=self,accepted=True)
		for conn in connections:  #conns with user as creator
			friends.add(conn.receiver)
		connections=Connection.objects.filter(receiver=self,accepted=True)
		for conn in connections:  #conns with user as receiver
			friends.add(conn.creator)
		return friends

	def get_conversations(self):
		return Conversation.objects.filter(creator=self).order_by('-creation_date')\
			 | Conversation.objects.filter(receiver=self).order_by('-creation_date')

	def get_notifications(self):
		posts = self.get_posts()
		actions = []
		for post in posts:
			for interest in post.get_interests():
				actions.append(interest)
			for comment in post.get_comments():
				actions.append(comment)
		actions.sort(reverse=True,key=SortNotificationsFunc)
		return actions

class Connection(models.Model):
	#on deletion of a creator or a receiver the said field will be set to null
	creator = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name="CActive")
	#https://stackoverflow.com/questions/26955319/django-reverse-accessor-clashes
	receiver = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name="CPassive")
	accepted = models.BooleanField(default=False)

	def __str__(self):
		return str(self.creator)+"+"+str(self.receiver)+"="+str(self.accepted)

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

class Conversation(models.Model):
	#this could be SET_DEFAULT as well
	creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="MActive")
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="MPassive")
	creation_date = models.DateTimeField(editable=False, default=timezone.now)

	def __str__(self):
		return str(self.creator)+str(self.receiver)

	def get_messages(self):
		return Message.objects.filter(conversation=self).order_by('creation_date')

class Message(models.Model):
	text = models.CharField(max_length=512)
	creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
	creation_date = models.DateTimeField(editable=False, default=timezone.now)
	conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)

	def __str__(self):
		return self.text

class Post(models.Model):
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	#maybe add editable = False in production level
	creation_date = models.DateTimeField()
	text = models.CharField(max_length=512)
	#interests = models.ManyToManyField(User, blank=True, related_name='interests')

	def __str__(self):
		return self.text

	def get_comments(self):
		comments = Comment.objects.filter(post_id=self.id)
		return comments

	def get_interests(self):
		return Interest.objects.filter(post=self)

	def get_comments(self):
		return Comment.objects.filter(post_id=self)

	def total_interests(self):
		return Interest.objects.filter(post=self).count()

class Interest(models.Model):
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	creation_date = models.DateTimeField()

	def __str__(self):
		return str(self.creation_date)
		#return str(self.creator)+"      "+self.post.__str__()

	def get_classname(self):
		return "Interest"

class Comment(models.Model):
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
	text = models.CharField(max_length=512)
	creation_date = models.DateTimeField()

	def __str__(self):
		return self.text

	def get_classname(self):
		return "Comment"

def SortNotificationsFunc(element):
	return element.creation_date
