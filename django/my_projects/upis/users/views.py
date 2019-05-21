from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from tehnicka.models import Ucenik, Smjer, Predmet
from .forms import UcenikForm
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    context = {
        "user": request.user
    }
    return render(request, "users/user.html", context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("tehnicka:index"))
    else:
        return render(request, "users/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out."})

def ucenici_view(request):
    if request.method == "POST":
        try:
            ime=request.POST["ime"]
            prezime=(request.POST["prezime"])
            smjer_id=(request.POST["smjer"])
            smjer=Smjer.objects.get(id=smjer_id)
            # Handle empty IntegerField
            try:
               jmbg=int(request.POST["jmbg"])
            except ValueError:
               jmbg = None
            # Handling empty name and last name
            if not (ime and prezime):
                context={
                'smjerovi':Smjer.objects.all(),
                'predmeti': Predmet.objects.all(),
                'message':'Niste unijeli podatke. Unesite ponovo.'
                }
                if request.user.is_authenticated:
                    return render(request, 'users/dodajucenika.html',context)
                else:
                    return render(request, "users/login.html", {"message": "Please log in."})
            if not (ime.isalpha() and prezime.isalpha()):
                if request.user.is_authenticated:
                    context={
                    'smjerovi':Smjer.objects.all(),
                    'predmeti': Predmet.objects.all(),
                    'message':'Ime/prezime ne smije imate cifre. Unesite ponovo'
                    }
                    return render(request, 'users/dodajucenika.html',context)
                else:
                    return render(request, "users/login.html", {"message": "Please log in."})
            # If everything is ok save in db
            ucenik= Ucenik(ime=ime, prezime=prezime, smjer=smjer,JMBG=jmbg)
            # Handle ocjene
            #return HttpResponse(ocjene) # radi dobijem listu
            '''
            ocjene=request.POST.getlist('ocjena')
            for i in range(len(ocjene)):
                if not ocjene[i]:
                    if request.user.is_authenticated:
                        context={
                        'smjerovi':Smjer.objects.all(),
                        'predmeti': Predmet.objects.all(),
                        'message':'Niste unijeli sve ocjene.'
                        }
                        return render(request, 'users/dodajucenika.html',context)
                    else:
                        return render(request, "users/login.html", {"message": "Please log in."})
            '''
            ucenik.save()
            #return HttpResponse(ocjene)
            for i in range(len(ocjene)):
                predmet=Predmet.objects.get(id=i+1)
                # Ucenik.objects.latest('id').id
                #Ocjena(predmet_id=predmet,ucenik_id=ucenik, ocjena=ocjene[i]).save()
                ucenik.save()
            # If everything is ok save ucenik
            #ucenik.save()
        except KeyError:
            if request.user.is_authenticated:
                context={
                'smjerovi':Smjer.objects.all(),
                'predmeti': Predmet.objects.all(),
                'message':'Niste unijeli podatke. Unesite ponovo.'
                }
                return render(request, 'users/dodajucenika.html',context)
            else:
                return render(request, "users/login.html", {"message": "Please log in."})
        '''
        Testing HttpResponse
        #return  HttpResponse("{{ime}}-{{prezime}}-{{smjer}}")
        #return HttpResponse(ime+prezime+smjer)
        # from django.http import JsonResponse
        #return HttpResponse(json.dumps({"lat":ime, "lng":prezime, "smjer":smjer}), content_type="application/json")
        '''
        # Uspjesno obavljeno ->
        if request.user.is_authenticated:
            context={
            'smjerovi':Smjer.objects.all(),
            'predmeti': Predmet.objects.all(),
            'message':'Dodali ste ucenika.'
            }
            return render(request, 'users/dodajucenika.html',context)
        else:
            return render(request, "users/login.html", {"message": "Please log in."})
    else:
        # GET METHOD
        if request.user.is_authenticated:
            context={
            'smjerovi':Smjer.objects.all(),
            'predmeti': Predmet.objects.all(),
            }
            return render(request, 'users/dodajucenika.html',context)
        else:
            return render(request, "users/login.html", {"message": "Please log in."})
    '''
    # handling the forms
    if request.method == "POST":
        form = UcenikForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form1 = UcenikForm()
        form2 = DiplomaForm()
    return render(request, 'blog/dodajucenika.html', {'form': form1, 'form2':form2})
# context
    context = {
        "ucenici": Ucenik.objects.all(),
        "smjerovi":Smjer.objects.all(),
    }
    return render(request, "users/ucenici.html", context)
'''
