from django.shortcuts import render

from eshop.models import Product

from django.shortcuts import render, get_object_or_404
# Create your views here.



def product_list(request):
    products = Product.objects.all()
    return render(request, "eshop/product_list.html", {'products': products})

def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'eshop/product_details.html', {'product': product})



