import pytest
from django.contrib.auth import get_user_model

from apps.projects.models import Project
from apps.tasks.models import Task

User = get_user_model()


@pytest.fixture
def project(db):
    user = User.objects.create_user(username="alice", password="pass12345")
    return Project.objects.create(owner=user, name="Test Project")


@pytest.mark.django_db
class TestTaskModel:
    def test_str_returns_name(self, project):
        task = Task.objects.create(project=project, name="Write tests")
        assert str(task) == "Write tests"

    def test_default_is_done_is_false(self, project):
        task = Task.objects.create(project=project, name="New task")
        assert task.is_done is False

    def test_tasks_ordered_by_priority_then_newest_first(self, project):
        low = Task.objects.create(project=project, name="Low", priority=3)
        high = Task.objects.create(project=project, name="High", priority=1)
        medium = Task.objects.create(project=project, name="Medium", priority=2)

        tasks = list(project.tasks.all())

        assert tasks == [high, medium, low]

    def test_deleting_project_deletes_its_tasks(self, project):
        Task.objects.create(project=project, name="Task")
        project.delete()

        assert Task.objects.count() == 0
