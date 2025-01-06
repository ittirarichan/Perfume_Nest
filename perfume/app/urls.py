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
    path('add_category',views.add_category),
    path('add_brand',views.add_brand),
    path('manage_products',views.manage_products),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),
    path('delete_brand/<int:id>/', views.delete_brand, name='delete_brand'),
    path('contact', views.contact),
    path('about', views.about),
    path('view_product/<pid>',views.view_product),
    # path('shop/<pid>',views.shop_page),
    path('shop', views.shop_page, name='shop_page'),
    path('shop_category_wise/<cat_id>', views.shop_category_wise, name='shop_category_wise'),
    path('men_pro',views.men_pro, name='men_pro'),
    path('women_pro',views.women_pro, name='women_pro'),
    path('unisex_pro',views.unisex_pro, name='unisex_pro'),
    path('user_profile',views.user_profile),


    path('add_to_cart/<pid>',views.add_to_cart),
    path('view_cart',views.view_cart),
    path("qty_inc/<cid>",views.qty_inc),
    path("qty_dec/<cid>",views.qty_dec),
    path("remove_cart/<cid>",views.remove_cart),
    # path('cart_pro_buy/<cid>',views.cart_pro_buy),
    path('booking',views.bookings),
    # path('pro_buy/<pid>',views.pro_buy),
    path('order/<pid>',views.order),
    # path('pay/<pid>', views.payment_methods, name='pay'),
    # path('buy_details/<int:cat_id>/', views.buy_details),

    # path('search', views.search, name='search'),
    # path('search_product', views.search_product, name='search_product'),
    # path('search_category', views.search_category, name='search_category'),
    # path('search_brand', views.search_brand, name='search_brand'),
    # path('search_price', views.search_price, name='search_price'),




]