from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from django.forms.widgets import TextInput, PasswordInput

from django.urls import reverse


class UserRegistration(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    

    def __init__(self, *args, **kwargs):
       super(UserRegistration, self).__init__(*args, **kwargs)
       self.fields['email'].required = True
    

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists() or len(email) < 4 or len(email) > 50:
            raise forms.ValidationError('Email Id is either already exist or incorrect!')
        
        return email


class UserLogin(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# Update Profile
class UserUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        exclude = ['password1', 'password2']
    

    def __init__(self, *args, **kwargs):
       super(UserUpdate, self).__init__(*args, **kwargs)
       self.fields['email'].required = True
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists() or len(email) < 4 or len(email) > 50:
            raise forms.ValidationError('Email Id is either already exist or incorrect!')
        
        return email
        
    
