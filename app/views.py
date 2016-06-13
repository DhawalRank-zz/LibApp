from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, get_list_or_404
# Import necessary classes
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect

from app.models import Book, Dvd, Libuser, Libitem


# Create your views here.
@csrf_protect
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            classob = Libitem.objects.filter(username=request.user.username)
            userob = Libuser.objects.get(username=request.user.username)
            request.session['userob'] = userob.username
            return HttpResponseRedirect('/app/index/')
            # else:
            #     d = 'True'
            #     return render(request, 'app/login/', {'notlogin': d})
            # return render(request, 'app/login')


# @login_required
def index(request):
    itemlist = Libitem.objects.all().order_by('title')[:10]
    return render(request, "libapp/index.html", {'itemlist': itemlist})


def about(request):
    return render(request, 'libapp/about.html')


def detail(request, item_id):
    libitem = get_object_or_404(Libitem, id=item_id)
    if libitem.itemtype == 'Book':
        book = get_list_or_404(Book, id=item_id)
        return render(request, 'libapp/detail.html', {'book': book})
    else:
        dvd = get_list_or_404(Dvd, id=item_id)
        return render(request, 'libapp/detail.html', {'dvd': dvd})


def myacct(request):
    return render(request, 'libapp/myacct.html')


def register(request):
    return render(request, 'libapp/register.html')
