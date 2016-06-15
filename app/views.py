from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from app.forms import SuggestionForm, SearchlibForm
from app.models import Book, Dvd, Libuser, Libitem, Suggestion


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
            return HttpResponseRedirect(reverse('app:suggestions'))
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
        SearchlibForm(request.POST)
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

        elif author1 != '' and title1 == '':    # Only Author searched
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

        else:   # Author and Title null
            form = SearchlibForm()
            return render(request, 'libapp/searchitem.html', {'notinput': True, 'form': form})

    else:
        form = SearchlibForm()
        return render(request, 'libapp/searchitem.html', {'form': form})


def suggestionsdet(request, item_id):
    suggestionsob = Suggestion.objects.filter(id=item_id)
    return render(request, 'libapp/suggestionsdet.html', {'suggestionob': suggestionsob})
