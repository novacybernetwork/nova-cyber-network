from django.contrib import admin
from django.urls import include, path

from teams import views as team_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("challenges/", include("challenges.urls")),
    path("teams/", include("teams.urls")),
    path("leaderboard/", team_views.leaderboard, name="leaderboard"),
    path("leaderboard/rows/", team_views.leaderboard_rows, name="leaderboard_rows"),
    path("", include("core.urls")),
]
