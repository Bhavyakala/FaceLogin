from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

class NewUserForm(UserCreationForm):
    email = forms.EmailField()
    picture = forms.ImageField()
    description = forms.CharField(max_length=250)
    class Meta():
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(NewUserForm, self).save(commit=True)
        user.email = self.cleaned_data.get('email')
        user.save()
        return user

class NewAuthenticationForm(AuthenticationForm):    
    image = forms.CharField(widget=forms.HiddenInput())