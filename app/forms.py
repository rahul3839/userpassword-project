from dataclasses import fields
from pyexpat import model
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm


class UserForm(UserCreationForm): #  inheritance 
    password2 = forms.CharField(label='confirm password (again)',widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')
        labels = {'email':'Email'}

# -----to show the data in form-------
class EditUserProfileForm(UserChangeForm):
    password = None
    class Meta:
        model= User
        fields = ['username','first_name','last_name','email','last_login','date_joined']
        labels = {'email':'Email'}
    
#-------------Admin--------------------
class EditAdminProfileForm(UserChangeForm):
    password = None
    class Meta:
        model= User
        fields = '__all__'
        labels = {'email':'Email'}