
# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField
from PIL import Image


class AutomobilioModelis(models.Model):
    marke = models.CharField(verbose_name="Automobilio gamintojas", max_length=50,
                             help_text="Įveskite automobilio gamintoją")
    modelis = models.CharField(verbose_name="Automobilio modelis", max_length=100,
                               help_text="Įveskite automobilio modelį")

    class Meta:
        verbose_name = "Automobilio modelis"
        verbose_name_plural = "Automobilių modeliai"

    def __str__(self):
        return f"{self.marke} {self.modelis}"


class Automobilis(models.Model):
    valstybinis_nr = models.CharField(verbose_name="Valstybinis numeris", max_length=10,
                                      help_text="Įveskite valstybinį numerį")
    automobilio_modelis = models.ForeignKey(to="AutomobilioModelis", on_delete=models.SET_NULL, null=True)
    vin_kodas = models.CharField(verbose_name="VIN kodas", max_length=50, help_text="Įveskite VIN kodą")
    klientas = models.CharField(verbose_name="Klientas", max_length=200, help_text="Įveskite klientą")
    paveikslelis = models.ImageField(verbose_name="Paveikslėlis", upload_to="paveiksleliai", null=True, blank=True)
    aprasymas = HTMLField(verbose_name="Aprašymas", null=True, blank=True)

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"

    def __str__(self):
        return f"{self.valstybinis_nr} {self.automobilio_modelis}"


class Uzsakymas(models.Model):
    data = models.DateTimeField(verbose_name="Užsakymo data", auto_now_add=True)
    automobilis = models.ForeignKey(to="Automobilis", on_delete=models.CASCADE)

    STATUSO_PASIRINKIMAI = (
        (1, "Patvirtintas"),
        (2, "Vykdomas"),
        (3, "Įvykdytas"),
        (4, "Atšauktas"),
    )

    statusas = models.IntegerField(choices=STATUSO_PASIRINKIMAI, default=1, help_text="Užsakymo statusas")
    vartotojas = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    atlikimo_terminas = models.DateField(verbose_name="Darbus atlikti iki",  null=True, blank=True,
                                              help_text="Užsakymo atlikimo terminas")

    class Meta:
        verbose_name = "Užsakymas"
        verbose_name_plural = "Užsakymai"

    def bendra_uzsakymo_suma(self):
        suma = 0
        visos_uzsakymo_eilutes = self.eilutes.all()
        for eilute in visos_uzsakymo_eilutes:
            suma += eilute.uzsakymo_eilutes_suma()
        return suma

    def terminas_suejo(self):
        return self.atlikimo_terminas and date.today() > self.atlikimo_terminas

    def __str__(self):
        return f"{self.automobilis} -- {self.data}"


class Paslauga(models.Model):
    pavadinimas = models.CharField(verbose_name="Paslaugos pavadinimas", max_length=200,
                                   help_text="Įveskite paslaugos pavadinimą")
    kaina = models.FloatField(verbose_name="Paslaugos kaina", help_text="Įveskite paslaugos kainą")

    class Meta:
        verbose_name = "Paslauga"
        verbose_name_plural = "Paslaugos"

    def __str__(self):
        return f"{self.pavadinimas}"


class UzsakymoEilute(models.Model):
    uzsakymas = models.ForeignKey(to="Uzsakymas", on_delete=models.CASCADE, related_name="eilutes")
    paslauga = models.ForeignKey(to="Paslauga", on_delete=models.SET_NULL, null=True)
    kiekis = models.IntegerField(verbose_name="Kiekis", help_text="Įveskite kiekį")

    class Meta:
        verbose_name = "Užsakymo eilutė"
        verbose_name_plural = "Užsakymo eilutės"

    def uzsakymo_eilutes_suma(self):
        return self.paslauga.kaina * self.kiekis

    def __str__(self):
        return f"{self.paslauga} ---- {self.kiekis}"


class UzsakymoAtsiliepimas(models.Model):
    uzsakymas = models.ForeignKey(to="Uzsakymas", verbose_name="Užsakymas", on_delete=models.SET_NULL, null=True,
                                  blank=True, related_name="atsiliepimai")
    komentatorius = models.ForeignKey(to=User, verbose_name="Vartotojas", on_delete=models.SET_NULL, null=True,
                                      blank=True)
    atsiliepimo_data = models.DateTimeField(verbose_name="Atsiliepimo data", auto_now_add=True)
    turinys = models.TextField(verbose_name="Atsiliepimas", max_length=3000)

    class Meta:
        verbose_name = "Užsakymo atsiliepimas"
        verbose_name_plural = "Užsakymo atsiliepimai"
        ordering = ["-atsiliepimo_data"]


class VartotojoProfilis(models.Model):
    vartotojas = models.OneToOneField(to=User, on_delete=models.CASCADE)
    foto = models.ImageField(default="profilio_foto/default.png", upload_to="profilio_foto")

    class Meta:
        verbose_name = "Vartotojo profilis"
        verbose_name_plural = "Vartotojų profiliai"

    def __str__(self):
        return f"{self.vartotojas.username} profilis"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        paveikslas = Image.open(self.foto.path)
        if paveikslas.height > 300 or paveikslas.width > 300:
            rodymo_dydis = (300, 300)
            paveikslas.thumbnail(rodymo_dydis)
            paveikslas.save(self.foto.path)

