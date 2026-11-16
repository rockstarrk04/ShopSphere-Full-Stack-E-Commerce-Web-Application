from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    fname = forms.CharField(max_length=30)
    lname = forms.CharField(max_length=30)
    email = forms.EmailField()
    uname = forms.CharField(max_length=150)
    upass = forms.CharField(widget=forms.PasswordInput)
    cpass = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('upass') != cleaned.get('cpass'):
            raise forms.ValidationError('Passwords do not match')
        return cleaned

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['uname'],
            password=self.cleaned_data['upass'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['fname'],
            last_name=self.cleaned_data['lname'],
        )
        return user
