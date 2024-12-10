from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User

# Create your views here.

def perfume_login(req):
    if 'shop' in req.session:
        return redirect(perfume_home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method=='POST':
        username=req.POST['username']
        password=req.POST['password']
        data=authenticate(username=username,password=password)
        if data:
            login(req,data)
            if data.is_superuser:
                req.session['shop']=username
                return redirect(perfume_home)
            else:
                req.session['user']=username
                return redirect(user_home)
        else:
            messages.warning(req, "Invalid username or password.")
            return redirect(perfume_login)
    else:
        return render(req,'login.html')

def perfume_shop_logout(req):
    logout(req)
    req.session.flush()                   #session delete
    return redirect(perfume_login)


#--------------------admin------------------------

def perfume_home(req):
    if 'shop' in req.session:              #checking section status
        if req.method=='POST':
            file=req.FILES['img']
            data=Carousel.objects.create(img=file)
            data.save()
            return redirect(perfume_home)
        else:
            return render(req,'shop/admin_home.html')
    else:
        return redirect(perfume_login)
    

    # data=Product.Carousel.objects.all()[::-1][:3]
    # delete_data=Carousel.objects.all()[::-1][3:]
    # if i in delete_data:
    #     i.delete


#--------------------user------------------------

def register(req):
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        pswd=req.POST['password']
        try:
            data=User.objects.create_user(first_name=name,email=email,username=email,password=pswd)    
            data.save()
        except:
            messages.warning(req, "Username/email already exist.")
            return redirect(register)
        return redirect(perfume_login)
    else:
        return render(req,'user/register.html')
    

def user_home(req):
    if 'user' in req.session:
        data=Product.objects.all()
        data1=Carousel.objects.all()[::-1][:3]
        return render (req,'user/user_home.html',{'products':data,'carousel':data1})
    else:
        return redirect(perfume_login)
    



def add_product(req):
    if 'shop' in req.session:
        if req.method=='POST':
            product_id=req.POST['pid']
            name=req.POST['name']
            description=req.POST['description']
            categories=req.POST['categories']
            price=req.POST['price']
            offer_price=req.POST['offer_price']
            stock=req.POST['stock']
            file=req.FILES['image']
            data=Product.objects.create(pid=product_id,name=name,dis=description,cat=categories,
                                         price=price,offer_price=offer_price,stock=stock,img=file)
            data.save()
            return redirect(manage_products)
        else:
            return render(req,'shop/add_product.html')
    else:
        return redirect(perfume_login)
    


def edit_product(req,pid):
    if req.method=='POST':
        product_id=req.POST['pid']
        name=req.POST['name']
        description=req.POST['description']
        categories=req.POST['categories']
        price=req.POST['price']
        offer_price=req.POST['offer_price']
        stock=req.POST['stock']
        file=req.FILES['image']
        if file :
            Product.objects.filter(pk=product_id).update(pid=product_id,name=name,dis=description,cat=categories,
                                         price=price,offer_price=offer_price,stock=stock,img=file)
            data=Product.objects.get(pk=pid)
            data.img=file
            data.save()

        else:
            Product.objects.filter(pk=pid).update(pid=product_id,name=name,dis=description,cat=categories,
                                         price=price,offer_price=offer_price,stock=stock,img=file)
            return redirect(perfume_home)
    else:
        data=Product.objects.get(pk=pid)
        return render(req,'shop/edit_product.html',{'data':data})
        
    


def delete_product(req,pid):
    data=Product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/' + file)
    data.delete()
    return redirect(perfume_home)



def view_users(req):
    data=User.objects.all()
    return render(req,'shop/manage_users.html',{'users':data})



def manage_products(req):
    data=Product.objects.all()
    return render(req,'shop/manage_products.html',{'products':data})