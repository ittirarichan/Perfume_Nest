from django.db import models

# Create your models here.

class Category(models.Model):
    cat_name=models.CharField(max_length=45)


class Brand(models.Model):
    bnd_name=models.CharField(max_length=45)

class Product(models.Model):
    pid=models.TextField()
    name=models.TextField()
    dis=models.TextField()
    gender=models.CharField(max_length=10)
    price=models.IntegerField()
    offer_price=models.IntegerField()
    stock=models.IntegerField()
    img=models.FileField()
    pro_cat=models.ForeignKey(Category,on_delete=models.CASCADE)
    pro_bnd=models.ForeignKey(Brand,on_delete=models.CASCADE)


class Carousel(models.Model):
    img=models.FileField()


