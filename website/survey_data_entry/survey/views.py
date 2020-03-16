from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SurveyInstance, HouseholdMember, Question, Choice, DataPoint
from users.models import Loggist
from .forms import *
from .data_analysis import *

# Just to check if the server is running without touching anything from the database
def test(request):
    return render(request, "basic_form.html")


def home(request):
    # migrate_data_into_choices()
    # update_plots()
    context = {
        "loggists": Loggist.objects.all(),
        "questions": Question.objects.all(),
        "choices": Choice.objects.all(),
        "data_points": DataPoint.objects.all(),
    }
    return render(request, "home.html", context)

def household_member_create(request, key):
    if request.method == "POST":
        form = HouseholdMemberCreateForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("survey")
    else:
        member = HouseholdMember(survey_instance = SurveyInstance.objects.get(id=key))
        context = {
                'form' : HouseholdMemberCreateForm(instance=member)
                }
    return render(request, 'household_member_create.html', context)

@login_required(login_url="/user/login")
def survey(request):
    if request.method == "POST":
        old_form = DataPointFormText(request.POST)
        if old_form.is_valid():
            last_data_point = old_form.save()
            # go home after last question is submitted
            if last_data_point.question.id == Question.objects.count():
                loggist = Loggist.objects.get(user=request.user)
                loggist.number_of_surveys_completed += 1
                loggist.has_uncompleted_survey = False
                loggist.save()
                update_plots()
                return redirect("home")
            local_question = Question.objects.get(id=last_data_point.question.id + 1)
            local_survey_instance = last_data_point.survey_instance
        else:
            if "selected_option" in request.POST:
                selected_option = request.POST["selected_option"]
                if selected_option == "":
                    question = Question.objects.get(id=request.POST["question"])
                    if question.id == Question.objects.count():
                        loggist = Loggist.objects.get(user=request.user)
                        loggist.number_of_surveys_completed += 1
                        loggist.has_uncompleted_survey = False
                        loggist.save()
                        update_plots()
                        return redirect("home")
                    else:
                        local_question = Question.objects.get(id=question.id + 1)
                        local_survey_instance = SurveyInstance.objects.get(
                            id=request.POST["survey_instance"]
                        )
                else:
                    last_data_point = DataPoint.objects.create(
                        loggist=request.user,
                        survey_instance=SurveyInstance.objects.get(
                            id=request.POST["survey_instance"]
                        ),
                        question=Question.objects.get(id=request.POST["question"]),
                        answer=selected_option,
                    )
                    last_data_point.save()
                # go home after last question is submitted
                if last_data_point.question.id == Question.objects.count():
                    loggist = Loggist.objects.get(user=request.user)
                    loggist.number_of_surveys_completed += 1
                    loggist.has_uncompleted_survey = False
                    loggist.save()
                    update_plots()
                    return redirect("home")
                else:
                    local_question = Question.objects.get(
                        id=last_data_point.question.id + 1
                    )
                    local_survey_instance = last_data_point.survey_instance
            else:
                question = Question.objects.get(id=request.POST["question"])
                local_question = Question.objects.get(id=question.id + 1)
                local_survey_instance = SurveyInstance.objects.get(
                    id=request.POST["survey_instance"]
                )

    else:
        loggist = Loggist.objects.get(user=request.user)

        if loggist.has_uncompleted_survey == True:
            loggists_last_data_point = DataPoint.objects.filter(
                loggist=request.user
            ).order_by("-time_entered")[:1][0]
            if loggists_last_data_point.question.id == Question.objects.count():
                local_question = Question.objects.get(id=1)
                local_survey_instance = SurveyInstance.objects.create(loggist = request.user)
            else:
                local_question = Question.objects.get(
                    id=loggists_last_data_point.question.id + 1
                )
            local_survey_instance = loggists_last_data_point.survey_instance
        else:
            local_question = Question.objects.get(id=1)
            local_survey_instance = SurveyInstance.objects.create(loggist = request.user)
            loggist.has_uncompleted_survey = True
            loggist.save()

    partial_data_point = DataPoint(
        question=local_question,
        loggist=request.user,
        survey_instance=local_survey_instance,
    )
    form = DataPointFormText(instance=partial_data_point)

    if local_question.question_type == "S":
        context = {
            "survey_instance": local_survey_instance,
            "question": local_question,
            "form": form,
            "choices": Choice.objects.filter(question=local_question),
        }
    else:
        context = {
            "survey_instance": local_survey_instance,
            "question": local_question,
            "form": form,
        }

    return render(request, "survey.html", context)
