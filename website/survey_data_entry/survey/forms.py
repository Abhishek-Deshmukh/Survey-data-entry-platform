from django.forms import ModelForm
from django import forms
from .models import DataPoint, Choice, Question
from django.contrib.auth.models import User

class DataPointFormText(ModelForm):
    class Meta:
        model = DataPoint
        fields = ['loggist','survey_instance','question','answer']
