from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.contrib import messages

from users.forms import VeterinarioForm
from users.models import Veterinario


class VeterinarioListView(ListView):
    model = Veterinario
    template_name = "users/veterinario_list.html"
    context_object_name = "veterinarios"
    paginate_by = 6
    ordering = ["-created_at"]


class VeterinarioDetailView(DetailView):
    model = Veterinario
    template_name = "users/veterinario_detail.html"
    context_object_name = "veterinario"


class VeterinarioCreateView(LoginRequiredMixin, CreateView):
    model = Veterinario
    form_class = VeterinarioForm
    template_name = "users/veterinario_form.html"
    success_url = reverse_lazy("users:veterinario_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Veterinario registrado exitosamente.")
        return response
