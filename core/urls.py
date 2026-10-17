from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("rules/", views.rules, name="rules"),
    path("health/", views.health, name="health"),
    path("manage/", views.admin_overview, name="admin_overview"),
    path("manage/submissions/", views.admin_submission_logs, name="admin_submission_logs"),
    path("manage/export/results.csv", views.admin_export_results, name="admin_export_results"),
    path("manage/export/submissions.csv", views.admin_export_submissions, name="admin_export_submissions"),
]
