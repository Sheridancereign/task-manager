import pytest
from django.contrib.auth import get_user_model

from apps.projects.models import Project

User = get_user_model()


@pytest.mark.django_db
class TestProjectModel:
    def test_str_returns_name(self):
        user = User.objects.create_user(username="alice", password="pass12345")
        project = Project.objects.create(owner=user, name="My Project")

        assert str(project) == "My Project"

    def test_get_absolute_url(self):
        user = User.objects.create_user(username="alice", password="pass12345")
        project = Project.objects.create(owner=user, name="My Project")

        assert project.get_absolute_url() == f"/projects/{project.pk}/"

    def test_projects_ordered_by_newest_first(self):
        user = User.objects.create_user(username="alice", password="pass12345")
        first = Project.objects.create(owner=user, name="First")
        second = Project.objects.create(owner=user, name="Second")

        projects = list(Project.objects.all())

        assert projects == [second, first]
