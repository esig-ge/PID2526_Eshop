from django.test import TestCase
from eshop.models import CustomUser, Product, Review, Cart, CartItem, AiSettings, Order, OrderItem
from django.utils import timezone

class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(email='test@example.com', password='password123')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_no_email(self):
        with self.assertRaisesMessage(ValueError, "L'adresse email est obligatoire"):
            CustomUser.objects.create_user(email='', password='password123')

    def test_create_superuser(self):
        admin_user = CustomUser.objects.create_superuser(email='admin@example.com', password='password123')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            description='A product for testing',
            price=19.99,
            availability=True
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, 19.99)
        self.assertTrue(self.product.availability)

    def test_product_publish(self):
        # Even though publish just calls save, we should test it runs without error
        self.product.name = 'Updated Product'
        self.product.publish()
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')

    def test_create_product_method(self):
        new_product = Product()
        new_product.create_product('New Prod', 'Desc', 25.50, False)
        self.assertEqual(new_product.name, 'New Prod')
        self.assertFalse(new_product.availability)

    def test_change_availability(self):
        self.product.change_availability(False)
        self.assertFalse(self.product.availability)


class ReviewModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='P1', description='D1', price=10.0, availability=True)

    def test_review_creation(self):
        review = Review.objects.create(
            product=self.product,
            user_mail='reviewer@example.com',
            review='Great product!'
        )
        self.assertEqual(review.user_mail, 'reviewer@example.com')
        self.assertEqual(str(review), f"avis {review.pk} pour {self.product}")


class CartModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user('user@example.com', 'pwd')
        self.product = Product.objects.create(name='P1', description='D', price=10.0, availability=True)

    def test_cart_item_sub_total(self):
        cart = Cart.objects.create(owner=self.user)
        cart_item = CartItem.objects.create(product=self.product, cart=cart, quantity=3)
        self.assertEqual(cart_item.sub_total(), 30.0)


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user('buyer@example.com', 'pwd')
        self.product1 = Product.objects.create(name='P1', description='D1', price=15.0, availability=True)
        self.product2 = Product.objects.create(name='P2', description='D2', price=20.0, availability=True)

    def test_order_and_items_cost(self):
        order = Order.objects.create(user=self.user, total_price=0)
        item1 = OrderItem.objects.create(order=order, product=self.product1, price=15.0, quantity=2)
        item2 = OrderItem.objects.create(order=order, product=self.product2, price=20.0, quantity=1)
        
        self.assertEqual(item1.get_cost(), 30.0)
        self.assertEqual(item2.get_cost(), 20.0)
        self.assertEqual(order.get_total_cost(), 50.0)


class AiSettingsModelTest(TestCase):
    def test_sub_total_format(self):
        settings = AiSettings.objects.create(aiModel="test-model", temperature=0.5, num_predict=100)
        self.assertEqual(settings.sub_total(), "test-model 0.5 100")
