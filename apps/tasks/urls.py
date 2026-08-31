from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path(
        "project/<int:project_pk>/create/",
        views.TaskCreateView.as_view(),
        name="create",
    ),
    path("<int:pk>/edit/", views.TaskUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.TaskDeleteView.as_view(), name="delete"),
    path("<int:pk>/toggle/", views.TaskToggleDoneView.as_view(), name="toggle"),
]