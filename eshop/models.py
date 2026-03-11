from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255, verbose_name="Adresse Email")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


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
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    def sub_total(self):
        return self.product.price * self.quantity
    

class AiSettings(models.Model):
    aiModel = models.CharField(default="gemma3:27b",max_length=100)
    temperature = models.FloatField(default=0.7, max_length=10)
    num_predict = models.IntegerField(default=500, max_length=1000)

    def sub_total(self):
        return f"{self.aiModel} {self.temperature} {self.num_predict}"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField(default=0) # On garde FloatField car ton Product.price est en Float
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Commande {self.id} - {self.user.email}"

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