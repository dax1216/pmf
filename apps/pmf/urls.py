from django.urls import path

from . import views

app_name = "pmf"
urlpatterns = [
    path("", views.SearchView.as_view(), name="search"),
    path("list", views.PmfListView.as_view(), name="list"),
]
