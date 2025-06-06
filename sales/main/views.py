from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def index(request):
    return render(request, 'main/index.html')

def login_user(request):
    error_auth = False
    error_fields = False

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not password:
            error_fields = True
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error_auth = True

    return render(request, 'main/login.html', {
        'error_auth': error_auth,
        'error_fields': error_fields
    })

def logout_user(request):
    logout(request)
    return redirect('login')
