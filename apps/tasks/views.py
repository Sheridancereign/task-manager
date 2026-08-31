import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from apps.projects.models import Project

from .forms import TaskForm
from .models import Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=kwargs["project_pk"], owner=request.user)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.project = self.project
        self.object = form.save()

        if self.request.htmx:
            return TemplateResponse(self.request, "tasks/_task_row.html", {"task": self.object})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.htmx:
            return HttpResponse(form.errors.as_json(), status=400)
        return super().form_invalid(form)

    def get_success_url(self):
        return self.project.get_absolute_url()


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"

    def get_queryset(self):
        return super().get_queryset().filter(project__owner=self.request.user)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.htmx:
            return TemplateResponse(
                request,
                "tasks/_task_form_inline.html",
                {"task": self.object, "form": self.get_form()},
            )
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        if self.request.htmx:
            return TemplateResponse(self.request, "tasks/_task_row.html", {"task": self.object})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.htmx:
            return TemplateResponse(
                self.request,
                "tasks/_task_form_inline.html",
                {"task": self.object, "form": form},
                status=400,
            )
        return super().form_invalid(form)

    def get_success_url(self):
        return self.object.project.get_absolute_url()


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"

    def get_queryset(self):
        return super().get_queryset().filter(project__owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        if request.htmx:
            return HttpResponse("")

        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.project.get_absolute_url()


class TaskToggleDoneView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, project__owner=request.user)
        task.is_done = not task.is_done
        task.save(update_fields=["is_done"])
        return TemplateResponse(request, "tasks/_task_row.html", {"task": task})


class TaskReorderView(LoginRequiredMixin, View):
    def post(self, request, project_pk):
        project = get_object_or_404(Project, pk=project_pk, owner=request.user)
        data = json.loads(request.body)
        task_ids = data.get("task_ids", [])

        tasks = {t.id: t for t in project.tasks.filter(id__in=task_ids)}
        for index, task_id in enumerate(task_ids):
            task = tasks.get(int(task_id))
            if task:
                task.priority = index
                task.save(update_fields=["priority"])

        return HttpResponse(status=204)
