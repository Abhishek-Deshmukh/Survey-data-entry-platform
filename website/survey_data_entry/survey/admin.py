from django.contrib import admin
from .models import *


class SurveyInstanceAdmin(admin.ModelAdmin):
    list_display = ("id",)


admin.site.register(SurveyInstance, SurveyInstanceAdmin)


class HouseholdMemberAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "gender",
        "age",
        "marital_status",
        "occupation",
        "secondary_occupation",
    )
    list_per_page = 20
    search_fields = ("name", "occupation", "secondary_occupation")


admin.site.register(HouseholdMember)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text",)


admin.site.register(Question, QuestionAdmin)


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("question", "choice_text", "votes")


admin.site.register(Choice, ChoiceAdmin)


class DataPointAdmin(admin.ModelAdmin):
    list_display = ("loggist", "survey_instance", "question", "answer", "time_entered")
    search_fields = ("loggist", "answer", "question", "survey_instance")


admin.site.register(DataPoint, DataPointAdmin)


## uncomment the following to edit those things

class VillageAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Village,VillageAdmin)

class GenderAdmin(admin.ModelAdmin):
    list_display = ('description',)
admin.site.register(Gender,GenderAdmin)

class RelationToHeadAdmin(admin.ModelAdmin):
    list_display = ('relation','code',)
admin.site.register(RelationToHead,RelationToHeadAdmin)

class MaritalStatusAdmin(admin.ModelAdmin):
    list_display = ('status','code',)
admin.site.register(MaritalStatus,MaritalStatusAdmin)
