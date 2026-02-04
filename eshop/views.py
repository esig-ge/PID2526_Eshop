from json import JSONDecodeError

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from eshop.models import Product, Review, Cart, CartItem
from .forms import PostReview
from django.shortcuts import render, get_object_or_404
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
    try:
        query = request.GET.get("q", "")

        client = genai.Client()

        ai_choice = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents="Give back a single product link (found on digitec.ch) that answers the best to this request :" + query,
        )

    except JSONDecodeError:
        ai_choice = Product.objects.none()

    ai_products_list = list(ai_choice)
    return JsonResponse({"results": ai_products_list})

def comparer(request, pk):
    product = get_object_or_404(Product, pk=pk)

    return render(request, 'eshop/comparer.html', {'product': product})