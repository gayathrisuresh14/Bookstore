from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Genre(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre)
    description = models.TextField()
    image_url = models.CharField(max_length=2083, blank=True)
    price = models.FloatField()
    book_available = models.BooleanField()

class Order(models.Model):
    product = models.ForeignKey(Book, max_length=200, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Book)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

class CartItems(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.book.price * self.quantity

    def __str__(self):
        return f'{self.book.price} * {self.quantity}'

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name
