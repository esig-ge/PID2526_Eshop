from django import forms
import re
from .models import Review, AiSettings, Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'availability', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du produit'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Description du produit'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix'}),
            'availability': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class PostReview(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('user_mail', 'review')

    # Validation du champ review pour interdire les numéros de téléphone
    def clean_review(self):
        review_text = self.cleaned_data.get('review')

        # Vérifier la longueur minimum
        if review_text and len(review_text) < 10:
            raise forms.ValidationError("Le texte de l'avis doit faire au moins 10 caractères.")

        # Vérifier qu'il n'y a pas de numéro de téléphone (10 chiffres consécutifs)
        if re.search(r'\b\d{10}\b', review_text):
            raise forms.ValidationError("Le texte de l'avis ne doit pas contenir de numéro de téléphone.")

        return review_text


class AiSettingsForm(forms.ModelForm):
    class Meta:
        model = AiSettings         # <-- ici on met le modèle exact
        fields = ['aiModel', 'prompt']  # <-- noms exacts des champs
        widgets = {
            'aiModel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du modèle AI'}),
            'prompt': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Prompt par défaut'}),
        }


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control form-control-lg'
