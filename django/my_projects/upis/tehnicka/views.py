from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect

from tehnicka.models import Ucenik, Smjer, Predmet, Diploma
from django.contrib.auth import authenticate, login, logout

from tehnicka.forms import UcenikEditForm
from django.urls import reverse
# INDEX: This view should show all students with corresponding classes and grades
def index(request):
    context={
    'ucenici':Ucenik.objects.all(),
    'smjerovi':Smjer.objects.all()
    }
    if request.user.is_authenticated:
        return render(request, 'tehnicka/index.html',context)
    else:
        return render(request, "users/login.html", {"message": "Please log in."})

# ADD STUDENT: This view should add new student (optional with data from form
def dodajucenika(request):
        if request.method == "POST":
            try:
                ime=request.POST["ime"]
                prezime=(request.POST["prezime"])
                smjer_id=(request.POST["smjer"])
                smjer=Smjer.objects.get(id=smjer_id)
                razred5_per_predmet=request.POST.getlist('razred5')
                razred6_per_predmet=request.POST.getlist('razred6')
                razred7_per_predmet=request.POST.getlist('razred7')
                razred8_per_predmet=request.POST.getlist('razred8')
                razred9_per_predmet=request.POST.getlist('razred9')

                # Handle empty IntegerField
                try:
                   jmbg=int(request.POST["jmbg"])
                except ValueError:
                   jmbg = None

                # Pod pretpostavkom da smo ispravno sve validirali
                # mozemo unijeti ucenika
                ucenik= Ucenik(ime=ime, prezime=prezime, smjer=smjer,JMBG=jmbg)
                ucenik.save()
                if Ucenik.objects.count()!=0:
                    ucenik_id= Ucenik.objects.latest('id').id
                else:
                    ucenik_id=1

                # Pod pretpostavkom da smo validno unijeli sve ocjene za sve predmete
                # mozemo ispuniti diplomu
                razred5=Diploma(razred_id=5, razred_naziv="Peti razred") # razred.razred_id = 5 (Diploma)
                razred6=Diploma(razred_id=6, razred_naziv="Šesti razred") # razred.razred_id = 6 (Diploma)
                razred7=Diploma(razred_id=7, razred_naziv="Sedmi razred") # razred.razred_id = 7 (Diploma)
                razred8=Diploma(razred_id=8, razred_naziv="Osmi razred") # razred.razred_id = 8 (Diploma)
                razred9=Diploma(razred_id=9, razred_naziv="Deveti razred") # razred.razred_id = 9 (Diploma)
                #if not razred9_per_predmet:

                razred5.save()
                razred6.save()
                razred7.save()
                razred8.save()
                razred9.save()

                razred5.ucenik_id=ucenik_id
                razred6.ucenik_id=ucenik_id
                razred7.ucenik_id=ucenik_id
                razred8.ucenik_id=ucenik_id
                razred9.ucenik_id=ucenik_id

                svi_predmeti=Predmet.objects.all()
                lista_predmeta=list(svi_predmeti)

                razred5.predmeti.add(*lista_predmeta)
                razred6.predmeti.add(*lista_predmeta)
                razred7.predmeti.add(*lista_predmeta)
                razred8.predmeti.add(*lista_predmeta)
                razred9.predmeti.add(*lista_predmeta)

                predmeti_razreda5=razred5.predmeti.all()
                predmeti_razreda6=razred5.predmeti.all()
                predmeti_razreda7=razred5.predmeti.all()
                predmeti_razreda8=razred5.predmeti.all()
                predmeti_razreda9=razred5.predmeti.all()

                # Spasi ocjena za predmete razreda 5
                i=0
                for predmet in predmeti_razreda5:
                        predmet.ocjena=razred5_per_predmet[i]
                        predmet.save()
                        i=i+1
                razred5.save()
                # Spasi ocjena za predmete razreda 6
                i=0
                for predmet in predmeti_razreda6:
                        predmet.ocjena=razred6_per_predmet[i]
                        predmet.save()
                        i=i+1
                razred6.save()
                # Spasi ocjena za predmete razreda 7
                i=0
                for predmet in predmeti_razreda7:
                        predmet.ocjena=razred7_per_predmet[i]
                        predmet.save()
                        i=i+1
                razred7.save()
                # Spasi ocjena za predmete razreda 8
                i=0
                for predmet in predmeti_razreda8:
                        predmet.ocjena=razred8_per_predmet[i]
                        predmet.save()
                        i=i+1
                razred8.save()
                # Spasi ocjena za predmete razreda 9
                i=0
                for predmet in predmeti_razreda9:
                        predmet.ocjena=razred9_per_predmet[i]
                        predmet.save()
                        i=i+1
                razred9.save()

                # Vrati se na home page
                return HttpResponseRedirect(reverse('tehnicka:index'))
            except KeyError:
                # Prints the error and the line that causes the error
                #import sys
                #print ("%s - %s at line: %s" % (sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno))
                return HttpResponse("Key error")
        else: # GET request
            context={
            'smjerovi': Smjer.objects.all(),
            'predmeti': Predmet.objects.all(),
            }
            return render(request, 'tehnicka/dodajucenika.html', context)


def details(request, ucenik_id):
    if request.method == "POST":
        form = UcenikEditForm(request.POST, instance=Ucenik.objects.get(id=ucenik_id))
        if form.is_valid():
            form.save()
            context={
            'ucenik':Ucenik.objects.get(id=ucenik_id),
            #'smjer':Ucenik.objects.get(id=ucenik_id).smjer., #Ucenik.smjer.get_queryset()
            #'predmeti': Ocjena.predmet_id.get_queryset(),
            #'ocjene':Ocjena.objects.filter(ucenik_id=Ucenik.objects.get(id=ucenik_id)),
            'message':'Niste unijeli podatke. Unesite ponovo.',
            }
            return render(request, 'tehnicka/details.html',context)
    else:
        diplome=Diploma.objects.filter(ucenik_id=ucenik_id);
        razred5=diplome[0]
        razred6=diplome[1]
        razred7=diplome[2]
        razred8=diplome[3]
        razred9=diplome[4]

        context={
        'ucenik':Ucenik.objects.get(id=ucenik_id),
        'diplome':diplome,
        'smjerovi':Smjer.objects.all(),
        }
        #if request.user.is_authenticated:
        return render(request, 'tehnicka/details.html',context)
        #else:
        #    return render(request, "users/login.html", {"message": "Please log in."})

'''
def editucenika(request, ucenik_id):
    if request.method == "POST":
        form = UcenikEditForm(request.POST, instance=request.Ucenik)
        name=request.POST.copy().get('ime')
        #return HttpResponse(name)
        if form.is_valid():
            form.save()
            context={
            'ucenik':Ucenik.objects.get(id=ucenik_id),
            #'smjer':Ucenik.objects.get(id=ucenik_id).smjer., #Ucenik.smjer.get_queryset()
            #'predmeti': Ocjena.predmet_id.get_queryset(),
            #'ocjene':Ocjena.objects.filter(ucenik_id=Ucenik.objects.get(id=ucenik_id)),
            #'message':'Ucenik editovan',
            }
            #if request.user.is_authenticated:
            return HttpResponse("Uasdfas")
            #return render(request, 'tehnicka/details.html',context)
        else:
            messages.error(request, form.errors)
            # return form with entered data, display messages at the top
    else:
        #return HttpResponse("get")
        form = UcenikEditForm(instance=Ucenik.objects.get(id=ucenik_id))
        context={
        'form':form,
        'ucenik_id':ucenik_id
        }
        return render(request, 'tehnicka/editucenika2.html', context)

        '''
