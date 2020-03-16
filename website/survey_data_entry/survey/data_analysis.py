from .models import *
from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np

# Setting up style
style.use("ggplot")


# sees all the DataPoint objects and updates the Choice.votes accordingly
def migrate_data_into_choices():
    for question in Question.objects.all():
        if question.question_type == "S":
            data_points = DataPoint.objects.filter(question=question).order_by("answer")
            choices = Choice.objects.filter(question=question)
            for choice in choices:
                choice.votes = 0
                for data_point in data_points:
                    if data_point.answer == choice.choice_text:
                        choice.votes += 1
                choice.save()


def update_plots():
    migrate_data_into_choices()

    for question in Question.objects.all():
        if question.question_type == "S":
            choices = Choice.objects.filter(question=question)
            choice_text = []
            votes = []
            for choice in choices:
                choice_text.append(choice.choice_text)
                votes.append(choice.votes)
            y_pos = np.arange(len(choice_text))
            plt.barh(y_pos, votes, align="center", alpha=1)
            plt.yticks(y_pos, choice_text)
            plt.savefig(f"./media/plots/{question.id}_bar.png")
