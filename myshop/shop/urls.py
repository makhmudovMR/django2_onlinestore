from django.urls import path, include
from .views import *
from .apps import ShopConfig

app_name = ShopConfig.name


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('detail/<str:slug>/', DetailProduct.as_view(), name='detail_product'),
]