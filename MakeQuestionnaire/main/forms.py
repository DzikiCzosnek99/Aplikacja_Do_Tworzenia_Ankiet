from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ['text']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'multiple_choice']

    multiple_choice = forms.BooleanField(widget=forms.CheckboxInput, required=False)


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
