from django.shortcuts import render, reverse
from django.views.generic import View
from django.http import HttpResponseRedirect, JsonResponse
from .models import *


def get_cart(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart.id)
    return cart 

# Create your views here.
class Home(View):

    def get(self, request):
        # take cart from sesison if it exist
        # if cart not exist
        # create cart and cart id write into session
        cart = get_cart(request)
        
        category = Category.objects.all()
        product = Product.objects.all()
        context = {
            'category': category,
            'product': product,
            'cart': cart, 
        }
        return render(request, 'shop/home.html', context=context)


class DetailProduct(View):

    def get(self, request, slug):
        category = Category.objects.all()
        product_item = Product.objects.get(slug__iexact=slug)

        cart = get_cart(request)

        context = {
            'category': category,
            'product_item': product_item,
            'cart': cart,
        }
        return render(request, 'shop/detail_product.html', context=context)

class CategoryPage(View):

    def get(self, request, slug):
        cart = get_cart(request)
        category_item = Category.objects.get(slug__iexact=slug)
        product = category_item.product_set.all()
        category = Category.objects.all()
        context = {
            'category': category,
            'product': product,
            'cart': cart,
        }
        return render(request, 'shop/home.html', context)


class CartPage(View):
    def get(self, request):
        cart = get_cart(request)

        context = {
            'cart': cart
        }
        return render(request, 'shop/cart.html', context=context)

# handler
class CartHandlerAddToCart(View):

    def get(self, request):
        slug = request.GET.get('product_slug')
        cart = get_cart(request)
        
        product = Product.objects.get(slug__iexact=slug)
        new_cart_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
        
        if new_cart_item not in cart.items.all():
            cart.items.add(new_cart_item)
            cart.save()
            return JsonResponse({'cart_total': cart.items.count()})
        return HttpResponseRedirect(reverse('shop:cart'))

class CartHandlerRemoveFromCart(View):
    def get(self, request):
        id = request.GET.get('id')
        cart = get_cart(request)
        cart_item = CartItem.objects.get(id=id)
        if cart_item in cart.items.all():
            cart.items.remove(cart_item)
            cart.save()
        return JsonResponse({'cart_total': cart.items.count()})


class CartHandlerChangeQty(View):

    def get(self, request):
        value_qty = request.GET.get('value')
        id = request.GET.get('id')
        cart_item = CartItem.objects.get(id=id)
        cart_item.qty = value_qty
        cart_item.item_total = int(cart_item.qty) * int(cart_item.product.price)
        cart_item.save()
        return JsonResponse({
            'qty': cart_item.qty, 
            'cart_id': cart_item.id, 
            'item_total': cart_item.item_total,
        })