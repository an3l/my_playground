from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect

from tehnicka.models import Ucenik, Smjer, Predmet, Diploma, PredmetIspis, Priznanja
from django.contrib.auth import authenticate, login, logout

from django.urls import reverse

from django.db import transaction
import json
#### ---------------- INDEX VIEW  ---------------- ####
# INDEX: This view should show all students with corresponding classes and grades
def index(request):
    message=''
    if request.session.get('message'):
        message='Korisnik obrisan!'
        del request.session['message']

    posebni_bodovi={}
    prosjek_6={}
    prosjek_7={}
    prosjek_8={}
    prosjek_9={}

    prosjek_ukupno=0
    posebni_predmet_ukupno=0
    posebni_predmet_1_ocjena_razred9=0
    posebni_predmet_2_ocjena_razred9=0
    posebni_predmet_3_ocjena_razred7=0
    UKUPNO=0
    posebni_predmet_1_ocjena_razred8=posebni_predmet_1_ocjena_razred9
    posebni_predmet_2_ocjena_razred8=posebni_predmet_2_ocjena_razred9
    posebni_predmet_3_ocjena_razred6=posebni_predmet_3_ocjena_razred7

    posebni_predmet_1=""
    posebni_predmet_2=posebni_predmet_1
    posebni_predmet_3=posebni_predmet_1

    # Dictionaries
    posebni_predmet_1_ocjena_razred8_dict={}
    posebni_predmet_1_ocjena_razred9_dict={}
    posebni_predmet_2_ocjena_razred8_dict={}
    posebni_predmet_2_ocjena_razred9_dict={}
    posebni_predmet_3_ocjena_razred6_dict={}
    posebni_predmet_3_ocjena_razred7_dict={}
    prosjek_ukupno_dict={}

    prosjek_6_dict={}
    prosjek_7_dict={}
    prosjek_8_dict={}
    prosjek_9_dict={}
    posebni_bodovi_dict={}
    ukupno_dict={}

    # Pokupi bodove sa priznanja
    priznanje_opcinsko_dict={} # @todo
    priznanje_kantonalno_dict={}
    priznanje_federalno_dict={}

