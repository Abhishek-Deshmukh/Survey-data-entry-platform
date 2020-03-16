from django.db import models
from django.contrib.auth.models import User

# Options
class Gender(models.Model):
    description = models.CharField(max_length=12)


class RelationToHead(models.Model):
    relation = models.CharField(max_length=50)
    code = models.IntegerField()


class MaritalStatus(models.Model):
    status = models.CharField(max_length=50)
    code = models.IntegerField()

class Village(models.Model):
    name = models.CharField(max_length=50)


# Options End


class SurveyInstance(models.Model):
    id = models.AutoField(primary_key=True)
    loggist = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)


class HouseholdMember(models.Model):
    survey_instance = models.ForeignKey(SurveyInstance, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    relation_to_head = models.ManyToManyField(RelationToHead)
    gender = models.ManyToManyField(Gender)
    age = models.IntegerField()
    marital_status = models.ManyToManyField(MaritalStatus)
    level_of_education = models.CharField(max_length=50)
    occupation = models.CharField(max_length=50, blank=True)
    monthly_income = models.IntegerField(blank=True)
    secondary_occupation = models.CharField(max_length=30, blank=True)
    secondary_monthly_income = models.IntegerField(blank=True)


QTYPE_CHOICES = (("T", "Text Input"), ("S", "Select One Choice"))


class Question(models.Model):
    question_number = models.IntegerField()
    question_type = models.CharField(max_length=2, choices=QTYPE_CHOICES)
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text + '-' + self.question.question_text

class DataPoint(models.Model):
    loggist = models.ForeignKey(User, on_delete=models.CASCADE)
    survey_instance = models.ForeignKey(SurveyInstance, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=500)
    time_entered = models.DateTimeField(auto_now=True)
