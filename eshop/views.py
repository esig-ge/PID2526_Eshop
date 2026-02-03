from json import JSONDecodeError

from django.shortcuts import render, redirect
from django.http import JsonResponse
from eshop.models import Product, Review
from .forms import PostReview
from .models import Product
from django.shortcuts import render, get_object_or_404
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

# modif meg
def product_list(request):
    products = Product.objects.all()

    # Récupération des paramètres
    query = request.GET.get('q')
    category = request.GET.get('cat')
    stock_only = request.GET.get('stock')
    tri = request.GET.get('tri')

    # Filtrage
    if query:
        products = products.filter(name__icontains=query)

    if category:
        products = products.filter(category__slug=category)  # Assure-toi d'avoir un champ category dans ton modèle

    if stock_only == 'on':
        products = products.filter(availability=True)

    # Tri final
    if tri == 'asc':
        products = products.order_by('price')
    elif tri == 'desc':
        products = products.order_by('-price')

    return render(request, 'eshop/votre_page.html', {'products': products})