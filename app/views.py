import os
from random import randint
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core import serializers
from django.views.generic import View

from app.forms import SuggestionForm, SearchlibForm, LoginForm, Register, MyAcct
from app.models import Book, Dvd, Libuser, Libitem, Suggestion
from django.core.mail import send_mail


# Create your views here.


@csrf_protect
def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            userob = Libuser.objects.get(username=request.user.username)
            luckynum = randint(0, 9)
            request.session['luckynum'] = luckynum
            request.session['profilepic'] = userob.profilepic.url
            request.session.set_expiry(3600)
            userob = Libuser.objects.filter(username=request.user.username)
            request.session['userob'] = serializers.serialize('json', userob)
            response = HttpResponseRedirect('/app/index/')
            response.flush()
            return response
        elif user is None:
            return render(request, 'libapp/login.html', {'notlogin': True, 'form': form})
        else:
            return render(request, 'libapp/login.html', {'notactive': True, 'form': form})
    else:
        return render(request, 'libapp/login.html', {'form': form})


@login_required
def user_logout(request):
    del request.session['userob']
    response = HttpResponseRedirect('/')
    response.delete_cookie('about_visits')
    logout(request)
    return response


def index(request):
    itemlist = Libitem.objects.all().order_by('title')[:10]
    itemlistper = Libitem.objects.filter(user_id__exact=request.user.id)
    userob = Libuser.objects.filter(username=request.user.username)
    return render(request, "libapp/index.html",
                  {'itemlist': itemlist, 'itemlistper': itemlistper, 'userob': userob})


def about(request):
    userob = Libuser.objects.filter(username=request.user.username)
    if 'about_visits' in request.COOKIES:
        about_visits = int(request.COOKIES['about_visits'])
        about_visits += 1
        response = render(request, 'libapp/about.html', {'about_visits': about_visits, 'userob': userob})
        response.set_cookie('about_visits', about_visits)
        return response
    else:
        about_visits = 1
        response = render(request, 'libapp/about.html', {'about_visits': about_visits, 'userob': userob})
        response.set_cookie('about_visits', about_visits)
        return response


def detail(request, item_id):
    libitem = get_object_or_404(Libitem, id=item_id)
    userob = Libuser.objects.filter(username=request.user.username)
    if libitem.itemtype == 'Book':
        book = get_list_or_404(Book, id=item_id)
        return render(request, 'libapp/detail.html', {'book': book, 'userob': userob})
    else:
        dvd = get_list_or_404(Dvd, id=item_id)
        return render(request, 'libapp/detail.html', {'dvd': dvd, 'userob': userob})


def suggestions(request):
    userob = Libuser.objects.filter(username=request.user.username)
    suggestionlist = Suggestion.objects.all()[:10]
    return render(request, 'libapp/suggestions.html', {'itemlist': suggestionlist, 'userob': userob})


def newitem(request):
    suggestionsob = Suggestion.objects.all()
    userob = Libuser.objects.filter(username=request.user.username)
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.num_interested = 1
            suggestion.save()
            return HttpResponseRedirect('/app/suggestions/')
        else:
            return render(request, 'libapp/newitem.html',
                          {'form': form, 'suggestions': suggestionsob, 'userob': userob})

    else:
        form = SuggestionForm()
        return render(request, 'libapp/newitem.html', {'form': form, 'suggestions': suggestionsob, 'userob': userob})


def searchitem(request):
    userob = Libuser.objects.filter(username=request.user.username)
    if request.method == 'POST':
        title1 = request.POST['title']
        author1 = request.POST['author']
        if title1 != '' and author1 != '':  # Title and User not null
            bookob = Book.objects.filter(title__contains=title1, author__contains=author1)
            dvdob = Dvd.objects.filter(title__contains=title1, maker__contains=author1)
            form = SearchlibForm()
            if bookob and dvdob:
                return render(request, 'libapp/searchitem.html',
                              {'bookob': bookob, 'dvdob': dvdob, 'form': form, 'userob': userob})
            elif not bookob and dvdob:
                return render(request, 'libapp/searchitem.html', {'dvdob': dvdob, 'form': form, 'userob': userob})
            elif bookob and not dvdob:
                return render(request, 'libapp/searchitem.html', {'bookob': bookob, 'form': form, 'userob': userob})
            else:
                return render(request, 'libapp/searchitem.html', {'notfound': True, 'form': form, 'userob': userob})

        elif title1 != '' and author1 == '':  # Only Title searched
            bookob = Book.objects.filter(title__contains=title1)
            dvdob = Dvd.objects.filter(title__contains=title1)
            form = SearchlibForm()
            if bookob and dvdob:
                return render(request, 'libapp/searchitem.html',
                              {'bookob': bookob, 'dvdob': dvdob, 'form': form, 'userob': userob})
            elif bookob and not dvdob:
                return render(request, 'libapp/searchitem.html', {'bookob': bookob, 'form': form, 'userob': userob})
            elif not bookob and dvdob:
                return render(request, 'libapp/searchitem.html', {'dvdob': dvdob, 'form': form, 'userob': userob})
            else:
                return render(request, 'libapp/searchitem.html', {'notfound': True, 'form': form, 'userob': userob})

        elif author1 != '' and title1 == '':  # Only Author searched
            bookob = Book.objects.filter(author__contains=author1)
            dvdob = Dvd.objects.filter(maker__contains=author1)
            form = SearchlibForm()
            if bookob and dvdob:
                return render(request, 'libapp/searchitem.html',
                              {'bookob': bookob, 'dvdob': dvdob, 'form': form, 'userob': userob})
            elif bookob and not dvdob:
                return render(request, 'libapp/searchitem.html', {'bookob': bookob, 'form': form, 'userob': userob})
            elif not dvdob and bookob:
                return render(request, 'libapp/searchitem.html', {'dvdob': dvdob, 'form': form, 'userob': userob})
            else:
                form = SearchlibForm()
                return render(request, 'libapp/searchitem.html', {'notfound': True, 'form': form, 'userob': userob})

        else:  # Author and Title null
            form = SearchlibForm()
            return render(request, 'libapp/searchitem.html', {'notinput': True, 'form': form, 'userob': userob})

    else:
        form = SearchlibForm()
        return render(request, 'libapp/searchitem.html', {'form': form, 'userob': userob})


