from json import JSONDecodeError

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import apikeys
from eshop.models import Product, Review, Cart, CartItem
from .forms import PostReview
from django.shortcuts import render, get_object_or_404
from ollama import Client
# Create your views here.

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


def product_list(request):
    products = Product.objects.all()
    return render(request, "eshop/product_list.html", {'products': products})

def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = Review.objects.filter(product=product)

# Post generé par IA ChatGPT
    if request.method == 'POST':
        form = PostReview(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            return redirect('product_details', pk=product.pk)  # éviter double POST redireciton !!!
    else:
        form = PostReview()

    return render(request, 'eshop/product_details.html', {
        'product': product,
        'reviews': reviews,
        'form': form,   # <-- important !
    })


def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'POST':
        form = PostReview(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('product_details', pk=review.product.pk)
    else:
        form = PostReview(instance=review)

    return render(request, 'eshop/review_edit.html', {'form': form, 'review': review})

def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    product_pk = review.product.pk
    review.delete()
    return redirect('product_details', pk=product_pk)


def product_search(request):
    try:
        query = request.GET.get("q", "")

        if query:
            resultats = Product.objects.filter(name__icontains=query).values('id', 'name', 'price')

        else:
            resultats = Product.objects.none()

    except JSONDecodeError:
        resultats = Product.objects.none()

    results_list = list(resultats)
    return JsonResponse({"results": results_list})

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # On récupère ou on crée le panier de l'utilisateur
    cart, created = Cart.objects.get_or_create(owner=request.user)

    # On cherche si le produit est déjà dans le panier
    cart_item, item_created = CartItem.objects.get_or_create(
        product=product, 
        cart=cart,
        defaults={'quantity': 1} # Si on le crée, on met 1 par défaut
    )

    # Si l'objet existait déjà, on incrémente juste la quantité
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')

@login_required
def cart_remove(request, product_id):
    cart = get_object_or_404(Cart, owner=request.user)
    product = get_object_or_404(Product, id=product_id)
    
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass # Le produit n'était pas dans le panier, on ne fait rien

    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(owner=request.user)

    cart_items = CartItem.objects.filter(cart=cart)

    total = sum(item.sub_total() for item in cart_items)

    return render(request, 'eshop/cart_detail.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total': total  
        
    })


def ai_search(request):
    query = request.GET.get("q", "")

    if len(query) < 2:
        return JsonResponse({"results": []})

    try:
        # ─── Configuration pour Ollama Cloud ───
        api_key = apikeys.api_key_osman  # api key is supposed to be found on your local files, dont push it on the repo

        if not api_key:
            raise ValueError("Aucune clé API Ollama configurée")

        client = Client(
            host="https://ollama.com",
            headers={
                "Authorization": f"Bearer {api_key}"
            }
        )

        # Appel simple et efficace
        response = client.chat(
            model="gemma3:27b",  # ← this one will need to be a variable taken from the database so the web "admin" can change it

            messages=[
                {
                    "role": "system",
                    "content": "Tu es un assistant de boutique en ligne très direct. Réponds en français, court et utile. Recommande un produit ou réponds à la question."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            options={
                "temperature": 0.7,
                "num_predict": 180  # LIMITS THE AI, DONT WANT TO HAVE A RESPONSE TOO LONG
            }
        )

        answer = response["message"]["content"]

        # We send back the its answer
        return JsonResponse({"results": [answer]})

    except Exception as e:
        import traceback
        print("Erreur Ollama Cloud :", str(e))
        print(traceback.format_exc())

        return JsonResponse({
            "results": [f"Erreur : impossible de contacter l'IA pour le moment ({str(e)})"],
            "error": True
        }, status=503)
    ai_products_list = list(ai_choice)
    return JsonResponse({"results": ai_products_list})

def comparer(request, pk):
    product = get_object_or_404(Product, pk=pk)

    return render(request, 'eshop/comparer.html', {'product': product})


# --------------------------------- modif meg------------------------

