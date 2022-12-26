from django.db import models

class Settings(models.Model):
    recursionDepth = models.IntegerField(default=10)