from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import CustomAuthenticationForm, CustomUserCreationForm

def register(request):
    if request.user.is_authenticated:
        return redirect('home') 

    try:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = CustomUserCreationForm()
    except Exception as e:
        print(f"An error occurred during registration: {e}")
        return render(request, 'templates/authetication/signup.html', {'form': form, 'error': 'An error occurred. Please try again.'})
    
    return render(request, 'templates/authetication/signup.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home') 

    try:
        if request.method == 'POST':
            form = CustomAuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
        else:
            form = CustomAuthenticationForm()
    except Exception as e:
        print(f"An error occurred during login: {e}")
        return render(request, 'templates/authetication/login.html', {'form': form, 'error': 'An error occurred. Please try again.'})
    
    return render(request, 'templates/authetication/login.html', {'form': form})

@login_required
def user_logout(request):
    try:
        logout(request)
    except Exception as e:
        print(f"An error occurred during logout: {e}")
        return redirect('home') 
    
    return redirect('login')
