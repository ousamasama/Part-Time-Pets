from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date

# Create your models here.
class Breed(models.Model):
    '''
    A way of specifying what breed the dog is
    '''
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)

class Dog(models.Model):
    '''
    A dog posted by a user
    '''
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=200, blank=False)
    is_available = models.BooleanField(default=True)
    image = models.FileField(upload_to='images/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)

class DogRental(models.Model):
    '''
    A relationship between a user and a dog listed
    '''
    renter = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog,on_delete=models.CASCADE)

class Review(models.Model):
    '''
    A relationship between a user and a dog listed
    '''
    description = models.CharField(max_length=200, blank=False, default='')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog,on_delete=models.CASCADE)
    date = models.DateField(default=None, blank=False, null=True)

    class Meta:
        ordering = ('date',)