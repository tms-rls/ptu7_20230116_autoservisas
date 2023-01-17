from django.contrib import admin

# Register your models here.

from .models import (AutomobilioModelis,
                     Automobilis,
                     Uzsakymas,
                     Paslauga,
                     UzsakymoEilute)


class UzsakymoEiluteInline(admin.TabularInline):    # kokia klase norime atvaizduoti
    model = UzsakymoEilute


class UzsakymasAdmin(admin.ModelAdmin):             # Kokioje klaseje norime matyti
    inlines = [UzsakymoEiluteInline]


admin.site.register(AutomobilioModelis)
admin.site.register(Automobilis)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(Paslauga)
admin.site.register(UzsakymoEilute)
