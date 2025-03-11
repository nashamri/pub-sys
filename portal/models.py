from django.db import models
from django.contrib.auth.models import User


# class MyModel(models.Model):
#     upload = models.FileField()
class UploadedFile(models.Model):
    upload = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
