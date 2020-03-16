from django.forms import ModelForm
from django import forms
from .models import HouseholdMember, DataPoint, Choice, Question
from django.contrib.auth.models import User


class DataPointFormText(ModelForm):
    class Meta:
        model = DataPoint
        fields = ["loggist", "survey_instance", "question", "answer"]

class HouseholdMemberCreateForm(ModelForm):
    class Meta:
        model = HouseholdMember
        fields = ["name", "relation_to_head", "gender", "age", "marital_status", "level_of_education", "occupation", "monthly_income", "secondary_occupation", "secondary_monthly_income"]
