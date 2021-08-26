from django import forms
from School_MS.models import StudentProfile, Courses
from Project import settings
from django.db import models
from django.forms import ModelForm
from datetime import *
from School_MS.models import *
from django.forms.widgets import*
from django.db.models.fields import CharField


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password')
        Widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }


class StudentProfileInfoForm(forms.ModelForm):
    class Meta():
        model = StudentProfile
        fields = ('profile_pic', 'date_of_birth', 'phone_nb')
        widgets = {
            'profile_pic':FileInput(attrs={'class':"form-control", 'type':"file"}),
            'date_of_birth': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'phone_nb': forms.TextInput(attrs={'class': 'form-control','placeholder':"+961/your phone number"})
        }
        
        
class ContactForm(forms.Form):
    """
    Contact form to contact admin, with auth
    """
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    Widgets = {
    'email':Textarea(attrs={'class':'form-control'} ),
    'subject':Textarea(attrs={'class':'form-control'} ),
    'message':Textarea(attrs={'class':'form-control'} ),

    }
    