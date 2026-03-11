from django.test import TestCase, Client
from django.urls import reverse
from eshop.models import Product, CustomUser, Review, Cart, CartItem
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name='Test Laptop',
            description='A nice test laptop',
            price=1500.0,
            availability=True
        )
        self.user = User.objects.create_user(email='user@test.com', password='password123')

    def test_product_list_GET(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eshop/product_list.html')
        self.assertContains(response, 'Test Laptop')
        
    def test_product_search_AJAX(self):
        response = self.client.get(reverse('ajax_search'), {'q': 'Laptop'})
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(len(json_data['results']), 1)
        self.assertEqual(json_data['results'][0]['name'], 'Test Laptop')

    def test_product_details_GET(self):
        response = self.client.get(reverse('product_details', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eshop/product_details.html')

    def test_product_details_POST_review(self):
        response = self.client.post(reverse('product_details', args=[self.product.pk]), {
            'user_mail': 'reviewer@test.com',
            'review': 'This is a fantastic product! I highly recommend it.'
        })
        self.assertEqual(response.status_code, 302) # Redirects on success
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().user_mail, 'reviewer@test.com')


class CartViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='cartuser@test.com', password='password123')
        self.product = Product.objects.create(
            name='Cart Item',
            description='Test item',
            price=10.0,
            availability=True
        )

    def test_cart_add_unauthenticated(self):
        response = self.client.get(reverse('cart_add', args=[self.product.id]))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_cart_add_authenticated(self):
        self.client.login(username='cartuser@test.com', password='password123')
        response = self.client.get(reverse('cart_add', args=[self.product.id]))
        # Should redirect to cart detail
        self.assertRedirects(response, reverse('cart_detail'))
        self.assertEqual(CartItem.objects.count(), 1)


class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_page_GET(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eshop/login.html')

    def test_register_page_GET(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eshop/register.html')
