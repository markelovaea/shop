from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import ForeignKey, CASCADE, SET_NULL
from django.db.models.fields import TextField, TimeField, DateTimeField, IntegerField


class Shop(models.Model):
    name = TextField(max_length=128, null=False)
    address = TextField(max_length=128, null=False)
    open_time = TimeField(null=False)
    close_time = TimeField(null=False)

class Customer(models.Model):
    fio = TextField(max_length=128, null=False)
    age = IntegerField(null=False, validators=[MinValueValidator(18)])

class Cart(models.Model):
    customer = ForeignKey(Customer, null=False, on_delete=CASCADE)
    shop = ForeignKey(Shop, null=False, on_delete=CASCADE)

class Product(models.Model):
    name = TextField(max_length=128, null=False)
    price = IntegerField(null=False)

class CartItem(models.Model):
    cart = ForeignKey(Cart, null=False, on_delete=CASCADE)
    product = ForeignKey(Product, null=False, on_delete=CASCADE)
    count = IntegerField(validators=[MinValueValidator(1)])