# =============== Racunanje statistike ===============
    for ucenik in Ucenik.objects.all():
        s=0 # prosjek po razredu laznjak -> brisi

        for razred in Diploma.objects.filter(ucenik_id=ucenik):
            p=0 # broj predmeta
            s1=0 # prosjek po razredu
            for predmet in razred.predmeti.all():
                p=p+1
                s1=s1+predmet.ocjena
                # Handling posebni_bodovi na predmete automatika/arhitekture/energetike
                if(ucenik.smjer.kod == 'AUT' or ucenik.smjer.kod == 'ARH' or ucenik.smjer.kod == 'EN'):
                    posebni_predmet_1="Matematika"
                    posebni_predmet_2="Fizika"
                    posebni_predmet_3="Informatika"
                    # RACUNAJ UKUPNE BODOVE NA POSEBNE PREDMETE
                    if razred.razred_id==8 or razred.razred_id==9:
                        if predmet.kod=='MM' or predmet.kod=='FI':
                            s=s+predmet.ocjena

                    if razred.razred_id==6 or razred.razred_id==7:
                        if predmet.kod=='IN':
                            s=s+predmet.ocjena

                    # RACUNAJ POJEDINACNE BODOVE NA POSEBNE PREDMETE
                    if predmet.kod=='MM' and razred.razred_id==8:
                        posebni_predmet_1_ocjena_razred8=predmet.ocjena
                    elif predmet.kod=='MM' and razred.razred_id==9:
                        posebni_predmet_1_ocjena_razred9=predmet.ocjena
                    elif predmet.kod=='FI' and razred.razred_id==8:
                        posebni_predmet_2_ocjena_razred8=predmet.ocjena
                    elif predmet.kod=='FI' and razred.razred_id==9:
                        posebni_predmet_2_ocjena_razred9=predmet.ocjena
                    elif predmet.kod=='IN' and razred.razred_id==6:
                        posebni_predmet_3_ocjena_razred6=predmet.ocjena
                    elif predmet.kod=='IN' and razred.razred_id==7:
                        posebni_predmet_3_ocjena_razred7=predmet.ocjena

                # Handling posebni_bodovi na predmete masinci/metalurzi
                if(ucenik.smjer.kod == 'MAS' or ucenik.smjer.kod == 'ME'):
                    posebni_predmet_1="Matematika"
                    posebni_predmet_2="Fizika"
                    posebni_predmet_3="Tehnička kultura"
                    # RACUNAJ UKUPNE BODOVE NA POSEBNE PREDMETE
                    if razred.razred_id==8 or razred.razred_id==9:
                        if predmet.kod=='MM' or predmet.kod=='FI':
                            s=s+predmet.ocjena
                    if razred.razred_id==6 or razred.razred_id==7:
                        if predmet.kod=='TK':
                            s=s+predmet.ocjena

                    # RACUNAJ POJEDINACNE BODOVE NA POSEBNE PREDMETE
                    if predmet.kod=='MM' and razred.razred_id==8:
                        posebni_predmet_1_ocjena_razred8=predmet.ocjena
                    elif predmet.kod=='MM' and razred.razred_id==9:
                        posebni_predmet_1_ocjena_razred9=predmet.ocjena
                    elif predmet.kod=='FI' and razred.razred_id==8:
                        posebni_predmet_2_ocjena_razred8=predmet.ocjena
                    elif predmet.kod=='FI' and razred.razred_id==9:
                        posebni_predmet_2_ocjena_razred9=predmet.ocjena
                    elif predmet.kod=='TK' and razred.razred_id==6:
                        posebni_predmet_3_ocjena_razred6=predmet.ocjena
                    elif predmet.kod=='TK' and razred.razred_id==7:
                        posebni_predmet_3_ocjena_razred7=predmet.ocjena


                # Handling posebni_bodovi na predmete tehnicar drumskog saobracaja
                if(ucenik.smjer.kod == 'TDS'):
                    posebni_predmet_1="Matematika"
                    posebni_predmet_2="Fizika"
                    posebni_predmet_3="Geografija"
                    # RACUNAJ UKUPNE BODOVE NA POSEBNE PREDMETE
                    if razred.razred_id==8 or razred.razred_id==9:
                        if predmet.kod=='MM' or predmet.kod=='FI':
                            s=s+predmet.ocjena
                    if razred.razred_id==6 or razred.razred_id==7:
                        if predmet.kod=='GE':
                            s=s+predmet.ocjena

                    # RACUNAJ POJEDINACNE BODOVE NA POSEBNE PREDMETE
                    if predmet.kod=='MM' and razred.razred_id==8:
                        posebni_predmet_1_ocjena_razred8=predmet.ocjena
                    elif predmet.kod=='MM' and razred.razred_id==9:
                        posebni_predmet_1_ocjena_razred9=predmet.ocjena
                    elif predmet.kod=='FI' and razred.razred_id==8:
                        posebni_predmet_2_ocjena_razred8=predmet.ocjena
                    elif predmet.kod=='FI' and razred.razred_id==9:
                        posebni_predmet_2_ocjena_razred9=predmet.ocjena
                    elif predmet.kod=='GE' and razred.razred_id==6:
                        posebni_predmet_3_ocjena_razred6=predmet.ocjena
                    elif predmet.kod=='GE' and razred.razred_id==7:
                        posebni_predmet_3_ocjena_razred7=predmet.ocjena


            # Racunaj prosjek po razredima za svakog ucenika
            if(razred.razred_id==6):
                prosjek_6=round(s1/p,2) # round(x,2) float("{0:.2f}".format(x))

            if(razred.razred_id==7):
                prosjek_7=round(s1/p,2)
            if(razred.razred_id==8):
                prosjek_8=round(s1/p,2)
            if(razred.razred_id==9):
                prosjek_9=round(s1/p,2)

        # Pokupi zakljucne ocjene na 2 decimale i ukupnu prosjecnu ocjenu
        prosjek_6_dict[ucenik.id]=prosjek_6
        prosjek_7_dict[ucenik.id]=prosjek_7
        prosjek_8_dict[ucenik.id]=prosjek_8
        prosjek_9_dict[ucenik.id]=prosjek_9
        prosjek_ukupno_dict[ucenik.id]=round((prosjek_6+prosjek_7+prosjek_8+prosjek_9)*3,2)

        # Pokupi ocjene iz posebnih predmeta i ukupnu ocjenu
        posebni_predmet_1_ocjena_razred8_dict[ucenik.id]=posebni_predmet_1_ocjena_razred8
        posebni_predmet_1_ocjena_razred9_dict[ucenik.id]=posebni_predmet_1_ocjena_razred9
        posebni_predmet_2_ocjena_razred8_dict[ucenik.id]=posebni_predmet_2_ocjena_razred8
        posebni_predmet_2_ocjena_razred9_dict[ucenik.id]=posebni_predmet_2_ocjena_razred9
        posebni_predmet_3_ocjena_razred6_dict[ucenik.id]=posebni_predmet_3_ocjena_razred6
        posebni_predmet_3_ocjena_razred7_dict[ucenik.id]=posebni_predmet_3_ocjena_razred7
        #posebni_bodovi_suma
        posebni_bodovi_dict[ucenik.id]= posebni_predmet_1_ocjena_razred8 + posebni_predmet_1_ocjena_razred9+\
        posebni_predmet_2_ocjena_razred8+posebni_predmet_2_ocjena_razred9+\
        posebni_predmet_3_ocjena_razred6+posebni_predmet_3_ocjena_razred7

        priznanja=Priznanja.objects.filter(ucenik_id=ucenik)
        if not priznanja:
            priznanje_opcinsko_dict[ucenik.id]=0
            priznanje_kantonalno_dict[ucenik.id]=0
            priznanje_federalno_dict[ucenik.id]=0
        else:
            s_o=0
            for p in priznanja:
                s_o=s_o+p.bodovi
            priznanje_opcinsko_dict[ucenik.id]=s_o # {{ key }} - {{ value.i }}<
            priznanje_kantonalno_dict[ucenik.id]=0
            priznanje_federalno_dict[ucenik.id]=0

        ukupno_dict[ucenik.id]=round(prosjek_ukupno_dict[ucenik.id]+\
        posebni_bodovi_dict[ucenik.id]+\
        priznanje_opcinsko_dict[ucenik.id]+priznanje_kantonalno_dict[ucenik.id]+\
        priznanje_federalno_dict[ucenik.id], 2)


    #return HttpResponse(json.dumps( bodovi ))

