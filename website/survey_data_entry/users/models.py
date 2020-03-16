from django.db import models
from django.contrib.auth.models import User

class Loggist(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    roll_no = models.IntegerField(default = 1811000)
    number_of_surveys_completed = models.IntegerField(default = 0)
    has_uncompleted_survey = models.BooleanField(default = False)
    def __str__(self):
        return self.roll_no
