from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .forms import RegisterUserForm, PasswordsChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from django.contrib.messages.views import SuccessMessageMixin


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, ("Ім'я або пароль не вірний, спробуйте ще!"))
            return redirect('login')
    else:
        return render(request, 'authentication/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Ви успішно вийшли з акаунта!"))
    return redirect('index')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            if User.objects.filter(email=email):
                messages.error(request, (f"Електронна адреса {email} вже використовується! Оберіть іншу."))
                return render(request, 'authentication/register.html', {'form':form})
            else:
                form.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, ("Ви успішно зареєструвалися!"))
                return redirect('index')
    else:
        form = RegisterUserForm()

    return render(request, 'authentication/register.html', {'form':form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            if current_user.email == email or len(User.objects.filter(email=email)) == 0:      
                current_user.username = username
                current_user.email = email
                current_user.save()
                login(request, current_user)
                messages.success(request, ("Ваші данні збереженні!"))
                return redirect('index')

            else:
                messages.error(request, (f"Електронна адреса {email} вже використовується! Оберіть іншу."))

        form = RegisterUserForm(request.POST or None, instance=current_user)
        return render(request, 'authentication/update_user.html', {'form':form})

    else:
        messages.error(request, ("Ви повинні зареєструватися для доступу до цієї сторінки!"))
        return redirect('login')

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordsChangeForm
    template_name = 'authentication/change_password.html'   
    success_url = reverse_lazy('update_user')

    def form_valid(self, form):
        messages.success(self.request, "Ваш пароль успішно змінено!")
        return super().form_valid(form)