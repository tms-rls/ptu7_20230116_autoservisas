# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.views.generic.edit import FormMixin
from django.core.paginator import Paginator
from django.db.models import Q
from .models import (Automobilis,
                     Uzsakymas,
                     Paslauga)
from .forms import UzsakymoAtsiliepimasForm, UserUpdateForm, VartotojoProfilisUpdateForm, VartotojoUzsakymasCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('vartotojo_registracija')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('vartotojo_registracija')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('vartotojo_registracija')  # nukreipiame i registracijos puslapi atgal pagal NAME is URLS'u
    else:
        return render(request, 'vartotojo_registracija.html')


@login_required
def vartotojo_profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = VartotojoProfilisUpdateForm(request.POST, request.FILES, instance=request.user.vartotojoprofilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Vartotojo profilis atnaujintas!")
            return redirect("vartotojo_profilis")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = VartotojoProfilisUpdateForm(instance=request.user.vartotojoprofilis)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'vartotojo_profilis.html', context=context)


class UzsakymasListView(generic.ListView):
    model = Uzsakymas
    paginate_by = 3
    template_name = "uzsakymai.html"
    context_object_name = "uzsakymai"


class UzsakymasDetailView(FormMixin, generic.DetailView):
    model = Uzsakymas
    template_name = "uzsakymas.html"
    context_object_name = "konkretus_uzsakymas"
    form_class = UzsakymoAtsiliepimasForm

    # nurodome, kur atsidursime komentaro sėkmės atveju.
    def get_success_url(self):
        return reverse("konkretus_uzsakymas", kwargs={"pk": self.object.id})    # grazina i save todel reikia id

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # štai čia nurodome, kad uzsakymas bus būtent tas, po kuriuo komentuojame, o vartotojas bus tas, kuris
    # yra prisijungęs.
    def form_valid(self, form):
        form.instance.uzsakymas = self.object
        form.instance.komentatorius = self.request.user
        form.save()
        return super(UzsakymasDetailView, self).form_valid(form)


class VartotojoUzsakymaiListView(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas
    template_name = "vartotojo_uzsakymai.html"
    paginate_by = 2
    context_object_name = "vartotojo_uzsakymai"

    def get_queryset(self):
        return Uzsakymas.objects.filter(vartotojas=self.request.user)


class VartotojoUzsakymasDetailView(LoginRequiredMixin, generic.DetailView):
    model = Uzsakymas
    template_name = "vartotojo_uzsakymas.html"
    context_object_name = "konkretus_vartotojo_uzsakymas"


class VartotojoUzsakymasCreateView(LoginRequiredMixin, generic.CreateView):
    model = Uzsakymas
    # fields = ["automobilis", "atlikimo_terminas", "statusas"]  # del datepicker kuriama jau per forms.py o ne per cia
    success_url = "/autoservice/vartotojouzsakymai/"
    template_name = "vartotojo_uzsakymo_forma.html"
    form_class = VartotojoUzsakymasCreateForm

    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        form.save()
        return super().form_valid(form)


class VartotojoUzsakymasUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Uzsakymas
    # fields = ["automobilis", "atlikimo_terminas", "statusas"]  # del datepicker kuriama jau per forms.py o ne per cia
    success_url = "/autoservice/vartotojouzsakymai/"
    template_name = "vartotojo_uzsakymo_forma.html"
    form_class = VartotojoUzsakymasCreateForm

    def test_func(self):
        uzsakymas = self.get_object()
        return uzsakymas.vartotojas == self.request.user

    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        form.save()
        return super().form_valid(form)


class VartotojoUzsakymasDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Uzsakymas
    success_url = "/autoservice/vartotojouzsakymai/"
    template_name = "vartotojo_uzsakymo_istrynimas.html"
    context_object_name = "konkretus_vartotojo_uzsakymas"

    def test_func(self):
        uzsakymas = self.get_object()
        return uzsakymas.vartotojas == self.request.user
