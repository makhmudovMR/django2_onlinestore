from django.shortcuts import render
from django.views.generic import View
from .models import *

# Create your views here.
class Home(View):

    def get(self, request):
        category = Category.objects.all()
        product = Product.objects.all()
        context = {
            'category': category,
            'product': product,
        }
        return render(request, 'shop/home.html', context=context)


class DetailProduct(View):

    def get(self, request, slug):
        category = Category.objects.all()
        product_item = Product.objects.get(slug__iexact=slug)
        context = {
            'category': category,
            'product_item': product_item,
        }
        return render(request, 'shop/detail_product.html', context=context)

# Category