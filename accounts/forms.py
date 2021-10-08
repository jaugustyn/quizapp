from django import forms
from .views import User
from django.core.validators import validate_email


class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=100)
    birth_date = forms.DateField()
    email = forms.EmailField(max_length=100, validators=[validate_email])
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),
        }
