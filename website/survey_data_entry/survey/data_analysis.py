from .models import *

# sees all the DataPoint objects and updates the Choice.votes accordingly
def migrate_data_into_choices():
    for question in Question.objects.all():
        if question.question_type == 'S':
            data_points = DataPoint.objects.filter(question = question).order_by('answer')
            choices = Choice.objects.filter(question = question)
            for choice in choices:
                choice.vote = 0
                for data_point in data_points:
                    if data_point.answer == choice.choice_text: choice.votes += 1
                choice.save()

def update_plots():
    migrate_data_into_choices()
    # for question in Question.objects.all():
