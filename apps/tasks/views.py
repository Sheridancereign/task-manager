from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from apps.projects.models import Project

from .models import Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["name", "priority", "deadline"]
    template_name = "tasks/task_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(
            Project, pk=kwargs["project_pk"], owner=request.user
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.project = self.project
        return super().form_valid(form)

    def get_success_url(self):
        return self.project.get_absolute_url()


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["name", "priority", "deadline"]
    template_name = "tasks/task_form.html"

    def get_queryset(self):
        return super().get_queryset().filter(project__owner=self.request.user)

    def get_success_url(self):
        return self.object.project.get_absolute_url()


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"

    def get_queryset(self):
        return super().get_queryset().filter(project__owner=self.request.user)

    def get_success_url(self):
        return self.object.project.get_absolute_url()

class TaskToggleDoneView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, project__owner=request.user)
        task.is_done = not task.is_done
        task.save(update_fields=["is_done"])
        return redirect(task.project.get_absolute_url())

