from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from time import time
from transliterate import translit

# function
def image_folder(instance, filename):
    filename = str(int(time())) + '-' + filename
    return '{0}/{1}'.format(instance.slug, filename)

# устанавливаем слаг перед сохранением в случае если его нет
def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(instance.name + str(int(time())))
        instance.slug = slug

def pre_save_product_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(instance.title + str(int(time())))
        instance.slug = slug

# Create your models here.
class Product(models.Model):
    category = models.ForeignKey('shop.Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to=image_folder)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    availabel = models.BooleanField(default=True) # доступен ли товар?


    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return 'cart item for product {}'.format(self.product.title)


class Cart(models.Model):
    items = models.ManyToManyField('shop.CartItem')
    cart_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return str(self.id)

# link signals

pre_save.connect(pre_save_category_slug, sender=Category)
pre_save.connect(pre_save_product_slug, sender=Product)