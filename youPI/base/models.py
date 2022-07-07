from xml.parsers.expat import model
from django.db import models
# Create your models here.


#Keys hold the google developer api keys (collection "key")
class Keys(models.Model):
    id = models.CharField(primary_key=True,max_length=32)
    key = models.CharField(max_length=100)
    status =models.CharField(max_length=10)
    time=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.key

class FetchData(models.Model):
    id = models.CharField(primary_key=True,max_length=32)
    key = models.CharField(max_length=100)
    status =models.CharField(max_length=10)
    time=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.key