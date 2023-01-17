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


class UzsakymasAdmin(admin.ModelAdmin):             # Kokioje klaseje norime matyti kita klase
    inlines = [UzsakymoEiluteInline]
    list_display = ("automobilis", "data")


class PaslaugaAdmin(admin.ModelAdmin):
    list_display = ("pavadinimas", "kaina")


admin.site.register(AutomobilioModelis)
admin.site.register(Automobilis, AutomobilisAdmin)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(Paslauga, PaslaugaAdmin)
admin.site.register(UzsakymoEilute)
