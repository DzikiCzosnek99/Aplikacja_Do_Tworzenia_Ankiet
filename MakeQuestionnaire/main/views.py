from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import login, authenticate
from .decorators import *
from .utils import get_plot


# Create your views here.
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
            questionnaire = Questionnaire(text=text, owner=request.user)
            questionnaire.save()
            return redirect(f"/questionnaireCreate/{questionnaire.id}")
    context = {'form': QuestionnaireForm}
    return render(request, 'createNewQuestionnaire.html', context)


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
                else:
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
    questionnaires = Questionnaire.objects.all()
    context = {'questionnaires': questionnaires}
    return render(request, 'questionnaires-DataBase.html', context)


#@qProfileAccess
def questionnaireProfile(request, id):
    questionnaire = Questionnaire.objects.get(id=id)
    if request.method == 'POST':
        questions = questionnaire.questions.all()
        user = request.user
        for p in request.POST:
            if p != 'csrfmiddlewaretoken':
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
        return redirect('/home')
    context = {'questionnaire': questionnaire}
    return render(request, 'questionnaireProfile.html', context)


def deleteQuestion(request, question_id, questionnaire_id):
    question = Question.objects.get(id=question_id)
    for answer in question.answers.all():
        answer.delete()
    question.delete()
    return redirect(f"/questionnaireCreate/{questionnaire_id}")


def deleteAnswer(request, answer_id, questionnaire_id):
    answer = Answer.objects.get(id=answer_id)
    answer.delete()
    return redirect(f"/questionnaireCreate/{questionnaire_id}")


def editQuestion(request, question_id, questionnaire_id):
    question = Question.objects.get(id=question_id)
    form = QuestionForm(instance=question)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect(f"/questionnaireCreate/{questionnaire_id}")
    context = {'form': form}
    return render(request, 'editQuestion.html', context)


def editAnswer(request, answer_id, questionnaire_id):
    answer = Answer.objects.get(id=answer_id)
    form = AnswerForm(instance=answer)
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            return redirect(f"/questionnaireCreate/{questionnaire_id}")
    context = {'form': form}
    return render(request, 'editQuestion.html', context)


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
            return redirect('/home')
    context = {'message': message}
    return render(request, 'login.html', context)


@loged
def register(request):
    form = UserCreationForm()
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(username=username).exists():
            message = 'Podana nazwa użytkownika jest zajęta.'
        elif len(username) < 5:
            message = 'Nazwa użytkownika musi składać się z przynajmniej 6 znaków. '
        elif password1 != password2:
            message = 'Nie poprawnie przepisano hasło.'
        elif len(password1) < 8:
            message = ' Hasło musi zawierać przynajmniej 8 znaków.'
        else:
            user = User(username=username, password=password1)
            user.save()
            return redirect('/login')
    context = {'form': form, 'message': message}
    return render(request, 'register.html', context)


def questionnaireResults(request, id):
    questionnaire = Questionnaire.objects.get(id=id)
    plots = []
    for question in questionnaire.questions.all():
        answers = []
        votes = []
        for answer in question.answers.all():
            answers.append(answer.text)
            votes.append(answer.votes)
        plot = get_plot(answers, votes)
        plots.append(plot)
    questions = questionnaire.questions.all()
    context = {'plots': plots, 'questions': questions, 'questionnaire': questionnaire}
    return render(request, 'questionnaireResults.html', context)