# =============== Prikazivanje statistike ===============

    context={
    'ucenici':Ucenik.objects.all(),     # 'smjerovi':Smjer.objects.all(),
    'posebni_predmet_1':posebni_predmet_1,
    'posebni_predmet_2':posebni_predmet_2,
    'posebni_predmet_3':posebni_predmet_3,

    'prosjek_6':prosjek_6_dict,
    'prosjek_7':prosjek_7_dict,
    'prosjek_8':prosjek_8_dict,
    'prosjek_9':prosjek_9_dict,

    'prosjek_ukupno':prosjek_ukupno_dict, # mnozi se sa 3

    'posebni_predmet_1_ocjena_razred8':posebni_predmet_1_ocjena_razred8_dict,
    'posebni_predmet_1_ocjena_razred9':posebni_predmet_1_ocjena_razred9_dict,
    'posebni_predmet_2_ocjena_razred8':posebni_predmet_2_ocjena_razred8_dict,
    'posebni_predmet_2_ocjena_razred9':posebni_predmet_2_ocjena_razred9_dict,
    'posebni_predmet_3_ocjena_razred6':posebni_predmet_3_ocjena_razred6_dict,
    'posebni_predmet_3_ocjena_razred7':posebni_predmet_3_ocjena_razred7_dict,

    'posebni_predmet_ukupno':posebni_bodovi_dict,

    'priznanje_opcinsko':priznanje_opcinsko_dict,
    'priznanje_kantonalno':priznanje_kantonalno_dict,
    'priznanje_federalno':priznanje_federalno_dict,

    'ukupno':ukupno_dict,

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
                osnovna_skola=(request.POST["osnovna_skola"])
                smjer_id=(request.POST["smjer"])
                smjer=Smjer.objects.get(id=smjer_id)

                razred6_per_predmet=request.POST.getlist('razred6')
                razred7_per_predmet=request.POST.getlist('razred7')
                razred8_per_predmet=request.POST.getlist('razred8')
                razred9_per_predmet=request.POST.getlist('razred9')

                priznanja_naziv=request.POST.getlist('priznanje_naziv');
                priznanje_bodovi=request.POST.getlist('priznanje_bodovi');
                # Handle empty IntegerField
                # try:
                #    jmbg=int(request.POST["jmbg"])
                # except ValueError:
                #    jmbg = None

                transaction.set_autocommit(False)
                try:
                    # Pod pretpostavkom da smo ispravno sve validirali
                    # mozemo unijeti ucenika
                    ucenik= Ucenik(ime=ime, prezime=prezime, smjer=smjer,osnovna_skola=osnovna_skola)
                    ucenik.save()

                    if priznanje_bodovi:
                        for i in range(len(priznanje_bodovi)):
                            naziv=priznanja_naziv[i]
                            bodovi=priznanje_bodovi[i]
                            priznanje=Priznanja(naziv=naziv, bodovi=bodovi, ucenik_id=ucenik)
                            priznanje.save()


                    if Ucenik.objects.count()==0:
                        ucenik_id=1

                    # Pod pretpostavkom da smo validno unijeli sve ocjene za sve predmete
                    # mozemo ispuniti diplomu
                    razred6=Diploma(razred_id=6, razred_naziv="Šesti razred",ucenik_id=ucenik) # razred.razred_id = 6 (Diploma)
                    razred7=Diploma(razred_id=7, razred_naziv="Sedmi razred",ucenik_id=ucenik) # razred.razred_id = 7 (Diploma)
                    razred8=Diploma(razred_id=8, razred_naziv="Osmi razred",ucenik_id=ucenik) # razred.razred_id = 8 (Diploma)
                    razred9=Diploma(razred_id=9, razred_naziv="Deveti razred",ucenik_id=ucenik) # razred.razred_id = 9 (Diploma)
                    #if not razred9_per_predmet:

                    razred6.save()
                    razred7.save()
                    razred8.save()
                    razred9.save()
                    # save all predmets in dictionary no need for hardcodin
                    #d={'MM': 'Matematika', 'BJ':'Bosanski jezik i književnost',
                    #  'IN':'Informatika'}
                    d={}
                    # Duplira predmet ne moze ovako
                    for predmet in PredmetIspis.objects.filter(razred_id=6):
                           d[predmet.kod]=predmet.naziv

                    #svi_predmeti=Predmet.objects.all() # ovo ne moze, kupi zadnje ocjene
                    lista_predmeta_6 = Predmet.objects.bulk_create([Predmet(kod=key, naziv=d[key]) for key in d]) # already list
                    d={}
                    # Duplira predmet ne moze ovako
                    for predmet in PredmetIspis.objects.filter(razred_id=7):
                           d[predmet.kod]=predmet.naziv
                    lista_predmeta_7 = Predmet.objects.bulk_create([Predmet(kod=key, naziv=d[key]) for key in d]) # already list
                    d={}
                    # Duplira predmet ne moze ovako
                    for predmet in PredmetIspis.objects.filter(razred_id=8):
                           d[predmet.kod]=predmet.naziv
                    lista_predmeta_8 = Predmet.objects.bulk_create([Predmet(kod=key, naziv=d[key]) for key in d]) # already list
                    d={}
                    # Duplira predmet ne moze ovako
                    for predmet in PredmetIspis.objects.filter(razred_id=9):
                           d[predmet.kod]=predmet.naziv
                    lista_predmeta_9 = Predmet.objects.bulk_create([Predmet(kod=key, naziv=d[key]) for key in d]) # already list

                    for predmet in lista_predmeta_6:
                        predmet.save()

                    for predmet in lista_predmeta_7:
                        predmet.save()

                    for predmet in lista_predmeta_8:
                        predmet.save()

                    for predmet in lista_predmeta_9:
                        predmet.save()
                    #lista_predmeta=list(svi_predmeti) # not needed to convert (needed for objects.all() query_set)

                    razred6.predmeti.add(*lista_predmeta_6)
                    razred7.predmeti.add(*lista_predmeta_7)
                    razred8.predmeti.add(*lista_predmeta_8)
                    razred9.predmeti.add(*lista_predmeta_9)

                    predmeti_razreda6=razred6.predmeti.all()
                    predmeti_razreda7=razred7.predmeti.all()
                    predmeti_razreda8=razred8.predmeti.all()
                    predmeti_razreda9=razred9.predmeti.all()

                    # Spasi ocjena za predmete razreda 6
                    i=0
                    for predmet in predmeti_razreda6:
                        if (i==8): # ovo je informatika predmet, stavi zadnji element
                            predmet.ocjena=razred6_per_predmet[len(razred6_per_predmet)-1]
                            predmet.save()
                        elif(i<8):
                            predmet.ocjena=razred6_per_predmet[i]
                            predmet.save()
                        elif(i>8):
                            predmet.ocjena=razred6_per_predmet[i-1]
                            predmet.save()
                        i=i+1
                    razred6.save()
                    # Spasi ocjena za predmete razreda 7
                    i=0
                    for predmet in predmeti_razreda7:
                        if (i==9): # ovo je informatika predmet, stavi zadnji element
                            predmet.ocjena=razred7_per_predmet[len(razred7_per_predmet)-1]
                            predmet.save()
                        elif(i<9):
                            predmet.ocjena=razred7_per_predmet[i]
                            predmet.save()
                        elif(i>9):
                            predmet.ocjena=razred7_per_predmet[i-1]
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
                return HttpResponse("Key error dodajucenika")
        else: # GET request
            inf=PredmetIspis.objects.filter(razred_id=6).filter(kod="IN"); #moramo dodati informatiku
            deveti=PredmetIspis.objects.filter(razred_id=9);
            deveti|=inf; # napravi uniju

            context={
            'smjerovi': Smjer.objects.all(),
            'predmeti_header': deveti.order_by('-razred_id'),
            }
            return render(request, 'tehnicka/dodajucenika.html', context)

#### ---------------- EDIT/DETAILS VIEW  ---------------- ####
def details(request, ucenik_id):
    if request.method == "POST":
        try:
            ime=request.POST["ime"]
            prezime=(request.POST["prezime"])
            osnovna_skola=(request.POST["osnovna_skola"])
            smjer_id=(request.POST["smjer"])
            smjer=Smjer.objects.get(id=smjer_id)

            razred6_ocjene=request.POST.getlist('razred6_ocjene')
            razred7_ocjene=request.POST.getlist('razred7_ocjene')
            razred8_ocjene=request.POST.getlist('razred8_ocjene')
            razred9_ocjene=request.POST.getlist('razred9_ocjene')

            priznanja_naziv=request.POST.getlist('priznanje_naziv')
            priznanje_bodovi=request.POST.getlist('priznanje_bodovi')
            vrsta_takmicenja=request.POST.getlist('vrsta_takmicenja')

            #return HttpResponse(razredi_ocjene)
            ucenik=Ucenik.objects.get(id=ucenik_id)
            diplome_qs=Diploma.objects.filter(ucenik_id=ucenik_id) # query_set -> not working
            #diplome_list=list(diplome_qs) #list -> not working
            i=0
            for razred in diplome_qs:
                predmeti_list= razred.predmeti.all() # predmeti is a list -> not working, also query_set
                j=0
                for predmet in predmeti_list: #Predmet query_set
                    if i==0:
                        razredi_ocjene=razred6_ocjene
                    if i==1:
                        razredi_ocjene=razred7_ocjene
                    if i==2:
                        razredi_ocjene=razred8_ocjene
                    if i==3:
                        razredi_ocjene=razred9_ocjene
                    predmet.ocjena=razredi_ocjene[j]

                    j=j+1
                    predmet.save()
                razred.save()
                i=i+1
            ucenik.ime=ime
            ucenik.prezime=prezime
            ucenik.smjer=smjer
            ucenik.osnovna_skola=osnovna_skola
            ucenik.save()
            i=0

            if priznanja_naziv:
                priznanje_ucenik=Priznanja.objects.filter(ucenik_id=ucenik)
                if not priznanje_ucenik: # Nema priznanja ime dugme add i mozemo dodati nova
                    for k in range(len(priznanje_bodovi)):
                        naziv=priznanja_naziv[k]
                        bodovi=priznanje_bodovi[k]
                        # tip=vrsta_takmicenja[k]
                        priznanje=Priznanja(naziv=naziv, bodovi=bodovi, ucenik_id=ucenik)
                        priznanje.save()

                else: # ima priznanja samo mijenjamo
                    i=0
                    for priznanje in priznanje_ucenik:
                        #for i in range(len(priznanje_bodovi)):
                        naziv=priznanja_naziv[i]
                        bodovi=priznanje_bodovi[i]
                        priznanje.naziv=naziv
                        priznanje.bodovi=bodovi
                        # priznanje.vrsta_takmicenja=tip
                        priznanje.save()
                        i=i+1

            return HttpResponseRedirect(reverse('tehnicka:index'))
        except KeyError:
            return HttpResponse("Key error - post uredi")

    else:
        ucenik=Ucenik.objects.get(id=ucenik_id)
        diplome=Diploma.objects.filter(ucenik_id=ucenik);
        sesti_predmeti=diplome[0].predmeti.all();
        sedmi_predmeti=diplome[1].predmeti.all();
        osmi_predmeti=diplome[2].predmeti.all();
        deveti_predmeti=diplome[3].predmeti.all();
        #fizika_7=diplome[1].predmeti.all()[4].ocjena
        #fizika_8=diplome[2].predmeti.all()[4].ocjena #hemija je 2/3 i 5
        context={
        'ucenik':ucenik,
        'sesti':sesti_predmeti,
        'sedmi':sedmi_predmeti,
        'osmi':osmi_predmeti,
        'deveti':deveti_predmeti,
        'smjerovi':Smjer.objects.all(),
        'priznanja':Priznanja.objects.filter(ucenik_id=ucenik)
        }
        #if request.user.is_authenticated:
        return render(request, 'tehnicka/details.html',context)
        #else:
        #    return render(request, "users/login.html", {"message": "Please log in."})

#### ---------------- DELETE VIEW  ---------------- ####
def delete(request, ucenik_id):
    ucenik=Ucenik.objects.filter(id=ucenik_id).delete()
    request.session['message']="Obrisan korisnik"
    return HttpResponseRedirect(reverse('tehnicka:index'))


def brisipriznanje(request, priznanje_id):
    if request.method == "GET":
        try:
            ucenik_id=Priznanja.objects.get(id=priznanje_id).ucenik_id.id
            #return HttpResponseRedirect(reverse('tehnicka:details'), kwargs={'ucenik_id':ucenik_id})args=(p.id)
            priznanje=Priznanja.objects.get(id=priznanje_id).delete()
            request.session['message']="Obrisano priznanje"
            return HttpResponseRedirect(reverse('tehnicka:details', args=(ucenik_id,)))

        except KeyError:
            return HttpResponse("Key error - post uredi priznanje")
