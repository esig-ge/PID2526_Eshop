from json import JSONDecodeError
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse,HttpResponse
from eshop.models import Product, Review, Cart, CartItem
from .forms import PostReview
from django.shortcuts import render, get_object_or_404
from ollama import Client
from django.db.models import Q
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import os
import stripe
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Create your views here.

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
            resultats = Product.objects.filter(
                name__icontains=query
            ).values('id', 'name', 'price')
        else:
            resultats = Product.objects.none()

    except JSONDecodeError:
        resultats = Product.objects.none()

    # 👉 Formatage backend ici
    results_list = []
    for p in resultats:
        results_list.append({
            "id": p["id"],
            "name": p["name"],
            "price": f"{p['price']:.2f}"   # <-- solution
        })

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
    #api key getter for ollama
    api_key_ollama = os.getenv("API_KEY_OLLAMA")
    if not api_key_ollama:
        raise ValueError("API_KEY_OLLAMA not set in environment")

    query = request.GET.get("q", "")

    if len(query) < 2:
        return JsonResponse({"results": []})

    try:

        if not api_key:
            raise ValueError("Aucune clé API Ollama configurée")

        client = Client(
            host="https://ollama.com",
            headers={
                "Authorization": f"Bearer {api_key_ollama}"
            }
        )

        # Ollama API call
        response = client.chat(
            model="gemma3:27b",  # ← this one will need to be a variable taken from the database so the web "admin" can change it

            messages=[
                {   # Ai instructions -> system role are for those
                    "role": "system",
                    "content": "Tu es un assistant de boutique en ligne très direct. Réponds en français, court et utile. Recommande un produit en me retournant un json avec name ,link ,prix ,resume , img_url"
                },
                {   # Actuel Query -> user role is for actual queries
                    "role": "user",
                    "content": query
                }
            ],
            options={
                "temperature": 0.7, # Temperature controls randomness/creativity in the model’s output
                "num_predict": 180  # LIMITS THE AI CHAR RESPONSE, DONT WANT TO HAVE A RESPONSE TOO LONG
            }
        )

        answer = response["message"]["content"]

        # Clean potential markdown wrappers (e.g., ```json ... ```)
        if answer.startswith('```json'):
            answer = answer[7:].strip()  # Remove ```json
        if answer.endswith('```'):
            answer = answer[:-3].strip()

        try:
            parsed_data = json.loads(answer)
        except json.JSONDecodeError:
                # Fallback if not valid JSON: wrap the raw text
                parsed_data = {
                    "name": "Erreur de parsing",
                    "link": "",
                    "prix": "",
                    "resume": answer,  # put the raw answer here
                    "img_url": ""
                }

            # Clean and standardize the dict (e.g., ensure all keys exist, add defaults if missing)
        clean_dict = {
            "name": parsed_data.get("name", "Produit inconnu"),
            "link": parsed_data.get("link", ""),
            "prix": parsed_data.get("prix", "Prix indisponible"),
            "resume": parsed_data.get("resume", "Pas de résumé disponible"),
            "img_url": parsed_data.get("img_url", "")
            }

            # Wrap in a consistent format for JS (e.g., as results list with one item)
        return JsonResponse({"results": [clean_dict]})

    except Exception as e:
        import traceback
        print("Erreur Ollama Cloud :", str(e))
        print(traceback.format_exc())

        return JsonResponse({"results": [f"Erreur : impossible de contacter l'IA pour le moment ({str(e)})"],"error": True}, status=503)

def _get_compare_ids(request):
    compare_ids = request.session.get('compare_ids', [])
    return compare_ids if isinstance(compare_ids, list) else []


def comparer(request):
    compare_ids = _get_compare_ids(request)
    products = Product.objects.filter(id__in=compare_ids)

    return render(request, 'eshop/comparer.html', {'products': products})


@require_POST
def comparer_add(request, pk):
    get_object_or_404(Product, pk=pk)

    compare_ids = _get_compare_ids(request)
    added = False

    if pk not in compare_ids:
        compare_ids.append(pk)
        request.session['compare_ids'] = compare_ids
        request.session.modified = True
        added = True

    # Réponse AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'ok': True,'added': added,'count': len(compare_ids),'compare_ids': compare_ids})

    return redirect('comparer')


