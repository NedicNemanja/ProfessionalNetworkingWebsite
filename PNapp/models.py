from django.db import models
from django.utils import timezone
import datetime


class Skill(models.Model):
	name = models.CharField(max_length=128, primary_key=True, blank=False)

	def __str__(self):
		return str(self.name)

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
	skills = models.ManyToManyField(Skill)
	skills_public = models.BooleanField(default=False)

	def __str__(self):
		return self.email

	def autheniticate(self,password):
		return (self.password == password)

	#get posts users network created
	def get_posts(self):
		group_of_interest = [self.email]
		users_friends = User.get_users_friends(self)
		for f in users_friends:
			group_of_interest.append(f.email)
		posts = Post.objects.filter(creator__email__in= group_of_interest)
		ordered_posts = posts.order_by('-creation_date')
		return ordered_posts

	#get posts user created
	def get_users_posts(self):
		return Post.objects.filter(creator=self)

	#get posts user created,interested,commented on
	def get_interacted_posts(self):
		#posts user created
		interacted_posts = self.get_users_posts()
		#posts user was interested in
		post_ids_interested = Interest.objects.filter(creator=self).values('post')
		for post_dict in post_ids_interested:
			interacted_posts = interacted_posts | Post.objects.filter(id=post_dict['post'])
		#posts user commented on
		post_ids_commented = Comment.objects.filter(creator=self).values('post_id')
		for post_dict in post_ids_commented:
			interacted_posts = interacted_posts | Post.objects.filter(id=post_dict['post_id'])
		return interacted_posts

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
		posts = self.get_users_posts()
		actions = []
		for post in posts:
			for interest in post.get_interests():
				actions.append(interest)
			for comment in post.get_comments():
				actions.append(comment)
		actions.sort(reverse=True,key=SortNotificationsFunc)
		return actions

	#num of total interests and comments of this user
	def shill_score(self):
		return Interest.objects.filter(creator=self).count()+Comment.objects.filter(creator=self).count()

	#get ads created by this user
	def get_user_ads(self):
		return Advertisment.objects.filter(creator=self)

	#get available ads for this user
	def get_ads(self):
		ads = []
		for friend in self.get_friends():
			ads += friend.get_user_ads()
			print(friend.get_user_ads())
		ads += self.get_user_ads()
		return ads

	#get the skills of a user
	def get_skills(self):
		return self.skills.all()

	#get the ads on which user has applied
	def get_applications(self):
		return self.advertisment_set.all()

class Connection(models.Model):
	#on deletion of a creator or a receiver the said field will be set to null
	creator = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name="CActive")
	#https://stackoverflow.com/questions/26955319/django-reverse-accessor-clashes
	receiver = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name="CPassive")
	accepted = models.BooleanField(default=False)

	def __str__(self):
		return str(self.creator)+"+"+str(self.receiver)+"="+str(self.accepted)

class Advertisment(models.Model):
	creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ad_creator")
	title = models.TextField()
	details = models.TextField()
	skills = models.ManyToManyField(Skill)
	creation_date = models.DateTimeField(editable=False, default=timezone.now)
	applicants = models.ManyToManyField(User)

	def __str__(self):
		return self.title

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
		return str(self.creator)+" is interested in"+self.post.__str__()

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
