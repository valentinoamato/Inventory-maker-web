from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password1 = forms.CharField(max_length=30,widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=30,widget=forms.PasswordInput)

class IvtForm(forms.Form):
    name = forms.CharField(max_length=200)

class ItmForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(max_length=1000)

