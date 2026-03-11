from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    availability = models.BooleanField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

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
    

class AiSettings(models.Model):
    aiModel = models.CharField(max_length=100, default="gemma3:27b")
    temperature = models.FloatField(default=0.7)
    num_predict = models.IntegerField(default=500)

    def sub_total(self):
        return f"{self.aiModel} {self.temperature} {self.num_predict}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField(default=0) # On garde FloatField car ton Product.price est en Float
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Commande {self.id} - {self.user.username}"

    # Cette méthode permet à ton template d'afficher le total via {{ order.get_total_cost }}
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    # Le related_name='items' est OBLIGATOIRE pour faire order.items.all() dans ta vue/HTML
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField() # On stocke le prix au moment de l'achat
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    # Cette méthode permet d'afficher le total par ligne via {{ item.get_cost }}
    def get_cost(self):
        return self.price * self.quantity