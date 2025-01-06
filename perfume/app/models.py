from django.db import models
from django.contrib.auth.models import User

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



class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    qty=models.IntegerField()



class Buy(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    qty=models.IntegerField()
    price=models.IntegerField()
    date=models.DateField(auto_now_add=True)
    payment=models.CharField(max_length=45)



class User_details(models.Model) :
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.TextField()
    phone=models.IntegerField()
    pincode=models.IntegerField()
    state=models.TextField()
    country=models.TextField()  


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # shop = models.ForeignKey(Shopreg, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.TextField()
    rating = models.IntegerField(default=5)  # 1 to 5 rating
    submitted_at = models.DateTimeField(auto_now_add=True)