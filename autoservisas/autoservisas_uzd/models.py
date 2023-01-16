
# Create your models here.


from django.db import models
import uuid


class AutomobilioModelis(models.Model):
    marke = models.CharField(verbose_name="Automobilio gamintojas", max_length=50, help_text="Įveskite automobilio gamintoją")
    modelis = models.CharField(verbose_name="Automobilio modelis", max_length=100, help_text="Įveskite automobilio modelį")
    metai = models.CharField(verbose_name="Automobilio pagaminimo metai", max_length=10, help_text="Įveskite automobilio pagaminimo metus")
    variklis = models.CharField(verbose_name="Automobilio variklis", max_length=5, help_text="Įveskite automobilio variklio tūrį")

    class Meta:
        verbose_name_plural = "Automobilio modeliai"

    def __str__(self):
        return f"{self.marke} {self.modelis} {self.metai}"


class Automobilis(models.Model):
    valstybinis_nr = models.CharField(verbose_name="Valstybinis numeris", max_length=10, help_text="Įveskite valstybinį numerį")
    automobilio_modelis = models.ForeignKey(to="AutomobilioModelis", on_delete=models.SET_NULL, null=True)
    vin_kodas = models.CharField(verbose_name="VIN kodas", max_length=50, help_text="Įveskite VIN kodą")
    klientas = models.CharField(verbose_name="Klientas", max_length=200, help_text="Įveskite klientą")

    class Meta:
        verbose_name_plural = "Automobiliai"

    def __str__(self):
        return f"{self.valstybinis_nr} {self.automobilio_modelis}"


class Uzsakymas(models.Model):
    uuid = models.UUIDField(verbose_name="UUID", default=uuid.uuid4, help_text="Unikalus ID užsakymui")
    data = models.CharField(verbose_name="Užsakymo data", max_length=20)
    automobilis = models.ForeignKey(to="Automobilis", on_delete=models.CASCADE)
    suma = models.CharField(verbose_name="Užsakymo suma", max_length=10)

    class Meta:
        verbose_name_plural = "Užsakymai"

    def __str__(self):
        return f"{self.automobilis} - {self.uuid}"


class Paslauga(models.Model):
    pavadinimas = models.CharField(verbose_name="Paslaugos pavadinimas", max_length=200, help_text="Įveskite paslaugos pavadinimą")
    kaina = models.CharField(verbose_name="Paslaugos kaina", max_length=10, help_text="Įveskite paslaugos kainą")

    class Meta:
        verbose_name_plural = "Paslaugos"

    def __str__(self):
        return f"{self.pavadinimas}"


class UzsakymoEilute(models.Model):
    uzsakymas = models.ForeignKey(to="Uzsakymas", on_delete=models.CASCADE)
    paslauga = models.ForeignKey(to="Paslauga", on_delete=models.SET_NULL, null=True)
    kiekis = models.CharField(verbose_name="Kiekis", max_length=5, help_text="Įveskite kiekį")
    kaina = models.CharField(verbose_name="Kaina", max_length=10, help_text="Įveskite kainą")

    class Meta:
        verbose_name_plural = "Užsakymo eilutės"

    def __str__(self):
        return f"{self.paslauga} - {self.uzsakymas}"
