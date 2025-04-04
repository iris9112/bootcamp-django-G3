from django.urls import path

from users.views.veterinario import (
    VeterinarioListView,
    VeterinarioDetailView,
    VeterinarioCreateView,
)

app_name = "users"

urlpatterns = [
    path("veterinarios/", VeterinarioListView.as_view(), name="veterinario_list"),
    path(
        "veterinarios/create/",
        VeterinarioCreateView.as_view(),
        name="veterinario_create",
    ),
    path(
        "veterinarios/<int:pk>/",
        VeterinarioDetailView.as_view(),
        name="veterinario_detail",
    ),
]
