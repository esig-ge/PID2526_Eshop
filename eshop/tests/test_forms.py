from django.test import TestCase
from eshop.forms import PostReview, ProductForm, AiSettingsForm, RegisterForm
from eshop.models import Product, Review
from django.contrib.auth import get_user_model

User = get_user_model()

class PostReviewFormTest(TestCase):
    def test_valid_review(self):
        form_data = {
            'user_mail': 'test@test.com',
            'review': 'This is a long enough review without any phone number.'
        }
        form = PostReview(data=form_data)
        self.assertTrue(form.is_valid())

    def test_short_review_invalid(self):
        form_data = {
            'user_mail': 'test@test.com',
            'review': 'Too short'
        }
        form = PostReview(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Le texte de l'avis doit faire au moins 10 caractères.", form.errors['review'])

    def test_phone_number_in_review_invalid(self):
        form_data = {
            'user_mail': 'test@test.com',
            'review': 'Here is a phone number 0123456789 to call.'
        }
        form = PostReview(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Le texte de l'avis ne doit pas contenir de numéro de téléphone.", form.errors['review'])

class ProductFormTest(TestCase):
    def test_product_form_valid(self):
        form_data = {
            'name': 'Laptop',
            'description': 'A very good laptop for gaming.',
            'price': 999.99,
            'availability': True,
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())

class RegisterFormTest(TestCase):
    def test_register_form_valid(self):
        form_data = {
            'email': 'newuser@example.com',
        }
        form = RegisterForm(data=form_data)
        # Note: UserCreationForm requires passwords when validating usually,
        # but the provided custom form just defines fields=('email',). 
        # Actually UserCreationForm will expect password and password confirmation unless removed.
        # Let's check if it raises password required.
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)
