from django.contrib import admin

from users.forms import PropietarioForm
from users.models import Propietario, Veterinario


@admin.register(Propietario)
class PropietarioAdmin(admin.ModelAdmin):
    form = PropietarioForm
    list_display = ("usuario", "identificacion", "telefono", "activo")
    list_filter = ("activo",)
    search_fields = (
        "usuario__first_name",
        "usuario__last_name",
        "usuario__email",
        "identificacion",
    )

    def get_usuario_email(self, obj):
        if email := obj.usuario.email:
            return email
        return "-"

    get_usuario_email.short_description = "Email"


@admin.register(Veterinario)
class VeterinarioAdmin(admin.ModelAdmin):
    list_display = ("usuario", "especializacion", "telefono", "activo")
    list_filter = ("especializacion", "activo")
    search_fields = (
        "usuario__first_name",
        "usuario__last_name",
        "usuario__email",
        "especializacion",
    )
