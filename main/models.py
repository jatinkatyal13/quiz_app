from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
	question = models.TextField()
	def __str__ (self):
		return self.question

class Choice(models.Model):
	question = models.ForeignKey(Question)
	choice = models.CharField(max_length = 100)
	is_correct = models.BooleanField()
	def __str__ (self):
		return self.choice

class QuestionResult(models.Model):
	user = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	selected_choice = models.ForeignKey(Choice)

	def getRes(self):
		return self.selected_choice.is_correct