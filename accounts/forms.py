import django.forms
from django import forms
from .views import User
from django.core.validators import validate_email


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=100)
    birth_date = forms.DateField(input_formats='%d-%m-%Y',
                                 widget=django.forms.DateInput(attrs={'placeholder': "__-__-____"}))
    email = forms.EmailField(max_length=100, validators=[validate_email])
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birth_date', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
