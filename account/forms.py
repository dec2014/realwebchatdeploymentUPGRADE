from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email', widget=forms.TextInput(attrs={
        'class': 'w-full py-4 px-6 rounded-xl border',
        'placeholder': 'Your email address'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full py-4 px-6 rounded-xl border',
        'placeholder': 'Your password'
    }))


class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'role', 'password',)
        widgets = {
            'email': forms.TextInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'role': forms.Select(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'password': forms.TextInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            })
        }
        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password"])  # 🔥 FIX
            if commit:
                user.save()
            return user


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'role',)
        widgets = {
            'email': forms.TextInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'role': forms.Select(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            })
        }