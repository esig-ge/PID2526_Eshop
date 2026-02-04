from django.urls import path
from eshop import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('get/<int:pk>/', views.product_details, name='product_details'),
    # Modifier un avis
    path('review/<int:pk>/edit/', views.review_edit, name='review_edit'),
    # Supprimer un avis
    path('review/<int:pk>/delete/', views.review_delete, name='review_delete'),
    path("ajax_search", views.product_search, name="ajax_search"),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]