from django.contrib import admin

# Register your models here.

from .models import (AutomobilioModelis,
                     Automobilis,
                     Uzsakymas,
                     Paslauga,
                     UzsakymoEilute)


class AutomobilisAdmin(admin.ModelAdmin):
    list_display = ("klientas", "automobilio_modelis", "valstybinis_nr", "vin_kodas")
    list_filter = ("klientas", "automobilio_modelis__modelis")
    search_fields = ("valstybinis_nr", "vin_kodas")


class UzsakymoEiluteInline(admin.TabularInline):    # kokia klase norime atvaizduoti kitoje klaseje, nereikia registruoti atskirai
    model = UzsakymoEilute
    extra = 0


class UzsakymoEiluteAdmin(admin.ModelAdmin):
    list_display = ("uzsakymas", "paslauga", "kiekis", "uzsakymo_eilutes_suma")    #nurodome ne lauką o funkciją/metodą


class UzsakymasAdmin(admin.ModelAdmin):             # Kokioje klaseje norime matyti kita klase
    inlines = [UzsakymoEiluteInline]
    list_display = ("automobilis", "data", "statusas", "atlikimo_terminas", "bendra_uzsakymo_suma", "vartotojas")
    list_editable = ("statusas", "atlikimo_terminas")


class PaslaugaAdmin(admin.ModelAdmin):
    list_display = ("pavadinimas", "kaina")


admin.site.register(AutomobilioModelis)
admin.site.register(Automobilis, AutomobilisAdmin)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(Paslauga, PaslaugaAdmin)
admin.site.register(UzsakymoEilute, UzsakymoEiluteAdmin)
