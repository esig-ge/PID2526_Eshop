import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comp_tences_Osmanistos.settings')
django.setup()

from eshop.models import Product

def populate_digitec_style(n=30):
    fake = Faker(['fr_FR'])
    
    # Listes pour construire des noms réalistes
    brands = ['Asus', 'Apple', 'Samsung', 'Logitech', 'Corsair', 'Sony', 'Lenovo', 'HP', 'MSI', 'Gigabyte']
    types = [
        ('MacBook Pro', 'Laptop puissant pour créatifs'),
        ('iPhone 15', 'Le dernier smartphone Apple'),
        ('RTX 4090', 'Carte graphique ultra performante'),
        ('Écran Gaming 27"', 'Dalle IPS 144Hz'),
        ('Souris sans fil', 'Capteur optique haute précision'),
        ('Clavier Mécanique', 'Switchs Cherry MX Red'),
        ('Casque Bluetooth', 'Réduction de bruit active'),
        ('SSD NVMe 2To', 'Vitesse de lecture 7000 Mo/s'),
        ('PS5 Slim', 'Console de jeux 4K'),
        ('RAM DDR5 32Go', 'Kit dual channel haute fréquence')
    ]

    print(f"Génération de {n} produits type Digitec...")

    for _ in range(n):
        brand = random.choice(brands)
        p_type, p_desc_short = random.choice(types)
        
        # On construit un nom crédible : [Marque] [Modèle]
        name = f"{brand} {p_type}"
        
        # On utilise Faker pour générer une description plus longue autour du produit
        description = f"{p_desc_short}. {fake.text(max_nb_chars=150)}"
        
        # Prix crédible (finissant souvent par .90 ou .00 chez les marchands)
        price = random.randint(20, 2500) + random.choice([0.00, 0.90, 0.95])
        
        availability = random.choice([True, True, True, False])

        Product.objects.create(
            name=name,
            description=description,
            price=price,
            availability=availability
        )

    print("Terminé ! C'est maintenant une vraie boutique de tech.")

if __name__ == '__main__':
    # Optionnel : On peut vider la table avant pour nettoyer les anciens noms "éclatés"
    # Product.objects.all().delete() 
    populate_digitec_style(30)