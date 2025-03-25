from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.core.exceptions import ValidationError

from authentication.models import UserProfile


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField(validators=[validators.EmailValidator])
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = UserProfile
        fields = ["first_name", "last_name", "username", "email", "password1", "password2" ]

    def clean_email(self):
        """
        Validates the email field to ensure it is unique.

        This method checks if the provided email address already exists in the database.
        If the email is already registered, it raises a ValidationError.

        Returns:
            str: The validated email address if it is unique.

        Raises:
            ValidationError: If the email address is already registered.
        """
        email = self.cleaned_data.get("email")
        if UserProfile.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered. Please use a different email.")
        return email

class LoginForm(forms.Form):
    email = forms.EmailField(required=True, validators=[validators.EmailValidator])
    password = forms.CharField(required=True, widget=forms.PasswordInput)
