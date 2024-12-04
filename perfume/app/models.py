from django.db import models

# Create your models here.

class Product(models.Model):
    pid=models.TextField()
    name=models.TextField()
    dis=models.TextField()
    cat=models.TextField()
    price=models.IntegerField()
    offer_price=models.IntegerField()
    stock=models.IntegerField()
    img=models.FileField()

class Carousel(models.Model):
    img=models.FileField()
