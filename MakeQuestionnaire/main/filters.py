import django_filters
from .models import *
from django.forms.widgets import TextInput


class QuestionnairesFilter(django_filters.FilterSet):
    text = django_filters.CharFilter(field_name='text', lookup_expr='icontains', widget=TextInput(attrs={
        'class': 'col-4',
    }))

    class Meta:
        model = Questionnaire
        fields = ''