@require_POST
def comparer_remove(request, pk):
    compare_ids = _get_compare_ids(request)

    if pk in compare_ids:
        compare_ids.remove(pk)
        request.session['compare_ids'] = compare_ids
        request.session.modified = True

    return redirect('comparer')


@require_POST
def comparer_clear(request):
    request.session['compare_ids'] = []
    request.session.modified = True

    return redirect('comparer')

stripe.api_key = settings.STRIPE_SECRET_KEY


@require_POST
def checkout_create_session(request):
    # Ton panier semble être en DB (cart_items). Souvent lié à l'utilisateur.
    # Si c’est bien ça, on filtre par request.user.
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect("cart_detail")

    line_items = []
    for item in cart_items:
        line_items.append({
            "price_data": {
                "currency": "chf",
                "product_data": {
                    "name": item.product.name,
                },
                "unit_amount": int(round(float(item.product.price) * 100)),  # centimes
            },
            "quantity": int(item.quantity),
        })

    success_url = request.build_absolute_uri(reverse("checkout_success"))
    cancel_url = request.build_absolute_uri(reverse("checkout_cancel"))

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=line_items,
        success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=cancel_url,
    )

    return redirect(session.url, permanent=False)


def checkout_success(request):
    return render(request, "eshop/checkout_success.html")


def checkout_cancel(request):
    return render(request, "eshop/checkout_cancel.html")


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session.get("metadata", {}).get("user_id")

        if user_id:
            # Exemple : vider le panier après paiement confirmé
            CartItem.objects.filter(user_id=user_id).delete()

    return HttpResponse(status=200)

# --------------------------------- modif meg------------------------
def product_list(request):
    products = Product.objects.all()
    query = request.GET.get('q')
    category = request.GET.get('cat')
    sort_order = request.GET.get('tri')
    in_stock = request.GET.get('stock')

    # 3. Filtrage par mot-clé (Recherche intelligente)
    if query:
        products = products.filter(name__icontains=query)
    # 4. Filtrage par catégorie
    if category:
        products = products.filter(
            Q(name__icontains=category) | Q(description__icontains=category))  # 5. Filtrage par stock
    # 5. Filtrage par stock
    show_dispo = request.GET.get('dispo')
    if show_dispo == 'on':
        products = products.filter(availability=True)
    # 6. Tri par prix (Croissant / Décroissant)
    if sort_order == 'asc':
        products = products.order_by('price')
    elif sort_order == 'desc':
        products = products.order_by('-price')

#     if in_stock == 'true':
    #         products = products.filter(availability=True)
    #     elif in_stock == 'false':  # Utilise elif et sors-le du premier bloc if
    #         products = products.filter(availability=False)

    return render(request, 'eshop/product_list.html', {'products': products,'tri': sort_order})

def facture_view(request, order_id):
    # Si order_id n'existe pas en BDD, ça retourne 404
    order = get_object_or_404(Order, id=order_id)

    # On vérifie aussi que la facture appartient bien à l'utilisateur connecté
    if order.user != request.user:
        from django.http import Http404
        raise Http404("Vous n'avez pas l'autorisation de voir cette facture.")

    context = {
        'order': order,
        'cart_items': order.items.all(),  # On récupère les items liés à la commande
        'total': order.get_total_cost(),
    }
    return render(request, 'eshop/facture.html', context)


def get_aiSettings(request):
    settings = AiSettings.objects.first()
    if not settings:
        return JsonResponse({"error": "AISettings not found"}, status=404)

    data = {
        "model": settings.model,
        "prompt": settings.prompt,
        }
    return JsonResponse(data)

# #facture meg
# def facture_pdf(request, order_id):
#     # 1. Récupérer la commande
#     order = get_object_or_404(Order, id=order_id)
#
#     # 2. Préparer les données pour le template de facture
#     context = {'order': order}
#
#     # 3. Rendre le template HTML en chaîne de caractères
#     html_string = render_to_string('eshop/facture_template.html', context)
#
#     # 4. Générer le PDF
#     html = HTML(string=html_string, base_url=request.build_absolute_uri())
#     pdf = html.write_pdf()
#
#     # 5. Renvoyer le fichier PDF
#     response = HttpResponse(pdf, content_type='application/pdf')
#     # 'attachment' pour forcer le téléchargement, 'inline' pour l'ouvrir dans le navigateur
#     response['Content-Disposition'] = f'attachment; filename="facture_{order.id}.pdf"'
#
#     return response