import django_filters
from .models import *
from django.forms.widgets import TextInput, Select


class QuestionnairesFilter(django_filters.FilterSet):
    text = django_filters.CharFilter(field_name='text', lookup_expr='icontains', widget=TextInput(attrs={
        'class': 'col-4 ', 'placeholder': 'Nazwa ankiety', 'style': 'height:40px;',
    }))
    choices = ((None, 'Wszystkie'), (True, 'Aktywne'), (False, 'Nieaktywne'))
    active = django_filters.ChoiceFilter(choices=choices, widget=Select(attrs={
        'class': 'form-select',
    }))

    class Meta:
        model = Questionnaire
        fields = '__all__'
