import os
import django
import random
import requests
from io import BytesIO
from django.core.files import File
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comp_tences_Osmanistos.settings')
django.setup()

from eshop.models import Product

def populate_digitec_style(n=50):
    fake = Faker(['fr_FR'])
    
    # 1. Un catalogue massif et varié
    # J'ai remplacé les images uniques par des listes d'images plus "studio/produit"
    CATALOG = [
        {
            "brands": ["Apple", "Samsung", "Google"],
            "models": ["iPhone 15 Pro", "Galaxy S24 Ultra", "Pixel 8 Pro", "iPhone 14"],
            "desc": "Smartphone haut de gamme. Écran OLED et appareil photo exceptionnel.",
            "price_min": 799, "price_max": 1400,
            "image_urls": [
                "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=640&q=80", # Smartphone neutre
                "https://images.unsplash.com/photo-1616348436168-de43ad0db179?w=640&q=80"  # iPhone
            ]
        },
        {
            "brands": ["Apple"],
            "models": ["MacBook Pro 14\" M3", "MacBook Air M2 13\""],
            "desc": "Laptop puissant pour créatifs. Autonomie exceptionnelle et écran Liquid Retina.",
            "price_min": 1100, "price_max": 3500,
            "image_urls": [
                "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=640&q=80", # MacBook de face
                "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=640&q=80"  # MacBook ouvert neutre
            ]
        },
        {
            "brands": ["Asus", "MSI", "Gigabyte"],
            "models": ["GeForce RTX 4090", "Radeon RX 7900 XTX", "GeForce RTX 4070 Ti"],
            "desc": "Carte graphique ultra performante pour le gaming en 4K et la création 3D.",
            "price_min": 800, "price_max": 2200,
            "image_urls": [
                "https://images.unsplash.com/photo-1591488320449-011701bb6704?w=640&q=80", # GPU
                "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=640&q=80"  # GPU 2
            ]
        },
        {
            "brands": ["Intel", "AMD"],
            "models": ["Core i9-14900K", "Ryzen 9 7950X3D", "Core i5-13600K"],
            "desc": "Processeur de dernière génération. Idéal pour le multitâche et le jeu.",
            "price_min": 250, "price_max": 700,
            "image_urls": [
                "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=640&q=80", # CPU plan serré
                "https://images.unsplash.com/photo-1555680202-c86f0e12f086?w=640&q=80"  # Chipset
            ]
        },
        {
            "brands": ["Corsair", "G.Skill", "Kingston"],
            "models": ["32Go DDR5-6000", "64Go DDR5-6400", "16Go DDR4-3200"],
            "desc": "Kit mémoire RAM haute fréquence avec dissipation thermique intégrée.",
            "price_min": 80, "price_max": 300,
            "image_urls": [
                "https://images.unsplash.com/photo-1562976540-1502f714426d?w=640&q=80" # RAM
            ]
        },
        {
            "brands": ["Samsung", "Crucial", "WD"],
            "models": ["SSD NVMe 2To", "SSD Externe 1To", "SSD SATA 4To"],
            "desc": "Stockage ultra-rapide. Vitesses de lecture jusqu'à 7000 Mo/s.",
            "price_min": 90, "price_max": 400,
            "image_urls": [
                "https://images.unsplash.com/photo-1531492746076-161ca9bcad58?w=640&q=80" # Disque dur
            ]
        },
        {
            "brands": ["Sony", "Nintendo", "Microsoft"],
            "models": ["PlayStation 5 Slim", "Switch OLED", "Xbox Series X"],
            "desc": "Console de jeux vidéo. Plongez dans des mondes immersifs.",
            "price_min": 320, "price_max": 550,
            "image_urls": [
                "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=640&q=80", # PS5
                "https://images.unsplash.com/photo-1605901309584-818e25960b8f?w=640&q=80"  # Manettes / Console
            ]
        },
        {
            "brands": ["Logitech", "Corsair", "Razer"],
            "models": ["Souris Gaming Superlight", "Souris Ergonomique MX Master 3"],
            "desc": "Capteur optique haute précision. Switchs garantis pour 50M de clics.",
            "price_min": 50, "price_max": 160,
            "image_urls": [
                "https://images.unsplash.com/photo-1527814050087-1508248c2017?w=640&q=80", # Souris de bureau
                "https://images.unsplash.com/photo-1615663245857-ac93bb7c3f17?w=640&q=80"  # Souris gaming
            ]
        },
        {
            "brands": ["Keychron", "Logitech", "Razer"],
            "models": ["Clavier Mécanique Sans Fil", "Clavier Gaming TKL"],
            "desc": "Frappe réactive et rétroéclairage RGB personnalisable.",
            "price_min": 80, "price_max": 250,
            "image_urls": [
                "https://images.unsplash.com/photo-1595225476474-87563907a212?w=640&q=80", # Clavier mécanique
                "https://images.unsplash.com/photo-1601445638532-3c6f6c3aa1d6?w=640&q=80"  # Clavier propre
            ]
        },
        {
            "brands": ["Samsung", "Asus", "LG"],
            "models": ["Écran Gaming 27\" 144Hz", "Moniteur Ultrawide 34\"", "Écran OLED 32\""],
            "desc": "Dalle IPS/OLED avec un temps de réponse de 1ms. Couleurs éclatantes.",
            "price_min": 250, "price_max": 1200,
            "image_urls": [
                "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=640&q=80", # Moniteur
                "https://images.unsplash.com/photo-1542393545-10f5cde2c810?w=640&q=80"  # Setup écran
            ]
        },
        {
            "brands": ["Sony", "Bose", "Sennheiser"],
            "models": ["Casque Bluetooth ANC", "Casque Gaming Sans Fil"],
            "desc": "Immersion sonore totale avec annulation de bruit active (ANC).",
            "price_min": 150, "price_max": 400,
            "image_urls": [
                "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=640&q=80", # Casque audio studio
                "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=640&q=80"  # Casque blanc clean
            ]
        },
        {
            "brands": ["Garmin", "Apple", "Samsung"],
            "models": ["Fenix 7 Pro", "Apple Watch Ultra 2", "Galaxy Watch 6"],
            "desc": "Montre connectée multisports avec GPS intégré et suivi santé avancé.",
            "price_min": 250, "price_max": 900,
            "image_urls": [
                "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=640&q=80", # Apple watch neutre
                "https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=640&q=80"  # Smartwatch acier
            ]
        },
        {
            "brands": ["LG", "Samsung", "Sony"],
            "models": ["TV OLED 65\"", "TV Neo QLED 55\"", "TV Bravia 75\""],
            "desc": "Téléviseur 4K UHD avec HDR10+. Des noirs profonds et des contrastes infinis.",
            "price_min": 900, "price_max": 3500,
            "image_urls": [
                "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=640&q=80", # TV murale neutre
                "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=640&q=80"  # TV avec netflix
            ]
        }
    ]

    print(f"Génération de {n} produits type Digitec...")

    for i in range(n):
        category = random.choice(CATALOG)
        
        brand = random.choice(category["brands"])
        model = random.choice(category["models"])
        name = f"{brand} {model}"
        
        description = f"{category['desc']} {fake.text(max_nb_chars=120)}"
        
        base_price = random.randint(category["price_min"], category["price_max"])
        price = float(base_price) + random.choice([0.00, 0.90, 0.95])
        
        availability = random.choices([True, False], weights=[0.85, 0.15])[0]

        print(f"  [{i+1}/{n}] Création de {name}...", end=" ")
        
        try:
            # On choisit une image au hasard dans la liste des images de cette catégorie
            image_url = random.choice(category["image_urls"])
            response = requests.get(image_url, timeout=10)
            
            if response.status_code == 200:
                img_temp = BytesIO(response.content)
                img_filename = f"{brand.lower()}_{model.replace(' ', '_').replace('/', '').lower()}_{random.randint(100,999)}.jpg"
                
                product = Product(
                    name=name,
                    description=description,
                    price=price,
                    availability=availability
                )
                product.image.save(img_filename, File(img_temp), save=True)
                print("OK")
            else:
                raise Exception(f"HTTP {response.status_code}")
        except Exception as e:
            print(f"Erreur image: {e}.")
            Product.objects.create(
                name=name,
                description=description,
                price=price,
                availability=availability
            )

    print("Terminé ! La base de données est prête et variée.")

if __name__ == '__main__':
    print("Nettoyage des anciens produits...")
    Product.objects.all().delete()
    # On génère 40 produits pour bien remplir la grille
    populate_digitec_style(40)