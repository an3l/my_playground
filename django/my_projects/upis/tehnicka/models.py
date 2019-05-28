from django.db import models

# Create your models here.
class Smjer(models.Model):
    # blank odnosi se na formu (false nije dozvoljeno ostaviti prazno polje)
    kod=models.CharField(max_length=3, default='AUT', blank=False)
    naziv=models.CharField(max_length=64)
    class Meta:
        verbose_name_plural = "smjerovi"
    def __str__(self):
        return f"id:{self.id}:{self.kod}-{self.naziv}"


class Ucenik(models.Model):
    ime=models.CharField(max_length=50)
    prezime=models.CharField(max_length=50)
    # JMBG=models.IntegerField(null=True, blank=False)
    osnovna_skola=models.CharField(max_length=50)
    smjer=models.ForeignKey(Smjer, on_delete=models.CASCADE)
    # Ukoliko ne bismo trazili listanje po smjerovima
    #smjer=model.CharField(max_length=3,choices=smjerovi, default=automaticar)
    # opcionalno bi trebalo napraviti izbor za 3 smjera (manytomany)

    #DEFAULT_DIPLOMA_ID=0 # will fail foreign key constraint
    #diploma_id=models.ForeignKey(Diploma,on_delete=models.CASCADE)
    #onetoonefield same as foreignkey and unique=True
    #diploma=models.OneToOneField(Diploma, on_delete=models.CASCADE)
    elektronicar = 'ELE'
    automaticar = 'AUT'
    arhitekt = 'ARH'
    masinac = 'MAS'
    metalurg='MET'
    smjerovi = (
    (elektronicar, 'Tehničar elektronike'),
    (automaticar, 'Tehničar računarske tehnike i automatike'),
    (arhitekt, 'Arhitektonski tehničar'),
    (masinac, 'Mašinski tehničar'),
    (metalurg, 'Metalurški tehničar'),
    )
    class Meta:
        verbose_name_plural = "Učenici"
    def __str__(self):
        return f"id:{self.id}:{self.ime}-{self.prezime}"

# class Takmicenje(models.Model):
#     kod=models.CharField(max_length=64)
#     naziv=models.CharField(max_length=64)
#     class Meta:
#         verbose_name_plural = "Takmicenja"
#     def __str__(self):
#         return f"{self.kod}-{self.naziv}"

class Priznanja(models.Model):
    naziv=models.CharField(max_length=64)
    bodovi=models.IntegerField(default='0')
    ucenik_id=models.ForeignKey(Ucenik, on_delete=models.CASCADE)
    # vrsta_takmicenja=models.ForeignKey(Takmicenje, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Priznanja"
    def __str__(self):
        return f"id:{self.id}:{self.naziv}-{self.bodovi}"

class PredmetIspis(models.Model):
    kod=models.CharField(max_length=2, default='MM', blank=False)
    naziv=models.CharField(max_length=64)
    razred_id=models.IntegerField(default='5')
    class Meta:
        verbose_name_plural = "Predmeti_ispis"
    def __str__(self):
        return f"{self.razred_id}:{self.naziv}-{self.kod}"

class Predmet(models.Model):
    kod=models.CharField(max_length=2, default='MM', blank=False)
    naziv=models.CharField(max_length=64)
    ocjena=models.IntegerField(null=True, blank=True)
    # diploma_id=models.ForeignKey(Diploma,on_delete=models.CASCADE) not defined
    class Meta:
        verbose_name = 'Predmet'
        verbose_name_plural = 'Predmeti'
    def __str__(self):
        return f"id:{self.id} {self.kod}-{self.naziv}"
'''
    def save(self, *args, **kwargs):
     if not self.ocjena:
          self.ocjena = None
     super(Predmet, self).save(*args, **kwargs)
'''
class Diploma(models.Model):
    razred_id=models.IntegerField(null=False, blank=False)
    razred_naziv=models.CharField(max_length=64)
    predmeti=models.ManyToManyField(Predmet)
    ucenik_id=models.ForeignKey(Ucenik, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Diplome"
    def __str__(self):
        return f"id:{self.id} {self.razred_naziv}"
