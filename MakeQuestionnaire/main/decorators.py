from django.shortcuts import redirect, render
from .models import *


def qProfileAccess(viewFunc):
    def wrapper_func(response, id, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=id)
        if UserResponse.objects.filter(user=response.user, questionnaire=questionnaire).exists():
            return redirect(f"/questionnaire_Results/{id}")
        elif response.method == 'POST':
            if 'access' in response.POST:
                password = response.POST.get('password')
                if password != questionnaire.password:
                    message = "Hasło niepoprawne!"
                    context = {'message': message, 'id': id}
                    return render(response, 'questionnaireAccess.html', context)
                else:
                    return viewFunc(response, id, *args, **kwargs)
            if 'finish' in response.POST:
                return viewFunc(response, id, *args, **kwargs)
        elif questionnaire.password != '':
            return redirect(f"/questionnaireAccess/{id}")
        else:
            return viewFunc(response, id, *args, **kwargs)
    return wrapper_func


def qEditAccess(viewFunc):
    def wrapper_func(response, id, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=id)
        user = response.user
        if questionnaire.owner != user:
            return redirect('/home')
        elif not questionnaire.active or questionnaire.public:
            return redirect('/profile')
        else:
            return viewFunc(response, id, *args, **kwargs)
    return wrapper_func


def qResultsAccess(viewFunc):
    def wrapper_func(response, id, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=id)
        if (questionnaire.publicResults and
            UserResponse.objects.filter(user=response.user, questionnaire=questionnaire).exists()) \
                or questionnaire.owner == response.user:
            return viewFunc(response, id, *args, **kwargs)
        else:
            return redirect('/questionnaireAccessInfo')
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
