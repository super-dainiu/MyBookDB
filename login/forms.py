from django import forms


class Login(forms.Form):
    username = forms.CharField(max_length=40, label="Username")
    password = forms.CharField(max_length=128, label="password")