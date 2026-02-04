from json import JSONDecodeError

from django.shortcuts import render, redirect
from django.http import JsonResponse
from eshop.models import Product, Review
from .forms import PostReview
from .models import Product
from django.shortcuts import render, get_object_or_404
import google.generativeai as genai
from django.db.models import Q

import os
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
            resultats = Product.objects.filter(name__icontains=query).values('id', 'name', 'price')

        else:
            resultats = Product.objects.none()

    except JSONDecodeError:
        resultats = Product.objects.none()

    results_list = list(resultats)
    return JsonResponse({"results": results_list})

# --------------------------------- modif meg------------------------


def product_list(request):
    # 1. On récupère tous les produits au départ
    products = Product.objects.all()
    # 2. Récupération des paramètres du formulaire (GET)
    query = request.GET.get('q')
    category = request.GET.get('cat')
    sort_order = request.GET.get('tri')
    in_stock = request.GET.get('stock')

    # 3. Filtrage par mot-clé (Recherche intelligente)
    if query:
        products = products.filter(name__icontains=query)
    # 4. Filtrage par catégorie
    if category:
        products = products.filter(Q(name__icontains=category) | Q(description__icontains=category))    # 5. Filtrage par stock
    if in_stock == 'on':
        products = products.filter(availability=True)
    # 6. Tri par prix (Croissant / Décroissant)
    if sort_order == 'asc':
        products = products.order_by('price')
    elif sort_order == 'desc':
        products = products.order_by('-price')

    return render(request, 'eshop/product_list.html', {'products': products})