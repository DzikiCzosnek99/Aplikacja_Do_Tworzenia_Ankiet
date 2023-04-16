from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import login, authenticate, logout
from .decorators import *
from .utils import get_plot
from .filters import *


def index(request):
    return redirect('home/')


def home(request):
    return render(request, 'home.html')


@notloged
def createNewQuestionnaire(request):
    questionnaireForm = QuestionnaireForm()
    if request.method == 'POST':
        questionnaireForm = QuestionnaireForm(request.POST)
        if questionnaireForm.is_valid():
            text = request.POST.get('text')
            publicResults = request.POST.get('publicResults')
            if publicResults == 'on':
                publicResults = True
            if publicResults is None:
                publicResults = False
            password = request.POST.get('password')
            questionnaire = Questionnaire(text=text, owner=request.user, publicResults=publicResults, password=password)
            questionnaire.save()
            return redirect(f"/questionnaireCreate/{questionnaire.id}")
    context = {'form': QuestionnaireForm}
    return render(request, 'createNewQuestionnaire.html', context)


@qEditAccess
def questionnaireCreate(request, id):
    questionnaire = Questionnaire.objects.get(id=id)
    questionForm = QuestionForm()
    answerForm = AnswerForm()
    if request.method == 'POST':
        if 'addQuestion' in request.POST:
            questionForm = QuestionForm(request.POST)
            if questionForm.is_valid():
                text = request.POST.get('text')
                multiple_choice = request.POST.get('multiple_choice')
                if multiple_choice == 'on':
                    multiple_choice = True
                if multiple_choice is None:
                    multiple_choice = False
                question = Question(text=text, multiple_choice=multiple_choice)
                question.save()
                questionnaire.questions.add(question)
                questionnaire.save()
        if 'save' in request.POST:
            questionnaire.public = True
            questionnaire.save()
            return redirect('/home')
    questionForm = QuestionForm()
    answerForm = AnswerForm()
    context = {'questionnaire': questionnaire, 'questionForm': questionForm, 'answerForm': answerForm}
    return render(request, 'questionnaireCreate.html', context)


