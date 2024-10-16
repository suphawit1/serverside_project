from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["group"].widget.attrs.update({"class": "form-select","placeholder": "Role"})
        self.fields['group'].empty_label = "--- Select a Role ---"
        self.fields['group'].label = 'Role'
        self.fields["password1"].widget.attrs.update({"class": "form-control","placeholder": "Enter password"})
        self.fields["password2"].widget.attrs.update({"class": "form-control","placeholder": "Confirm password"})

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
        labels ={
            'first_name': 'ชื่อ',
            'last_name': 'นามสกุล',
            'group': 'ตำแหน่ง',
            'username': 'ชื่อผู้ใช้',
            'email': 'อีเมล',
            'password1': 'รหัสผ่าน',
            'password2': 'ยืนยันรหัสผ่าน',
        }

class LoginForm(AuthenticationForm):
      def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control","placeholder": "username"})
        self.fields["password"].widget.attrs.update({"class": "form-control","placeholder": "password"})

class NewPasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'ใส่รหัสผ่านเดิม'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'ใส่รหัสผ่านใหม่'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'ยืนยันรหัสผ่านใหม่'
        })

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets  = {
            "username": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ใส่ชื่อผู้ใช้ใหม่'
                })
        }
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            if self.instance.pk is not None and self.instance.username == username:
                return username
            raise forms.ValidationError("มีชื่อผู้ใช้นี้แล้ว")
        return username

