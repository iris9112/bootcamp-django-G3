from django.contrib import admin

from appointments.models import Consulta


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "mascota",
        "veterinario",
        "fecha_consulta",
        "estado_cita",
        "requiere_control",
        "created_at",
    )
    list_filter = ("estado_cita", "veterinario")
    search_fields = ("mascota__nombre", "veterinario__usuario__last_name")
    ordering = ("-created_at",)
