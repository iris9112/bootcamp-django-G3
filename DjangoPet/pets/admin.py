from django.contrib import admin

from pets.models import Mascota, FichaMedica


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "especie", "raza", "propietario", "estado")
    list_filter = ("especie", "estado")
    search_fields = ("nombre", "propietario__usuario__last_name")


@admin.register(FichaMedica)
class FichaMedicaAdmin(admin.ModelAdmin):
    list_display = ("numero_ficha", "mascota", "desparasitado", "created_at")
    list_filter = ("desparasitado",)
    search_fields = ("mascota__nombre", "numero_ficha")
