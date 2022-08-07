from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Video(models.Model):

    done_by = models.ForeignKey(User, on_delete=models.CASCADE)
    transcript = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def get_url(self):
        return reverse("document", args=[self.id])
