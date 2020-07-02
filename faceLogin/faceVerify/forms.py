from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

class NewUserForm(UserCreationForm):
    email = forms.EmailField()
    picture = forms.ImageField()
    class Meta():
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data.get("email")
        user.picture = self.cleaned_data.get("picture")
        if commit:
            user.save()
        return user

class NewAuthenticationForm(AuthenticationForm):
    image = forms.ImageField()