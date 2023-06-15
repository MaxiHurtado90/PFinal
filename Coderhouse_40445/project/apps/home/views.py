from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from venta.models import Vendedor
from django.contrib.admin.views.decorators import staff_member_required


def index(request):
    return render(request, 'home/index.html')


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home:index')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'home/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return render(request, 'home/logout.html')



def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            is_vendedor = form.cleaned_data.get("is_vendedor", False)
            if request.user.is_superuser:
                user.is_staff = True
                user.is_superuser = True
                user.is_vendedor = True
                user.save()
            else:
                user.is_staff = False
            user.save()
            return redirect('home:index')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'home/register.html', context)


def about(request):
    return render(request, 'home/about.html')


def about_me(request):
    return render(request, 'home/about_me.html')
