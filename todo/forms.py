from django import forms
from django.core.exceptions import ValidationError

email_style_dict = {'type': 'email', 'placeholder': 'Enter email', 'class': 'form-control',
                    'id': 'email', 'name': 'email'}

username_style_dict = {'type': 'text', 'placeholder': 'Enter username', 'class': 'form-control',
                       'id': 'username', 'name': 'username'}

password1_style_dict = {'type': 'password', 'placeholder': 'Enter password', 'class': 'form-control',
                        'id': 'password1', 'name': 'password1'}

password2_style_dict = {'type': 'password', 'placeholder': 'Confirm password', 'class': 'form-control',
                        'id': 'password2', 'name': 'password2'}

password_style_dict = {'type': 'password', 'placeholder': 'Enter password', 'class': 'form-control',
                       'id': 'password', 'name': 'password'}


class RegistrationForm(forms.Form):
    email = forms.CharField(label='Email Address', widget=forms.TextInput(attrs=email_style_dict))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs=username_style_dict))
    password1 = forms.CharField(label='Password', widget=forms.TextInput(attrs=password1_style_dict))
    password2 = forms.CharField(label='Password (Confirm)', widget=forms.TextInput(attrs=password2_style_dict))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        print(password1)

        if password1 and password2:
            if password1 != password2:
                # self.add_error('password1', ValidationError('Password don\'t match.', code='pass_not_match'))
                raise ValidationError('Password don\'t match.', code='pass not match')

            elif len(password1) < 6:
                raise ValidationError('Password must be greater than 5 characters.', code='pass too short')
        return cleaned_data

    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        if email:
            if len(email) < 5:
                raise ValidationError('Email must be greater than 4 characters.', code='pass too short')
        return cleaned_data['email']

    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        if username:
            if len(username) < 2:
                raise ValidationError('Username must be greater than 1 character.', code='pass too short')
        return cleaned_data['username']


class LoginForm(forms.Form):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs=username_style_dict))
    password = forms.CharField(label='Password',
                               widget=forms.TextInput(attrs=password_style_dict))


