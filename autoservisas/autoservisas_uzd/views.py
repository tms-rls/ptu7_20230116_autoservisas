# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from .models import (Automobilis,
                     Uzsakymas,
                     Paslauga)
from django.contrib.auth.mixins import LoginRequiredMixin


def pasisveikinimas(request):
    sesiju_kiekis = request.session.get('sesiju_kiekis', 1)
    request.session['sesiju_kiekis'] = sesiju_kiekis + 1
    return render(request, 'pradzia.html', {'sesiju_kiekis': sesiju_kiekis})


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
    paginator = Paginator(visi_automobiliai, 2)
    page_number = request.GET.get('page')
    puslapiuoti_automobiliai = paginator.get_page(page_number)
    context = {
        "visi_automobiliai": puslapiuoti_automobiliai
    }
    return render(request, "automobiliai.html", context=context)


def konkretus_automobilis(request, automobilio_id):
    konkretus_automobilis = get_object_or_404(Automobilis, pk=automobilio_id)
    context = {
        "konkretus_automobilis": konkretus_automobilis,
    }
    return render(request, "automobilis.html", context=context)


def paieska(request):
    query = request.GET.get('query')
    search_results = Automobilis.objects.filter(Q(valstybinis_nr__icontains=query) |
                                                Q(automobilio_modelis__marke__icontains=query) |
                                                Q(automobilio_modelis__marke__icontains=query) |
                                                Q(vin_kodas__icontains=query) |
                                                Q(klientas__icontains=query))
    return render(request, 'paieska.html', {'visi_automobiliai': search_results, 'query': query})


class UzsakymasListView(generic.ListView):
    model = Uzsakymas
    paginate_by = 3
    template_name = "uzsakymai.html"
    context_object_name = "uzsakymai"


class UzsakymasDetailView(generic.DetailView):
    model = Uzsakymas
    template_name = "uzsakymas.html"
    context_object_name = "konkretus_uzsakymas"


class VartotojoUzsakymaiListView(generic.ListView, LoginRequiredMixin):
    model = Uzsakymas
    template_name = "vartotojo_uzsakymai.html"
    paginate_by = 2
    context_object_name = "vartotojo_uzsakymai"

    def get_queryset(self):
        return Uzsakymas.objects.filter(vartotojas=self.request.user)
