from django import forms

from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order

        fields = (
            'name',
            'email',
            'phone',
            'address',
            'city',
        )

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your full name',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter your email address',
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your phone number',
                }
            ),
            'address': forms.Textarea(
                attrs={
                    'placeholder': 'Enter your complete address',
                    'rows': 4,
                }
            ),
            'city': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your city',
                }
            ),
        }