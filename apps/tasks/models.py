from django.db import models


class Task(models.Model):
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    name = models.CharField(max_length=200)
    priority = models.PositiveIntegerField(
        default=0,
        help_text="Lower number = higher priority (used for manual ordering).",
    )
    deadline = models.DateField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["priority", "-created_at"]

    def __str__(self):
        return self.name
