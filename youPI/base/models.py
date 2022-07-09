from xml.parsers.expat import model
from django.db import models
# Create your models here.


#Keys hold the google developer api keys (collection "key")
class Keys(models.Model):
    key = models.CharField(max_length=100)
    status =models.CharField(max_length=10)
    time=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.key


#Holds the data fetched from youtube
class FetchedData(models.Model):
    _id = models.CharField(primary_key=True,max_length=32)
    title = models.CharField(max_length=100)
    description =models.TextField()
    thumbnail=models.CharField(max_length=200)
    publishedAt=models.CharField(max_length=40)
    # The RFC 3339 Format can 8
    def __str__(self):
        return self.key