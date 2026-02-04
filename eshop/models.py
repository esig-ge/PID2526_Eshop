from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    availability = models.BooleanField()

    #Def Publish obligatoire pour l'espace admin django !!!!!!
    def publish(self):
        self.save()

    #Def de creation de produit via un form non native
    def create_product(self, name, description, price, availability):
        self.name = name
        self.description = description
        self.price = price
        self.availability = availability
        self.save()

    def change_availability(self, av):
        self.availability = av
        self.save()


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_mail = models.EmailField()
    # blank=true pour ne pas obliger une entrée
    review = models.TextField(blank=True)
    publish_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"avis {self.pk} pour {self.product}"


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    def sub_total(self):
        return self.product.price * self.quantity