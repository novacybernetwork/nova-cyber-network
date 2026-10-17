from django.urls import path

from . import views

app_name = "challenges"

urlpatterns = [
    path("", views.challenge_list, name="challenge_list"),
    path("<slug:slug>/", views.challenge_detail, name="challenge_detail"),
    path("<slug:slug>/submit/", views.challenge_submit, name="challenge_submit"),
]
