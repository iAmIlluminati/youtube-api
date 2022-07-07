from xml.parsers.expat import model
from django.db import models

# Create your models here.
class Keys(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=100)
    status =models.CharField(max_length=10)
    time=models.DateTimeField(auto_now_add=True)