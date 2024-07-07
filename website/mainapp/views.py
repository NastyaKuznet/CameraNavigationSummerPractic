from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import logout
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import sys
sys.path.append('D:\Python\CameraNavigation\CameraNavigationSummerPractic')
import analyzeData.analyzerData as ad

@login_required()
def index(request):
    return render(request, 'mainapp/index.html')


class MyForm(forms.Form):
    lx = forms.CharField(max_length=255)
    ly = forms.CharField(max_length=255)
    rx = forms.CharField(max_length=255)
    ry = forms.CharField(max_length=255)
    sx = forms.CharField(max_length=255)
    sy = forms.CharField(max_length=255)
    ts = forms.CharField(max_length=255)
    te = forms.CharField(max_length=255)


@login_required()
def button_click(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            x0_f = form.cleaned_data['lx']
            y0_f = form.cleaned_data['ly']
            x1_f = form.cleaned_data['rx']
            y1_f = form.cleaned_data['ry']
            size_x = form.cleaned_data['sx']
            size_y = form.cleaned_data['sy']
            time_start: str = form.cleaned_data['ts']
            time_end: str = form.cleaned_data['te']
            chart, answ, bad_photo = ad.AnalyzerData.start_demo4(int(x0_f), int(y0_f), int(x1_f), int(y1_f), int(size_x), int(size_y), time_start, time_end, 800, 600)
            context = {'chart': chart, 'answer': answ, "bad_photo": bad_photo}
            return render(request, 'mainapp/index.html', context)
    else:
        return render(request, 'mainapp/index.html')


@login_required()
def log_out(request):
    logout(request)
    return redirect('/register/login')


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
