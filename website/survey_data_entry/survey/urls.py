from django.urls import path
from . import views

urlpatterns = [
    path("test/", views.test, name="test"),
    path("", views.home, name="home"),
    path("survey/", views.survey, name="survey"),
    path("member_add/<int:key>", views.household_member_create, name="household_member_create"),
]
