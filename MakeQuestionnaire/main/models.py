from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Answer(models.Model):
    text = models.CharField(max_length=80)
    votes = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.text


class Question(models.Model):
    text = models.CharField(max_length=80)
    answers = models.ManyToManyField(Answer, blank=True)
    multiple_choice = models.BooleanField(default=False)
    plot = models.CharField(max_length=1500, blank=True, null=True)

    def __str__(self):
        return self.text


class Questionnaire(models.Model):
    text = models.CharField(max_length=50)
    questions = models.ManyToManyField(Question, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    public = models.BooleanField(null=True, default=False)
    publicResults = models.BooleanField(null=True, blank=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(auto_now_add=True, null=True)
    active = models.BooleanField(null=True, default=True)

    def __str__(self):
        return self.text


class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    answers = models.ManyToManyField(Answer, blank=True)


class QuestionnairesDone(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    questionnaires = models.ManyToManyField(Questionnaire, blank=True)
