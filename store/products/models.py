from django.db import models

from users.models import User

class ProductCategory(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_image', blank=True, null=True)
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.name

class BasketQuerySet(models.QuerySet):

    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)




class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    create_timestamp = models.DateTimeField(auto_now_add=True)

    objects=BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username} | с продуктами {self.product.name}'

    def sum(self):
        return self.quantity*self.product.price




