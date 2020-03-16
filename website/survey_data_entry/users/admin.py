from django.contrib import admin
from .models import Loggist

class LoggistAdmin(admin.ModelAdmin):
    list_display = ("roll_no","user","number_of_surveys_completed","has_uncompleted_survey")
admin.site.register(Loggist,LoggistAdmin)
