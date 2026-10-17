from django.urls import path

from . import views

app_name = "teams"

urlpatterns = [
    path("", views.team_list, name="team_list"),
    path("create/", views.team_create, name="team_create"),
    path("join/", views.team_join, name="team_join"),
    path("leave/", views.team_leave, name="team_leave"),
    path("manage/", views.team_manage, name="team_manage"),
    path("<slug:slug>/", views.team_detail, name="team_detail"),
]
