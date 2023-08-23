from django import forms
from .models import User


class user_form(forms.forms):
    username = forms.CharField(max_length=60)
    email = forms.EmailField(max_length=50)
    password=forms.CharField(max_length=30,min_length=8)
    cf_password=forms.CharField(max_length=30,min_length=8)

    def clean_cf_password(self,*args,**kwargs):
        cf_password=self.cleaned_data.get('cf_password')
        if cf_password!=self.cleaned_data.get('password'):
            raise forms.ValidationError("password does not match")