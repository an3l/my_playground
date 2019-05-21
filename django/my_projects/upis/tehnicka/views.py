from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect

from tehnicka.models import Ucenik, Smjer, Predmet, Diploma, PredmetIspis
from django.contrib.auth import authenticate, login, logout

from tehnicka.forms import UcenikEditForm
from django.urls import reverse

from django.db import transaction

#### ---------------- INDEX VIEW  ---------------- ####
# INDEX: This view should show all students with corresponding classes and grades
def index(request):
    message=''
    if request.session.get('message'):
        message='Deleted user'
        del request.session['message']
    context={
    'ucenici':Ucenik.objects.all(),
    'smjerovi':Smjer.objects.all(),
    'message':message
    }
    if request.user.is_authenticated:
        return render(request, 'tehnicka/index.html',context)
    else:
        return render(request, "users/login.html", {"message": "Please log in."})

#### ---------------- ADD VIEW  ---------------- ####
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

                transaction.set_autocommit(False)
                try:
                    # Pod pretpostavkom da smo ispravno sve validirali
                    # mozemo unijeti ucenika
                    ucenik= Ucenik(ime=ime, prezime=prezime, smjer=smjer,JMBG=jmbg)
                    ucenik.save()
                    if Ucenik.objects.count()==0:
                        ucenik_id=1

                    # Pod pretpostavkom da smo validno unijeli sve ocjene za sve predmete
                    # mozemo ispuniti diplomu
                    razred5=Diploma(razred_id=5, razred_naziv="Peti razred",ucenik_id=ucenik) # razred.razred_id = 5 (Diploma)
                    razred6=Diploma(razred_id=6, razred_naziv="Šesti razred",ucenik_id=ucenik) # razred.razred_id = 6 (Diploma)
                    razred7=Diploma(razred_id=7, razred_naziv="Sedmi razred",ucenik_id=ucenik) # razred.razred_id = 7 (Diploma)
                    razred8=Diploma(razred_id=8, razred_naziv="Osmi razred",ucenik_id=ucenik) # razred.razred_id = 8 (Diploma)
                    razred9=Diploma(razred_id=9, razred_naziv="Deveti razred",ucenik_id=ucenik) # razred.razred_id = 9 (Diploma)
                    #if not razred9_per_predmet:

                    razred5.save()
                    razred6.save()
                    razred7.save()
                    razred8.save()
                    razred9.save()
                    # save all predmets in dictionary no need for hardcodin
                    #d={'MM': 'Matematika', 'BJ':'Bosanski jezik i književnost',
                    #  'IN':'Informatika'}
                    d={}
                    # Duplira predmet ne moze ovako
                    for predmet in PredmetIspis.objects.all():
                           d[predmet.kod]=predmet.naziv

                    #svi_predmeti=Predmet.objects.all() # ovo ne moze, kupi zadnje ocjene
                    lista_predmeta_5 = Predmet.objects.bulk_create([Predmet(kod=key, naziv=d[key]) for key in d]) # already list
                    lista_predmeta_6 = Predmet.objects.bulk_create([Predmet(kod=key, naziv=d[key]) for key in d]) # already list
                    lista_predmeta_7 = Predmet.objects.bulk_create([Predmet(kod=key, naziv=d[key]) for key in d]) # already list
                    lista_predmeta_8 = Predmet.objects.bulk_create([Predmet(kod=key, naziv=d[key]) for key in d]) # already list
                    lista_predmeta_9 = Predmet.objects.bulk_create([Predmet(kod=key, naziv=d[key]) for key in d]) # already list
    
                    for predmet in lista_predmeta_5:
                        predmet.save()

                    for predmet in lista_predmeta_6:
                        predmet.save()

                    for predmet in lista_predmeta_7:
                        predmet.save()

                    for predmet in lista_predmeta_8:
                        predmet.save()

                    for predmet in lista_predmeta_9:
                        predmet.save()
                    #lista_predmeta=list(svi_predmeti) # not needed to convert (needed for objects.all() query_set)

                    razred5.predmeti.add(*lista_predmeta_5)
                    razred6.predmeti.add(*lista_predmeta_6)
                    razred7.predmeti.add(*lista_predmeta_7)
                    razred8.predmeti.add(*lista_predmeta_8)
                    razred9.predmeti.add(*lista_predmeta_9)

                    predmeti_razreda5=razred5.predmeti.all()
                    predmeti_razreda6=razred6.predmeti.all()
                    predmeti_razreda7=razred7.predmeti.all()
                    predmeti_razreda8=razred8.predmeti.all()
                    predmeti_razreda9=razred9.predmeti.all()

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

                except:
                    transaction.rollback()
                    raise
                else:
                    transaction.commit()
                finally:
                    transaction.set_autocommit(True)

            except KeyError:
                # Prints the error and the line that causes the error
                #import sys
                #print ("%s - %s at line: %s" % (sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno))
                return HttpResponse("Key error")
        else: # GET request
            context={
            'smjerovi': Smjer.objects.all(),
            'predmeti_header': PredmetIspis.objects.all(),
            }
            return render(request, 'tehnicka/dodajucenika.html', context)

#### ---------------- EDIT/DETAILS VIEW  ---------------- ####
def details(request, ucenik_id):
    if request.method == "POST":
        try:
            ime=request.POST["ime"]
            prezime=(request.POST["prezime"])
            smjer_id=(request.POST["smjer"])
            smjer=Smjer.objects.get(id=smjer_id)
            razredi_ocjene=request.POST.getlist('razredi_ocjene')
            #return HttpResponse(razredi_ocjene)
            ucenik=Ucenik.objects.get(id=ucenik_id)
            diplome_qs=Diploma.objects.filter(ucenik_id=ucenik_id) # query_set -> not working
            diplome_list=list(diplome_qs) #list -> not working
            i=0
            for razred in diplome_qs: # or diplome_qs not working
                predmeti_list= (razred.predmeti.all()) # predmeti is a list -> not working, also query_set
                for predmet in predmeti_list: #Predmet query_set
                    predmet.ocjena=razredi_ocjene[i]
                    i=i+1
                    predmet.save()
                razred.save()

            return HttpResponseRedirect(reverse('tehnicka:index'))
        except KeyError:
            return HttpResponse("Key error - post uredi")

    else:
        ucenik=Ucenik.objects.get(id=ucenik_id)
        diplome=Diploma.objects.filter(ucenik_id=ucenik);
        context={
        'ucenik':ucenik,
        'diplome':diplome,
        'smjerovi':Smjer.objects.all(),
        }
        #if request.user.is_authenticated:
        return render(request, 'tehnicka/details.html',context)
        #else:
        #    return render(request, "users/login.html", {"message": "Please log in."})

#### ---------------- DELETE VIEW  ---------------- ####
def delete(request, ucenik_id):
    ucenik=Ucenik.objects.filter(id=ucenik_id).delete()
    request.session['message']="Deleted user"
    return HttpResponseRedirect(reverse('tehnicka:index'))
