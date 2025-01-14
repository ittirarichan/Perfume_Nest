from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus
from django.db.models.fields import CharField

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


class Enquire(models.Model):
    name=models.TextField()
    email=models.EmailField()
    subject=models.TextField()
    Phone=models.IntegerField()
    message=models.TextField()


class Order(models.Model):
    name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"