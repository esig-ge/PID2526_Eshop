from django.urls import path
from eshop import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('get/<int:pk>/', views.product_details, name='product_details'),
]