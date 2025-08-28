from django.urls import path
from . import views

urlpatterns = [
    path("", views.quote_view, name="home"),
    path("add/", views.add_quote, name="add_quote"),
    path("vote/<int:quote_id>/<str:action>/", views.vote, name="vote"),
    path("top/", views.top_quotes, name="top_quotes"),
]
