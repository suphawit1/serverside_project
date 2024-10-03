from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["group"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})

    group = forms.ModelChoiceField(queryset=Group.objects.all())

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'group',
            'username', 
            'email', 
            'password1', 
            'password2'
            ]
        widgets = {
            "first_name": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter firstname'
                }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter lastname'
                }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
                }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email'
                }),
        }