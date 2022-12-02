from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



