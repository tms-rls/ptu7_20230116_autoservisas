
from django.urls import path
from . import views

urlpatterns = [
    path('', views.pasisveikinimas, name='pradzia'),  # name nurodo web psl pavadinima, naudojama puslapiu iskvietimuose
    path('statistika/', views.statistika, name='statistika'),  # views faile iskvieciama apibrezta funkcija statistika
    path("automobiliai/", views.visi_automobiliai, name="visi_automobiliai"),
    path("automobiliai/<int:automobilio_id>", views.konkretus_automobilis, name="konkretus_automobilis"),
    path("uzsakymai/", views.UzsakymasListView.as_view(), name="uzsakymai"),
    path("uzsakymai/<int:pk>", views.UzsakymasDetailView.as_view(), name="konkretus_uzsakymas"),
    path('paieska/', views.paieska, name='paieska'),
    ]
