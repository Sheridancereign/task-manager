from django import forms
from django.utils import timezone

from .models import Task


class TaskForm(forms.ModelForm):
    PRIORITY_CHOICES = [
        (1, "Low Priority"),
        (2, "Medium Priority"),
        (3, "High Priority"),
    ]

    priority = forms.TypedChoiceField(
        choices=PRIORITY_CHOICES,
        coerce=int,
        initial=2,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Task
        fields = ["name", "priority", "deadline"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Start typing here to create a task...",
                    "maxlength": 200,
                    "required": True,
                }
            ),
            "deadline": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Task name cannot be empty.")
        return name

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline and deadline < timezone.localdate():
            raise forms.ValidationError("Deadline cannot be in the past.")
        return deadline
