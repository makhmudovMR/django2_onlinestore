from django.urls import path, include
from .views import *
from .apps import ShopConfig

app_name = ShopConfig.name


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('detail/<str:slug>/', DetailProduct.as_view(), name='detail_product'),
    path('category/<str:slug>/', CategoryPage.as_view(), name='category'),
    path('cart/', CartPage.as_view(), name='cart'),
    path('addtocart/', CartHandlerAddToCart.as_view(), name='add_to_cart'),
    path('removefromcart/<int:id>/', CartHandlerRemoveFromCart.as_view(), name='remove_from_cart'),
]