from random import randint

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core import serializers
from app.forms import SuggestionForm, SearchlibForm, LoginForm, Register
from app.models import Book, Dvd, Libuser, Libitem, Suggestion


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
            return HttpResponseRedirect('/app/index/')
        elif user is None:
            return render(request, 'libapp/login.html', {'notlogin': True, 'form': form})
        else:
            return render(request, 'libapp/login.html', {'notactive': True, 'form': form})
    else:
        return render(request, 'libapp/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def index(request):
    luckynum = request.session.get('luckynum', 0)
    itemlist = Libitem.objects.all().order_by('title')[:10]
    if luckynum:
        if request.user.username:
            libuserob = Libuser.objects.get(username=request.user.username)
            itemlistper = Libitem.objects.filter(user_id__exact=request.user.id)
            return render(request, "libapp/index.html",
                          {'itemlist': itemlist, 'itemlistper': itemlistper, 'luckynum': luckynum,
                           'libuserob': libuserob})
    else:
        return render(request, "libapp/index.html",
                      {'itemlist': itemlist, 'luckynum': luckynum})


def about(request):
    about_visits = request.session.get('about_visits', True)
    if about_visits:
        about_visits += 1
        request.session['about_visits'] = about_visits
        request.session.set_expiry(300)
        return render(request, 'libapp/about.html', {'about_visits': about_visits})
    else:
        return render(request, 'libapp/about.html', {'about_visits': about_visits})


def detail(request, item_id):
    libitem = get_object_or_404(Libitem, id=item_id)
    if libitem.itemtype == 'Book':
        book = get_list_or_404(Book, id=item_id)
        return render(request, 'libapp/detail.html', {'book': book})
    else:
        dvd = get_list_or_404(Dvd, id=item_id)
        return render(request, 'libapp/detail.html', {'dvd': dvd})


def register(request):
    form = Register()
    return render(request, 'libapp/register.html', {'form': form})


def suggestions(request):
    suggestionlist = Suggestion.objects.all()[:10]
    return render(request, 'libapp/suggestions.html', {'itemlist': suggestionlist})


def newitem(request):
    suggestionsob = Suggestion.objects.all()
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.num_interested = 1
            suggestion.save()
            return HttpResponseRedirect('/app/suggestions/')
        else:
            return render(request, 'libapp/newitem.html', {'form': form, 'suggestions': suggestionsob})

    else:
        form = SuggestionForm()
        return render(request, 'libapp/newitem.html', {'form': form, 'suggestions': suggestionsob})


def searchitem(request):
    if request.method == 'POST':
        title1 = request.POST['title']
        author1 = request.POST['author']
        if title1 != '' and author1 != '':  # Title and User not null
            bookob = Book.objects.filter(title__contains=title1, author__contains=author1)
            dvdob = Dvd.objects.filter(title__contains=title1, maker__contains=author1)
            form = SearchlibForm()
            if bookob and dvdob:
                return render(request, 'libapp/searchitem.html', {'bookob': bookob, 'dvdob': dvdob, 'form': form})
            elif not bookob and dvdob:
                return render(request, 'libapp/searchitem.html', {'dvdob': dvdob, 'form': form})
            elif bookob and not dvdob:
                return render(request, 'libapp/searchitem.html', {'bookob': bookob, 'form': form})
            else:
                return render(request, 'libapp/searchitem.html', {'notfound': True, 'form': form})

        elif title1 != '' and author1 == '':  # Only Title searched
            bookob = Book.objects.filter(title__contains=title1)
            dvdob = Dvd.objects.filter(title__contains=title1)
            form = SearchlibForm()
            if bookob and dvdob:
                return render(request, 'libapp/searchitem.html', {'bookob': bookob, 'dvdob': dvdob, 'form': form})
            elif bookob and not dvdob:
                return render(request, 'libapp/searchitem.html', {'bookob': bookob, 'form': form})
            elif not bookob and dvdob:
                return render(request, 'libapp/searchitem.html', {'dvdob': dvdob, 'form': form})
            else:
                return render(request, 'libapp/searchitem.html', {'notfound': True, 'form': form})

        elif author1 != '' and title1 == '':  # Only Author searched
            bookob = Book.objects.filter(author__contains=author1)
            dvdob = Dvd.objects.filter(maker__contains=author1)
            form = SearchlibForm()
            if bookob and dvdob:
                return render(request, 'libapp/searchitem.html', {'bookob': bookob, 'dvdob': dvdob, 'form': form})
            elif bookob and not dvdob:
                return render(request, 'libapp/searchitem.html', {'bookob': bookob, 'form': form})
            elif not dvdob and bookob:
                return render(request, 'libapp/searchitem.html', {'dvdob': dvdob, 'form': form})
            else:
                form = SearchlibForm()
                return render(request, 'libapp/searchitem.html', {'notfound': True, 'form': form})

        else:  # Author and Title null
            form = SearchlibForm()
            return render(request, 'libapp/searchitem.html', {'notinput': True, 'form': form})

    else:
        form = SearchlibForm()
        return render(request, 'libapp/searchitem.html', {'form': form})


def suggestionsdet(request, item_id):
    suggestionsob = Suggestion.objects.filter(id=item_id)
    return render(request, 'libapp/suggestionsdet.html', {'suggestionob': suggestionsob})


@login_required
def myacct(request):
    userob = Libuser.objects.get(id=request.user.id)
    d = {'first_name': userob.first_name, 'last_name': userob.last_name, 'emailid': userob.email,
         'address': userob.address, 'city': userob.city, 'province': userob.province, 'phone': userob.phone,
         'imageloc': userob.profilepic}
    if request.method == 'POST':
        input_file = request.FILES.get('imageloc', 0)
        if input_file:
            new_file = open('E:/University of Windsor/Inter 2016/Python/Labs/Lab2Django/app/static/ProfilePics/' + str(input_file), "w+")
            new_file.write(input_file.read())
            imageloc = 'app/static/ProfilePics/' + str(input_file)
            userob = Libuser.objects.filter(id=request.user.id).update(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['emailid'],
                address=request.POST['address'],
                city=request.POST['city'],
                province=request.POST['province'],
                phone=request.POST['phone'],
                profilepic=imageloc,
            )
        else:
            userob = Libuser.objects.filter(id=request.user.id).update(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['emailid'],
                address=request.POST['address'],
                city=request.POST['city'],
                province=request.POST['province'],
                phone=request.POST['phone'],
            )
        userob = Libuser.objects.get(id=request.user.id)
        d = {'first_name': userob.first_name, 'last_name': userob.last_name, 'emailid': userob.email,
             'address': userob.address, 'city': userob.city, 'privince': userob.province, 'phone': userob.phone,
             'imageloc': userob.profilepic}
        d1 = 'True'
        return render(request, 'libapp/myacct.html', {"values": d, "record_added": d1})
    else:
        return render(request, 'libapp/myacct.html', {"values": d})


def myitems(request):
    itemob = Libitem.objects.filter(user__username=request.user.username, checked_out=True)
    return render(request, 'libapp/myitem.html', {'itemob': itemob})