class SuggestionView(View):

    def get(self, request, item_id):
        suggestionsob = Suggestion.objects.filter(id=item_id)
        userob = Libuser.objects.filter(username=request.user.username)
        return render(request, 'libapp/suggestionsdet.html', {'suggestionob': suggestionsob, 'userob': userob})


@login_required
def myacct(request):
    userob1 = Libuser.objects.filter(username=request.user.username)
    if request.method == 'POST':
        userob = Libuser.objects.get(id=request.user.id)
        form = MyAcct(request.POST or None, request.FILES or None, instance=userob)
        if form.is_valid():
            form.save()
            userob = Libuser.objects.get(id=request.user.id)
            form = MyAcct(instance=userob)
            return render(request, 'libapp/myacct.html', {"form": form, "added": True, 'userob': userob1})
        else:
            userob = Libuser.objects.get(id=request.user.id)
            form = MyAcct(instance=userob)
            return render(request, 'libapp/myacct.html', {"form": form, 'userob': userob1, 'failed': True})
    else:
        userob = Libuser.objects.get(id=request.user.id)
        form = MyAcct(instance=userob)
        return render(request, 'libapp/myacct.html', {"form": form, 'userob': userob1})


def register(request):
    if request.method == 'POST':
        form = Register(request.POST, request.FILES)
        if form.is_valid():
            user = Libuser.objects.create(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                province=form.cleaned_data['province'],
                phone=form.cleaned_data['phone']
            )
            password = form.cleaned_data['password']
            user.profilepic = form.cleaned_data['profilepic']
            user.set_password(password)
            user.save()
            form = Register()
            return render(request, 'libapp/register.html', {'form': form, 'added': True})
        else:
            form = Register()
            return render(request, 'libapp/register.html', {'form': form, 'failed': True})
    else:
        form = Register()
        return render(request, 'libapp/register.html', {'form': form})


def myitems(request):
    userob = Libuser.objects.filter(username=request.user.username)
    itemob = Libitem.objects.filter(user__username=request.user.username, checked_out=True)
    return render(request, 'libapp/myitem.html', {'itemob': itemob, 'userob': userob})


def forgotpwd(request):
    if request.method == 'POST':
        username = request.POST['username']
        userob = Libuser.objects.get(username=username)
        password = str(os.urandom(4))
        userob.set_password(password)
        userob.save()
        send_mail(
            'LibApp Password',
            'Your new Password is:' + password,
            'sojitradhawal@gmail.com',
            [userob.email],
        )
        return render(request, 'libapp/forgotpwd.html', {'emailSent': True})
    else:
        return render(request, 'libapp/forgotpwd.html')


@csrf_protect
def checkuname(request):
    from app.models import Libuser
    from django.http import HttpResponse
    username = request.POST.get('username', False)
    if username:
        userob = Libuser.objects.filter(username=username).count()
        if userob:
            responce = True
        else:
            responce = False
    else:
        responce = ""

    return HttpResponse(responce)


def setpwd(request):
    userob = Libuser.objects.filter(username=request.user.username)
    if request.method == 'POST':
        userob = Libuser.objects.get(username=request.user.username)
        password = request.POST.get('npassword', 0)
        userob.set_password(password)
        userob.save()
        return render(request, 'libapp/setpwd.html', {'changed': True, 'userob': userob})
    else:
        return render(request, 'libapp/setpwd.html', {'userob': userob})
