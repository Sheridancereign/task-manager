import datetime

import pytest

from apps.tasks.forms import TaskForm


@pytest.mark.django_db
class TestTaskForm:
    def test_valid_data(self):
        form = TaskForm(data={"name": "Buy milk", "priority": 2, "deadline": ""})
        assert form.is_valid()

    def test_blank_name_is_invalid(self):
        form = TaskForm(data={"name": "   ", "priority": 2, "deadline": ""})
        assert not form.is_valid()
        assert "name" in form.errors

    def test_deadline_in_the_past_is_invalid(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        form = TaskForm(data={"name": "Task", "priority": 2, "deadline": yesterday.isoformat()})
        assert not form.is_valid()
        assert "deadline" in form.errors

    def test_deadline_today_is_valid(self):
        today = datetime.date.today()
        form = TaskForm(data={"name": "Task", "priority": 2, "deadline": today.isoformat()})
        assert form.is_valid()

    def test_invalid_priority_choice_is_rejected(self):
        form = TaskForm(data={"name": "Task", "priority": 99, "deadline": ""})
        assert not form.is_valid()
        assert "priority" in form.errors
