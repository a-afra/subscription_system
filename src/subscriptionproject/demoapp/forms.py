from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class SignupForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', 'email']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            try:
                customer = Customer.objects.get(username=username)
                if not customer.check_password(password):
                    raise forms.ValidationError("Invalid password")
            except Customer.DoesNotExist:
                raise forms.ValidationError("Invalid username")
        return cleaned_data