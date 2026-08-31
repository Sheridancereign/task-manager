import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.projects.models import Project
from apps.tasks.models import Task

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="alice", password="pass12345")


@pytest.fixture
def other_user(db):
    return User.objects.create_user(username="bob", password="pass12345")


@pytest.fixture
def project(user):
    return Project.objects.create(owner=user, name="My Project")


@pytest.mark.django_db
class TestTaskCreateView:
    def test_creates_task_in_project(self, client, user, project):
        client.force_login(user)
        url = reverse("tasks:create", kwargs={"project_pk": project.pk})
        response = client.post(url, {"name": "New task", "priority": 2, "deadline": ""})

        assert response.status_code == 302
        assert Task.objects.filter(project=project, name="New task").exists()

    def test_cannot_create_task_in_other_users_project(self, client, user, other_user):
        other_project = Project.objects.create(owner=other_user, name="Not Mine")
        client.force_login(user)
        url = reverse("tasks:create", kwargs={"project_pk": other_project.pk})
        response = client.post(url, {"name": "Sneaky task", "priority": 2, "deadline": ""})

        assert response.status_code == 404
        assert not Task.objects.filter(project=other_project).exists()


@pytest.mark.django_db
class TestTaskToggleDoneView:
    def test_toggles_is_done(self, client, user, project):
        task = Task.objects.create(project=project, name="Task", is_done=False)
        client.force_login(user)
        url = reverse("tasks:toggle", kwargs={"pk": task.pk})

        client.post(url)
        task.refresh_from_db()
        assert task.is_done is True

        client.post(url)
        task.refresh_from_db()
        assert task.is_done is False

    def test_cannot_toggle_other_users_task(self, client, user, other_user):
        other_project = Project.objects.create(owner=other_user, name="Not Mine")
        task = Task.objects.create(project=other_project, name="Task")

        client.force_login(user)
        url = reverse("tasks:toggle", kwargs={"pk": task.pk})
        response = client.post(url)

        assert response.status_code == 404
        task.refresh_from_db()
        assert task.is_done is False


@pytest.mark.django_db
class TestTaskDeleteView:
    def test_deletes_own_task(self, client, user, project):
        task = Task.objects.create(project=project, name="Task")
        client.force_login(user)
        url = reverse("tasks:delete", kwargs={"pk": task.pk})

        response = client.post(url)

        assert response.status_code == 302
        assert not Task.objects.filter(pk=task.pk).exists()

    def test_cannot_delete_other_users_task(self, client, user, other_user):
        other_project = Project.objects.create(owner=other_user, name="Not Mine")
        task = Task.objects.create(project=other_project, name="Task")

        client.force_login(user)
        url = reverse("tasks:delete", kwargs={"pk": task.pk})
        response = client.post(url)

        assert response.status_code == 404
        assert Task.objects.filter(pk=task.pk).exists()
