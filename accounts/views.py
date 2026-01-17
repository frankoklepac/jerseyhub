from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("login") 
    else:
        form = RegisterForm()  
    return render(request, "auth/register.html", {"form": form})

class CustomLoginView(LoginView):
    template_name = "auth/login.html"

def logout_view(request):
    logout(request)
    return render(request, "home.html")

def home(request):
    return render(request, "home.html")