def addAnswer(request, question_id, questionnaire_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        question = Question.objects.get(id=question_id)
        answer = Answer(text=text)
        answer.save()
        question.answers.add(answer)
        question.save()
    else:
        return redirect('home/')
    return redirect(f"/questionnaireCreate/{questionnaire_id}")


def questionnaire_DataBase(request):
    questionnaires = Questionnaire.objects.filter(public=True, active=True)
    Myfilter = QuestionnairesFilter(request.GET, queryset=questionnaires)
    questionnaires = Myfilter.qs
    context = {'questionnaires': questionnaires, 'Myfilter': Myfilter}
    return render(request, 'questionnaires-DataBase.html', context)


@notloged
@qProfileAccess
def questionnaireProfile(request, id):
    questionnaire = Questionnaire.objects.get(id=id)
    if request.method == 'POST' and 'access' not in request.POST:
        questions = questionnaire.questions.all()
        user = request.user
        questionnairesDone = QuestionnairesDone.objects.get(user=user)
        questionnairesDone.questionnaires.add(questionnaire)
        questionnairesDone.save()
        for p in request.POST:
            if p != 'csrfmiddlewaretoken' and p != 'finish':
                question = questions.get(text=str(p))
                answers = question.answers.all()
                answersList = request.POST.getlist(str(p))
                userResponse = UserResponse(user=user, questionnaire=questionnaire, question=question)
                userResponse.save()
                for text in answersList:
                    answer = answers.get(text=text)
                    userResponse.answers.add(answer)
                    answer.votes += 1
                    answer.save()
                    userResponse.save()
            else:
                pass
        return redirect(f"/questionnaire_Results/{id}")
    context = {'questionnaire': questionnaire}
    return render(request, 'questionnaireProfile.html', context)


def deleteQuestion(request, question_id, questionnaire_id):
    if request.method != 'POST':
        return redirect('/home')
    question = Question.objects.get(id=question_id)
    for answer in question.answers.all():
        answer.delete()
    question.delete()
    return redirect(f"/questionnaireCreate/{questionnaire_id}")


def deleteAnswer(request, answer_id, questionnaire_id):
    if request.method != 'POST':
        return redirect('/home')
    answer = Answer.objects.get(id=answer_id)
    answer.delete()
    return redirect(f"/questionnaireCreate/{questionnaire_id}")


def editQuestion(request, question_id, questionnaire_id):
    if request.method != 'POST':
        return redirect('/profile')
    question = Question.objects.get(id=question_id)
    form = QuestionForm(instance=question)
    if 'edit' not in request.POST:
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect(f"/questionnaireCreate/{questionnaire_id}")
    context = {'form': form}
    return render(request, 'editQuestion.html', context)


def editAnswer(request, answer_id, questionnaire_id):
    if request.method != 'POST':
        return redirect('/profile')
    answer = Answer.objects.get(id=answer_id)
    form = AnswerForm(instance=answer)
    if 'edit' not in request.POST:
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            return redirect(f"/questionnaireCreate/{questionnaire_id}")
    context = {'form': form}
    return render(request, 'editAnswer.html', context)


@notloged
def myQuestionnaires(request):
    questionnaires = Questionnaire.objects.filter(owner=request.user)
    context = {'questionnaires': questionnaires}
    return render(request, 'myQuestionnaires.html', context)


@loged
def loginPage(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            message = 'Dane logowania są niepoprawne'
        else:
            login(request, user)
            return redirect('/profile')
    context = {'message': message}
    return render(request, 'login.html', context)


@loged
def register(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(username=username).exists():
            message = 'Podana nazwa użytkownika jest zajęta.'
        elif len(username) < 5:
            message = 'Nazwa użytkownika musi składać się z przynajmniej 5 znaków. '
        elif password1 != password2:
            message = 'Nie poprawnie przepisano hasło.'
        elif len(password1) < 8:
            message = ' Hasło musi zawierać przynajmniej 8 znaków.'
        else:
            user = User.objects.create_user(username=username, password=password1)
            user.save()
            questionnairesDone = QuestionnairesDone.objects
            questionnairesDone.create(user=user)
            return redirect('/login')
    context = {'message': message}
    return render(request, 'register.html', context)


@qResultsAccess
def questionnaireResults(request, id):
    questionnaire = Questionnaire.objects.get(id=id)
    for question in questionnaire.questions.all():
        votes = []
        answers = []
        i = 1
        for answer in question.answers.all():
            votes.append(answer.votes)
            text = chr(96 + i)
            text = text.upper()
            answers.append(text)
            i = i + 1
        answers.reverse()
        votes.reverse()
        plot = get_plot(answers, votes)
        question.plot = plot
        question.save()
    questions = questionnaire.questions.all()
    context = {'questions': questions, 'questionnaire': questionnaire}
    return render(request, 'questionnaireResults.html', context)


@notloged
def profile(request):
    if request.method == "POST":
        logout(request)
        return redirect('/home')
    return redirect('/profile/myQuestionnaires')


def questionnaireAccess(request, id):
    message = ''
    context = {'message': message, 'id': id}
    return render(request, 'questionnaireAccess.html', context)


def questionnaireAccessInfo(request):
    return render(request, 'questionnaireAccessInfo.html')


def myQuestionnaires(request):
    questionnaires = Questionnaire.objects.filter(owner=request.user, public=True)
    Myfilter = QuestionnairesFilter(request.GET, queryset=questionnaires)
    questionnaires = Myfilter.qs
    context = {'questionnaires': questionnaires, 'Myfilter': Myfilter}
    return render(request, 'myQuestionnaires.html', context)


def disableQuestionnaire(request, id):
    if request.method != 'POST':
        return redirect('/home')
    else:
        questionnaire = Questionnaire.objects.get(id=id)
        if 'active' in request.POST:
            questionnaire.active = True
            questionnaire.save()
        else:
            questionnaire.active = False
            questionnaire.save()
        return redirect('/profile')


def deleteQuestionnaire(request, id):
    if request.method != 'POST':
        return redirect('/home')
    else:
        questionnaire = Questionnaire.objects.get(id=id)
        for question in questionnaire.questions.all():
            for answer in question.answers.all():
                answer.delete()
            question.delete()
        questionnaire.delete()
        return redirect('/profile')


def questionnaireDone(request):
    questionnaires = QuestionnairesDone.objects.get(user=request.user).questionnaires.all()
    Myfilter = QuestionnairesFilter(request.GET, queryset=questionnaires)
    questionnaires = Myfilter.qs
    context = {'questionnaires': questionnaires, 'Myfilter': Myfilter}
    return render(request, 'questionnaireDone.html', context)


def notPublicQuestionnaire(request):
    if request.method == 'POST' and 'public' in request.POST:
        id = request.POST.get('public')
        questionnaire = Questionnaire.objects.get(id=id)
        questionnaire.public = True
        questionnaire.save()
    questionnaires = Questionnaire.objects.filter(owner=request.user, public=False)
    Myfilter = QuestionnairesFilter(request.GET, queryset=questionnaires)
    questionnaires = Myfilter.qs
    context = {'questionnaires': questionnaires, 'Myfilter': Myfilter}
    return render(request, 'notPublicQuestionnaire.html', context)


def editQuestionnaire(request, id):
    questionnaire = Questionnaire.objects.get(id=id)
    form = QuestionnaireForm(instance=questionnaire)
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST, instance=questionnaire)
        if form.is_valid():
            form.save()
            return redirect('/profile/notPublicQuestionnaire')
    context = {'form': form}

    return render(request, 'editQuestionnaire.html', context)


