from django.shortcuts import render


# Create your views here.
from django.contrib.auth.decorators import login_required
import sys
sys.path.append('D:\Python\CameraNavigation\CameraNavigationSummerPractic\myversion\general')
from DBHelper import DBHelper


@login_required()
def index(request):
    name = request.GET.get('name')
    db = DBHelper(database="big_brother", user="postgres", password="1111", host='localhost')
    db.exec("select l.id, l.name "
            "from location l join map m on m.id = l.id_map "
            "join users u on u.id = m.id_user "
            f"where u.name = '{name}'")
    locations = db.fetch_all()
    return render(request, 'main/main.html', {'locations': locations})
