from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User


# Create your views here.



#--------------------shop login------------------------


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

#--------------------shop logout------------------------


def perfume_shop_logout(req):
    logout(req)
    req.session.flush()                   #session delete
    return redirect(perfume_login)














# --------------admin functions starting from here-------------


#--------------------admin homepage------------------------


def perfume_home(req):
    if 'shop' in req.session:              #checking section status
        if req.method=='POST':
            file=req.FILES['img']
            data=Carousel.objects.create(img=file)
            data.save()
            data=Carousel.objects.all()[::-1][:3]
            delete_data=Carousel.objects.all()[::-1][3:]
            
            for i in delete_data:
                file=i.img.url
                file=file.split('/')[-1]
                os.remove('media/' + file)
                i.delete()
            return redirect(perfume_home)
        else:
            data=Carousel.objects.all()[::-1][:3]
            return render(req,'shop/admin_home.html',{'carousel':data})
    else:
        return redirect(perfume_login)
    









# --------------Add category and display-------------


def add_category(req):
    if 'shop' in req.session:
        if req.method == 'POST':
            cat_name = req.POST['cat_name']
            Category.objects.create(cat_name=cat_name.upper())
            categories = Category.objects.all()
            return render(req, 'shop/add_category.html', {'categories': categories})
        else:
            categories = Category.objects.all()
            return render(req, 'shop/add_category.html', {'categories': categories})
    else:
        return redirect(perfume_login)










# ------------------to delete category----------------


def delete_category(req, id):
    if 'shop' in req.session:
        try:
            category = Category.objects.get(id=id)
            category.delete()
        except Category.DoesNotExist:
            pass  # You can add an error message here if needed
        return redirect(add_category)
    else:
        return redirect(perfume_login)









# ------------------to add brand ----------------


def add_brand(req):
    if 'shop' in req.session:
        if req.method == 'POST':
            bnd_name = req.POST['bnd_name']
            Brand.objects.create(bnd_name=bnd_name.upper())
            brands = Brand.objects.all()
            return render(req, 'shop/add_brand.html', {'brands': brands})
        else:
            
            brands = Brand.objects.all()
            return render(req, 'shop/add_brand.html', {'brands': brands})
    else:
        return redirect(perfume_login)










# -----------------to delete a brand -----------------


def delete_brand(req, id):
    if 'shop' in req.session:
        try:
            brand = Brand.objects.get(id=id)
            brand.delete()
        except Brand.DoesNotExist:
            pass  
        return redirect(add_brand)
    else:
        return redirect(perfume_login)
    









# --------------Add product-------------


def add_product(req):
    if 'shop' in req.session:
        if req.method == 'POST':
            product_id = req.POST['pid']
            name = req.POST['name']
            description = req.POST['description']
            gender = req.POST['gender']
            price = req.POST['price']
            offer_price = req.POST['offer_price']
            stock = req.POST['stock']
            file = req.FILES['image']
            pro_cat_id = req.POST['pro_cat']  # Get selected category ID (no need to create)
            pro_bnd_id = req.POST['pro_bnd']  # Get selected brand ID (no need to create)

            # Fetch the related Category and Brand objects
            pro_cat = Category.objects.get(id=pro_cat_id)
            pro_bnd = Brand.objects.get(id=pro_bnd_id)


            product = Product.objects.create(pid=product_id,name=name,dis=description,gender=gender.upper(),
                                price=price,offer_price=offer_price,stock=stock,img=file,pro_cat=pro_cat,pro_bnd=pro_bnd)

            product.save()  # Save the product object
            return redirect(manage_products)
        else:
            # Fetch categories and brands to populate dropdowns
            categories = Category.objects.all()
            brands = Brand.objects.all()
            return render(req, 'shop/add_product.html', {'categories': categories, 'brands': brands})
    else:
        return redirect(perfume_login)









# --------------Edit product-------------


def edit_product(req,pid):
    if req.method=='POST':
        product_id=req.POST['pid']
        name=req.POST['name']
        description=req.POST['description']
        gender=req.POST['gender']
        price=req.POST['price']
        offer_price=req.POST['offer_price']
        stock=req.POST['stock']
        file=req.FILES['image']
        pro_cat_id = req.POST['pro_cat']  # Get selected category ID (no need to create )
        pro_bnd_id= req.POST['pro_bnd']  # Get selected brand ID (no need to create )

        # Fetch the related Category and Brand objects
        pro_cat = Category.objects.get(id=pro_cat_id)
        pro_bnd = Brand.objects.get(id=pro_bnd_id)
        

        if file :
            Product.objects.filter(pid=product_id,name=name,dis=description,gender=gender.upper(),
                                price=price,offer_price=offer_price,stock=stock,img=file,pro_cat=pro_cat,pro_bnd=pro_bnd)
            data=Product.objects.get(pk=pid)
            data.img=file
            data.save()

        else:
            Product.objects.filter(pk=pid).update(pid=product_id,name=name,dis=description,gender=gender.upper(),
                                price=price,offer_price=offer_price,stock=stock,img=file,pro_cat=pro_cat,pro_bnd=pro_bnd)
            return redirect(perfume_home)
    else:
        data=Product.objects.get(pk=pid)
        categories = Category.objects.all()
        brands = Brand.objects.all()
        return render(req,'shop/edit_product.html',{'data':data ,'categories': categories, 'brands': brands})
    









