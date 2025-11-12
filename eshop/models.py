from django.conf import settings
from django.db import models
from django.utils import timezone


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

    def __str__(self):
        return self.name

