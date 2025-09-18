from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nome')
    last_name = forms.CharField(max_length=30, required=True, label='Cognome')
    email = forms.EmailField(max_length=254, required=True, label='Email')
    data_nascita = forms.DateField(required=True, widget=forms.DateInput(attrs={'type':'date'}), label='Data di nascita')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'data_nascita', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(user=user, data_nascita=self.cleaned_data['data_nascita'])
        return user
