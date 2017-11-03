from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    url(r'^leaderboard/?$', views.leaderboard, name = "leaderboard"),
    url(r'^login/?$', views.login_view, name = "login"),
    url(r'^logout/?$', views.logout_view, name = "login"),
]