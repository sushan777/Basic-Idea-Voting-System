from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class Idea(models.Model):
	title = models.CharField(max_length=50)
	image = models.ImageField(upload_to="images/")
	description = models.TextField()
	created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

class Comment(models.Model):
	comment = models.TextField()
	created = models.DateTimeField(default=timezone.now)
	# updated = models.DateTimeField(default=timezone.now,on_update=timezone.now)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	idea = models.ForeignKey(Idea, on_delete=models.CASCADE)

	def __str__(self):
		return self.comment

class Vote(models.Model):
	VOTE_CHOICES = (
		('U',"Upvote"),
		('D',"Downvote")
		)
	vote = models.CharField(
		max_length = 1,
		choices = VOTE_CHOICES
		)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	idea = models.ForeignKey(Idea, on_delete=models.CASCADE)

	def __str__(self):
		return self.vote