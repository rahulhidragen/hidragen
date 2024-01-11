from django.db import models

# Create your models here.

# models.py
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.username
    

class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    jwt = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username
    

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Products(models.Model):
    name = models.CharField(max_length=100)
    category_id = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    created_by = models.CharField(max_length=50)
    image = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.name