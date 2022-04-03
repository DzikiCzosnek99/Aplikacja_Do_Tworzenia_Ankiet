from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('createNewQuestionnaire/', views.createNewQuestionnaire, name='createNewQuestionnaire'),
    path('home/', views.home, name='home'),
    path('questionnaireCreate/<str:id>', views.questionnaireCreate, name='questionnaireCreate'),
    path('addAnswer/<str:question_id>/<str:questionnaire_id>', views.addAnswer, name='addAnswer'),
    path('questionnaire_DataBase/', views.questionnaire_DataBase, name='questionnaire_DataBase'),
    path('questionnaireProfile/<str:id>', views.questionnaireProfile, name='questionnaireProfile'),
    path('deleteQuestion/<str:question_id>/<str:questionnaire_id>', views.deleteQuestion, name='deleteQuestion'),
    path('editQuestion/<str:question_id>/<str:questionnaire_id>', views.editQuestion, name='editQuestion'),
    path('deleteAnswer/<str:answer_id>/<str:questionnaire_id>', views.deleteAnswer, name='deleteAnswer'),
    path('editAnswer/<str:answer_id>/<str:questionnaire_id>', views.editAnswer, name='editAnswer'),
    path('myQuestionnaires', views.myQuestionnaires, name='myQuestionnaires'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.register, name='register'),
    path('questionnaire_Results/<str:id>', views.questionnaireResults, name='questionnaireResults'),
    path('profile/', views.profile, name='profile'),
    ]
