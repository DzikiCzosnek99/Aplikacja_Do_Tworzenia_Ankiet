from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ['text', 'password', 'publicResults']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'col-6 col-form-label', 'style': 'margin-top:20px;'}),
            'password': forms.PasswordInput(attrs={'class': 'col-6 col-form-label', 'style': 'margin-top:20px;'}),
            'publicResults': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'multiple_choice']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'col-10 col-form-label',
                'style': 'background-color:#e6b3ff;border-bottom: 1px solid #000;'}),
            'multiple_choice': forms.CheckboxInput(attrs={'class': 'form-check-input'})
            }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'col-10 col-form-label',
                                           'style': 'background-color:#b3ffb3;border-bottom: 1px solid #000;'})
        }


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
