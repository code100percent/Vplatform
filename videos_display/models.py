from django.db import models

class Video(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    published_date = models.DateField(auto_now=True)
    category = models.CharField(max_length=25)
    video = models.FileField(upload_to='videos/')


    


