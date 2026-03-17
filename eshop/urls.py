from django.urls import path
from django.contrib.auth import views as auth_views
from eshop import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product_search_result/', views.get_all_products_json, name='product_search_result'),
    path('our_products/', views.view_products, name='our_products'),
    path('get/<int:pk>/', views.product_details, name='product_details'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='eshop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='product_list'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='eshop/password_reset_form.html',
        email_template_name='eshop/password_reset_email.html',
        subject_template_name='eshop/password_reset_subject.txt',
        success_url='/password_reset/done/'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='eshop/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='eshop/password_reset_confirm.html',
        success_url='/reset/done/'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='eshop/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('profile/', views.profile, name='profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
    # Modifier un avis
    path('review/<int:pk>/edit/', views.review_edit, name='review_edit'),
    # Supprimer un avis
    path('review/<int:pk>/delete/', views.review_delete, name='review_delete'),
    path("ajax_search", views.product_search, name="ajax_search"),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path("ai_search", views.ai_search, name="ai_search"),
    path('comparer/', views.comparer, name='comparer'),
    path('comparer/add/<int:pk>/', views.comparer_add, name='comparer_add'),
    path('comparer/remove/<int:pk>/', views.comparer_remove, name='comparer_remove'),
    path('comparer/clear/', views.comparer_clear, name='comparer_clear'),
    #path('facture/<int:order_id>/', views.facture_view, name='facture'),
    path("checkout/", views.checkout_create_session, name="checkout"),
    path("checkout/info/", views.checkout_info, name="checkout_info"),
    path("checkout/success/", views.checkout_success, name="checkout_success"),
    path("checkout/cancel/", views.checkout_cancel, name="checkout_cancel"),
    path("stripe/webhook/", views.stripe_webhook, name="stripe_webhook"),
    path('facture_demo/<int:order_id>/', views.facture_demo, name='facture_demo'),
    path('ai_settings/', views.ai_settings, name='ai_settings'),


]