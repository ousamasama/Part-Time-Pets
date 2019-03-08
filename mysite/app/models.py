from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date

# Create your models here.
class Breed(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name

class Dog(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=200, blank=False)
    is_available = models.BooleanField(default=True)
    image = models.FileField(upload_to='images/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)

class DogRental(models.Model):
    renter = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog,on_delete=models.CASCADE)

