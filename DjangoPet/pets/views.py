from django.views.generic import ListView, DetailView

from pets.choices import EstadoMascotaChoices
from pets.models import Mascota


class MascotaListView(ListView):
    model = Mascota
    template_name = "pets/mascota_list.html"
    context_object_name = "mascotas"
    paginate_by = 6
    ordering = ["-created_at"]

    def get_queryset(self):
        return Mascota.objects.exclude(estado=EstadoMascotaChoices.FALLECIDO)


class MascotaDetailView(DetailView):
    model = Mascota
    template_name = "pets/mascota_detail.html"
    context_object_name = "mascota"
