from django.db import models

class Blog(models.Model):
    creator = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    details = models.CharField(max_length=255)
    blog = models.TextField()
    tags = models.CharField(max_length=255)
    responses = models.TextField()
