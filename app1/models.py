from django.db import models
from django.core import validators
# Create your models here.
from django.contrib.auth.models import User

class Profile(models.Model):
    username=models.OneToOneField(User,on_delete=models.CASCADE)
    adress=models.TextField()
    profile_pic=models.ImageField(upload_to='sab')
    subscription = models.TextField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.adress
    
class Search(models.Model):
    movie_name = models.CharField(max_length = 30)
    image = models.ImageField(upload_to='sab')
    discription = models.CharField(max_length = 100)
    category = models.CharField(max_length = 100)
    language = models.CharField(max_length = 10)
    director = models.CharField(max_length = 30)
    movie_runtime = models.IntegerField()
    release_date = models.DateField()

    def __str__(self):
        return self.movie_name
