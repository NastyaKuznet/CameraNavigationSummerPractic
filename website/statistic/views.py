from django.contrib.auth.models import User
from django.shortcuts import render
from django.db.models import Count
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from plotly import graph_objs as go
from django import forms


class MyForm(forms.Form):
    count_days = forms.CharField(max_length=255)


@login_required()
def get_statistic(request):

    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            n = form.cleaned_data['count_days']
            context = get_stat_new_user(int(n))
    else:
        context = get_stat_new_user(3)
    return render(request, 'statistic/statistic.html', context)


def get_stat_new_user(n):
    times = []
    str_times = []
    for i in range(n):
        times.append(datetime.now() - timedelta(days=i))
        str_times.append(str(times[i].date()))
    registered_users_last = []
    for i in range(n):
        registered_users_last.append(User.objects.filter(date_joined__gte=times[i]).count())
    fig = go.Figure(data=[go.Bar(x=str_times, y=registered_users_last)])
    fig.update_layout(
        title=f"Статистика по количеству новых пользователей за последние дни",
        xaxis_title="Дата",
        yaxis_title="Количество новых пользователей",
        xaxis=dict(tickformat='%Y-%m-%d', type='date',
                   tickmode='array',
                   tickvals=str_times),
    )
    context = {'chart': fig.to_html()}
    return context


