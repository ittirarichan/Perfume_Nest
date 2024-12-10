from django.urls import path
from . import views

urlpatterns=[
    path('',views.perfume_login),
    path('register',views.register),
    path('user_home',views.user_home),
    path('logout',views.perfume_shop_logout),

    path('perfume_home',views.perfume_home),
    path('add_product',views.add_product),
    path('edit_product/<pid>',views.edit_product),
    path('delete_product/<pid>',views.delete_product),
    path('view_users',views.view_users),
    path('manage_products',views.manage_products)

]