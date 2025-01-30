from django.db import models

# Create your models here.

class Accessible(models.Model):
    access = models.BooleanField(default=False)

    