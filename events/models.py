from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="events_created"
    )

    def __str__(self):
        return self.name
