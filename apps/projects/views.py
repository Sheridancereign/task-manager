from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ProjectForm
from .models import Project


class OwnerQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class ProjectListView(OwnerQuerysetMixin, ListView):
    model = Project
    context_object_name = "projects"
    template_name = "projects/project_list.html"


class ProjectDetailView(OwnerQuerysetMixin, DetailView):
    model = Project
    context_object_name = "project"
    template_name = "projects/project_detail.html"


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(OwnerQuerysetMixin, UpdateView):
    model = Project
    fields = ["name"]
    template_name = "projects/project_form.html"


class ProjectDeleteView(OwnerQuerysetMixin, DeleteView):
    model = Project
    template_name = "projects/project_confirm_delete.html"
    success_url = reverse_lazy("projects:list")
