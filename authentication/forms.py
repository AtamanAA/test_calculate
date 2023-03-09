from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Ім'я", max_length=15, error_messages={'max_length': "Введіть коротше ім'я"})
    email = forms.EmailField(label="E-mail", max_length=40, error_messages={'invalid': 'Введіть коректну адресу пошти!'})
    password1 = forms.CharField(label='Пароль', max_length=20, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторити пароль', max_length=20, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'auth__field'
        self.fields['email'].widget.attrs['class'] = 'auth__field'
        self.fields['password1'].widget.attrs['class'] = 'auth__field'
        self.fields['password2'].widget.attrs['class'] = 'auth__field'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Два поля пароля не збігаються")
        return password2


class PasswordsChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старий пароль', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='Новий пароль', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Повторити новий пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super(PasswordsChangeForm, self).__init__(*args, **kwargs)        
        self.fields['old_password'].widget.attrs['class'] = 'auth__field'
        self.fields['new_password1'].widget.attrs['class'] = 'auth__field'
        self.fields['new_password2'].widget.attrs['class'] = 'auth__field'        