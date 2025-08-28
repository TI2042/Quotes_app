from django.urls import path

from . import views

urlpatterns = [
    path("", views.quote_view, name="home"),
    path("add/", views.add_quote, name="add_quote"),
    path("vote/<int:quote_id>/<str:action>/", views.vote, name="vote"),
    path("top/", views.top_quotes, name="top_quotes"),
    path("quotes/", views.all_quotes_view, name="all_quotes"),
    path("quotes/<int:pk>/edit/", views.edit_quote_view, name="edit_quote"),
    path("quotes/<int:pk>/delete/", views.delete_quote_view, name="delete_quote"),
]
