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
        # print('jgfdt')
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
        data=Product.objects.all()
        return render(req,'shop/home.html',{'products':data})
    else:
        return redirect(perfume_login)
    


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
    

