from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.utils.safestring import mark_safe
from jinja2 import Template


def index(request, path='static/b.png'):
    return render(request, 'mainapp/index.html', {'image_url': path})


class MyForm(forms.Form):
    lx = forms.CharField(max_length=255)
    ly = forms.CharField(max_length=255)
    rx = forms.CharField(max_length=255)
    ry = forms.CharField(max_length=255)
    sx = forms.CharField(max_length=255)
    sy = forms.CharField(max_length=255)
    ts = forms.CharField(max_length=255)
    te = forms.CharField(max_length=255)


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
            image_path = '../static/kot.gif'

            # хтмл код можно так отрендерить и отдать:
            '''template = Template('<h1>Hello, {{ name }}!</h1>')
            rendered_html = template.render(name='John Doe')
            return HttpResponse(rendered_html)'''

            return index(request, image_path)
    else:
        return index(request)
