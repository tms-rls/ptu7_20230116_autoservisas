
from django.urls import path, include
from . import views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', views.pasisveikinimas, name='pradzia'),  # name nurodo web psl pavadinima, naudojama puslapiu iskvietimuose
    path('statistika/', views.statistika, name='statistika'),  # views faile iskvieciama apibrezta funkcija statistika
    path("automobiliai/", views.visi_automobiliai, name="visi_automobiliai"),
    path("automobiliai/<int:automobilio_id>", views.konkretus_automobilis, name="konkretus_automobilis"),
    path("uzsakymai/", views.UzsakymasListView.as_view(), name="uzsakymai"),
    path("uzsakymai/<int:pk>", views.UzsakymasDetailView.as_view(), name="konkretus_uzsakymas"),
    path('paieska/', views.paieska, name='paieska'),
    path('registracija/', views.register, name="vartotojo_registracija"),
    path('vartotojoprofilis/', views.vartotojo_profilis, name="vartotojo_profilis"),
    path('vartotojouzsakymai/', views.VartotojoUzsakymaiListView.as_view(), name="vartotojo_uzsakymai"),
    path('vartotojouzsakymai/sukurti', views.VartotojoUzsakymasCreateView.as_view(), name="vartotojo_uzsakymo_sukurimas"),
    path('vartotojouzsakymai/<int:pk>/atnaujinti', views.VartotojoUzsakymasUpdateView.as_view(), name="vartotojo_uzsakymo_atnaujinimas"),
    path('vartotojouzsakymai/<int:pk>/istrinti', views.VartotojoUzsakymasDeleteView.as_view(), name="vartotojo_uzsakymo_trynimas"),
    path('vartotojouzsakymai/<int:pk>/sukurtieilute', views.VartotojoUzsakymoEiluteCreateView.as_view(), name="vartotojo_uzsakymo_eilutes_sukurimas"),
    path('vartotojouzsakymai/<int:uzsakymas_pk>/atnaujintieilute/<int:pk>', views.VartotojoUzsakymoEiluteUpdateView.as_view(), name="vartotojo_uzsakymo_eilutes_atnaujinimas"),
    path('vartotojouzsakymai/<int:uzsakymas_pk>/istrintieilute/<int:pk>', views.VartotojoUzsakymoEiluteDeleteView.as_view(), name="vartotojo_uzsakymo_eilutes_istrynimas"),
    ]
