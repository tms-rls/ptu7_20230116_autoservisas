# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import (Automobilis,
                     Uzsakymas,
                     Paslauga)


def statistika(request):
    paslaugu_kiekis = Paslauga.objects.all().count()
    atliktu_uzsakymu_kiekis = Uzsakymas.objects.filter(statusas__exact=3).count()
    automobiliu_kiekis = Automobilis.objects.all().count()

    skaiciai = {
        "paslaugu_kiekis": paslaugu_kiekis,
        "atliktu_uzsakymu_kiekis": atliktu_uzsakymu_kiekis,
        "automobiliu_kiekis": automobiliu_kiekis,
    }

    return render(request, 'statistika.html', context=skaiciai)


def visi_automobiliai(request):
    visi_automobiliai = Automobilis.objects.all()
    context = {
        "visi_automobiliai": visi_automobiliai
    }
    return render(request, "automobiliai.html", context=context)


def konkretus_automobilis(request, automobilio_id):
    konkretus_automobilis = get_object_or_404(Automobilis, pk=automobilio_id)
    context = {
        "konkretus_automobilis": konkretus_automobilis,
    }
    return render(request, "automobilis.html", context=context)


class UzsakymasListView(generic.ListView):
    model = Uzsakymas
    context_object_name = "uzsakymai"
    template_name = "uzsakymai.html"
