from django.shortcuts import render, reverse, redirect
from django.views.generic import View
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth import login, authenticate, logout
from .forms import *
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

class CheckOutPage(View):
    def get(self, request):
        cart = get_cart(request)
        total_price = 0
        for item in cart.items.all():
            total_price += item.item_total
        context = {
            'cart': cart,
            'total_price': total_price,
        }
        return render(request, 'shop/checkout.html', context=context)

class OrderPage(View):

    def post(self, request):
        cart = get_cart(request)
        form = OrderForm(request.POST)
        if form.is_valid():
            # some wrong
            new_order = Order()
            new_order.user = request.user
            new_order.save()
            new_order.items.add(cart)
            new_order.first_name = form.cleaned_data['name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.email = form.cleaned_data['email']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.date = form.cleaned_data['date']
            new_order.comment = form.cleaned_data['comment']
            new_order.total = cart.cart_total
            new_order.save()

            del request.session['cart_id']
            del request.session['total']

            return redirect(reverse('shop:thankyou'))


    def get(self, request):
        form = OrderForm()
        return render(request, 'shop/order.html', context={'form': form})

class ThankYou(View):
    def get(self, request):
        return render(request, 'shop/thankyou.html')


class UserPanel(LoginRequiredMixin, View):
    raise_exception = True
    def get(self, request):
        order = Order.objects.filter(user=request.user)
        cart = get_cart(request)
        context = {
            'cart': cart,
            'order': order,

        }
        return render(request, 'shop/userpanel.html', context=context)

class RegisterView(View):
    def post(self, request):
        form = RegsiterForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = form.save(commit=False)
            user.email = email
            user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            login(request,user)
        return redirect(reverse('shop:home'))
        

    def get(self, request):
        form = RegsiterForm()
        return render(request, 'shop/register.html', context={'form': form})


class LoginView(View):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse('shop:home'))
        return redirect(reverse('shop:home'))



    def get(self, request):
        form = LoginForm()
        return render(request, 'shop/login.html', context={'form': form})



# handler

class LogoutHandler(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('shop:home'))

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
        
        new_cart_total = 0
        cart = get_cart(request)
        for cart_item_ in cart.items.all():
            new_cart_total += float(cart_item_.item_total)
        cart.cart_total = new_cart_total
        cart.save()
        return JsonResponse({
            'qty': cart_item.qty, 
            'cart_id': cart_item.id, 
            'item_total': cart_item.item_total,
            'new_cart_total': cart.cart_total
        })