# --------------delete product-------------


def delete_product(pid):
    data=Product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/' + file)
    data.delete()
    return redirect(perfume_home)










# --------------view users-------------

def view_users(req):
    users = User.objects.all()
    users_data = []
    for user in users:
        users_data.append({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined,    
            'last_login': user.last_login,
        })

    return users_data
    # return render(req,'shop/manage_users.html',{'users':data})










# --------------view all users-------------


def user_list_view(req):
    users_data = view_users()
    return render(req, 'manage_users.html', {'users_data': users_data})










# --------------Manage products-------------------

def manage_products(req):
    data=Product.objects.all()
    return render(req,'shop/manage_products.html',{'products':data})


# ---------------------------------------------------Admin functions ends here------------------------------------------------------------














# ---------------------------------------------------user functions starting from here------------------------------------------------------------

#--------------------user reg------------------------


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








#--------------------User home------------------------


def user_home(req):
    if 'user' in req.session:
        data1=Carousel.objects.all()[::-1][:3]          #display latest added 8 Carousel
        categories = Category.objects.all()             #display latest added 8 prodects
        data2=Product.objects.all()[::-1][:4]           #display latest added 8 prodects
        return render (req,'user/user_home.html',{'carousel':data1,'product':data2,'categories':categories})
    else:
        return redirect(perfume_login)
    








#--------------------shop page in user (for display all products)------------------------


def shop_page(req):
        # If no category is selected, show all products
    products = Product.objects.all()
    categories = Category.objects.all()
    # Render the shop page with products and categories
    return render(req, 'user/shop.html', {'products': products,'categories': categories})








#--------------------shop Category wise (display products in category wise)------------------------


def shop_category_wise(req,cat_id):
    cat=Category.objects.get(pk=cat_id)
    products = Product.objects.filter(pro_cat=cat)
    categories=Category.objects.all()
    return render(req, 'user/shop_category_wise.html', {'products': products, 'categories': categories})










#--------------------men Products (display all mens products in this page)------------------------


def men_pro(req):
    product=Product.objects.filter(gender="MALE")
    categories = Category.objects.all()
    return render(req, 'user/men.html', {'product': product,'categories': categories})










#--------------------user profile (in user page)------------------------


def user_profile(req):
    if 'user' in req.session:
        return render (req,'user/user_profile.html')
    else:
        return redirect(perfume_login)


#--------------------View products (display all the details of the product in this page)------------------------


def view_product(req,pid):
    data=Product.objects.get(pk=pid)
    return render(req,'user/view_product.html',{'product':data})






def add_to_cart(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    try:
        cart=Cart.objects.get(user=user,product=product)
        cart.qty+=1
        cart.save()
    except:
        data=Cart.objects.create(product=product,user=user,qty=1)
        data.save()
    return redirect(view_cart)

def view_cart(req):
    user=User.objects.get(username=req.session['user'])
    data=Cart.objects.filter(user=user)
    return render(req,'user/cart.html',{'cart':data})  

def qty_inc(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty+=1
    data.save()  
    return redirect(view_cart)

def qty_dec(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty-=1
    data.save()  
    if data.qty==0:
        data.delete()
    return redirect(view_cart)

def remove_cart(req,cid):
    data=Cart.objects.get(pk=cid)

    data.delete()
    return redirect(view_cart)

def cart_pro_buy(req,cid):
    cart=Cart.objects.get(pk=cid)
    product=cart.product
    user=cart.user
    qty=cart.qty
    price=product.offer_price*qty
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(bookings)

def pro_buy(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    qty=1
    price=product.offer_price
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(bookings)

def bookings(req):
    user=User.objects.get(username=req.session['user'])
    buy=Buy.objects.filter(user=user)[::-1]
    return render(req,'user/bookings.html',{'bookings':buy})











# --------------contact page-------------


def contact(req):
    return render(req,'user/contact.html')










# --------------about page-------------

def about(req):
    return render(req,'user/about.html')
