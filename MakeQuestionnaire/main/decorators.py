from django.shortcuts import redirect
from .models import *


def qProfileAccess(viewFunc):
    def wrapper_func(request, id, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=id)
        if UserResponse.objects.filter(user=request.user, questionnaire=questionnaire).exists():
            return redirect('/home')
        else:
            return viewFunc(request, id, *args, **kwargs)

    return wrapper_func


def loged(viewFunc):
    def wrapper_func(response, *args, **kwargs):
        if response.user.is_authenticated:
            return redirect('/home')
        else:
            return viewFunc(response, *args, **kwargs)

    return wrapper_func


def notloged(viewFunc):
    def wrapper_func(response, *args, **kwargs):
        if not response.user.is_authenticated:
            return redirect('/login')
        else:
            return viewFunc(response, *args, **kwargs)

    return wrapper_func
