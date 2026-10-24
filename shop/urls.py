
from django.urls import path, include
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('login/',views.user_login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('signout/',views.user_logout, name='signout'),
    path('shop/',views.shop,name='shop'),
    path('cart/',views.cart,name='cart'),
    path('addtocart/<int:id>', views.add_to_cart, name='addtocart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/delete/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('initiate-payment/', views.initiate_payment),
    path('payment-success/', views.payment_success),
] +static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)
