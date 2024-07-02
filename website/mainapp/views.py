from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


@login_required()
def index(request):
    if request.method == 'POST':
        logout(request)
        return redirect('register/login')
    else:
        return render(request, 'mainapp/index.html')

