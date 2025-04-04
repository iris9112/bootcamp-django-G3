from django.urls import path

from pets.views import MascotaListView, MascotaDetailView

app_name = "pets"

urlpatterns = [
    path("mascotas/", MascotaListView.as_view(), name="mascota_list"),
    path("mascotas/<int:pk>/", MascotaDetailView.as_view(), name="mascota_detail"),
]
