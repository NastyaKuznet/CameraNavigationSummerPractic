from django.contrib.auth.models import User
from django.shortcuts import render
from django.db.models import Count
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required

@login_required()
def get_statistic(request):
    n = 3
    times = []
    for i in range(n):
        times.append(datetime.now() - timedelta(days=3))
    registered_users_last = []
    for i in range(n):
        registered_users_last.append(User.objects.filter(date_joined__gte=times[i]).count())

    return render(request, 'statistic/statistic.html')