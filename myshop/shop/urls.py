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
    path('removefromcart/', CartHandlerRemoveFromCart.as_view(), name='remove_from_cart'),
    path('changecartitemqty/', CartHandlerChangeQty.as_view(), name='change_qty'),
    path('checkout/', CheckOutPage.as_view(), name='checkout'),
    path('order/', OrderPage.as_view(), name='order'),
    path('thankyou/', ThankYou.as_view(), name='thankyou'),
    path('userpanel/', UserPanel.as_view(), name='userpanel'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutHandler.as_view(), name='logout'),
]