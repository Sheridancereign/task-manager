import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.projects.models import Project

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="alice", password="pass12345")


@pytest.fixture
def other_user(db):
    return User.objects.create_user(username="bob", password="pass12345")


@pytest.mark.django_db
class TestProjectListView:
    def test_requires_login(self, client):
        response = client.get(reverse("projects:list"))
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_only_shows_own_projects(self, client, user, other_user):
        own_project = Project.objects.create(owner=user, name="Mine")
        Project.objects.create(owner=other_user, name="Not Mine")

        client.force_login(user)
        response = client.get(reverse("projects:list"))

        assert response.status_code == 200
        projects = list(response.context["projects"])
        assert projects == [own_project]


@pytest.mark.django_db
class TestProjectCreateView:
    def test_creates_project_owned_by_current_user(self, client, user):
        client.force_login(user)
        response = client.post(reverse("projects:create"), {"name": "New Project"})

        assert response.status_code == 302
        project = Project.objects.get(name="New Project")
        assert project.owner == user


@pytest.mark.django_db
class TestProjectDetailView:
    def test_cannot_access_other_users_project(self, client, user, other_user):
        other_project = Project.objects.create(owner=other_user, name="Not Mine")

        client.force_login(user)
        response = client.get(reverse("projects:detail", kwargs={"pk": other_project.pk}))

        assert response.status_code == 404


@pytest.mark.django_db
class TestProjectDeleteView:
    def test_cannot_delete_other_users_project(self, client, user, other_user):
        other_project = Project.objects.create(owner=other_user, name="Not Mine")

        client.force_login(user)
        response = client.post(reverse("projects:delete", kwargs={"pk": other_project.pk}))

        assert response.status_code == 404
        assert Project.objects.filter(pk=other_project.pk).exists()
