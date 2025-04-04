from django import forms
from django.contrib.auth.models import User
from users.models import Propietario, Veterinario


class PropietarioForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label="Nombre de usuario")
    first_name = forms.CharField(max_length=30, required=True, label="Nombre")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido")
    email = forms.EmailField(required=True, label="Correo electrónico")
    password = forms.CharField(
        widget=forms.PasswordInput(), required=True, label="Contraseña"
    )

    class Meta:
        model = Propietario
        fields = ["identificacion", "telefono", "direccion", "activo"]
        labels = {
            "identificacion": "Número de identificación",
            "telefono": "Teléfono",
            "direccion": "Dirección",
            "activo": "¿Está activo?",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = {
            "username": self.fields.pop("username"),
            "first_name": self.fields.pop("first_name"),
            "last_name": self.fields.pop("last_name"),
            "email": self.fields.pop("email"),
            "password": self.fields.pop("password"),
            "identificacion": self.fields.pop("identificacion"),
            "telefono": self.fields.pop("telefono"),
            "direccion": self.fields.pop("direccion"),
            "activo": self.fields.pop("activo"),
        }

    def save(self, commit=True):
        user_data = {
            "username": self.cleaned_data["username"],
            "first_name": self.cleaned_data["first_name"],
            "last_name": self.cleaned_data["last_name"],
            "email": self.cleaned_data["email"],
        }
        password = self.cleaned_data["password"]

        if self.instance.pk:
            self.instance.usuario.username = user_data["username"]
            self.instance.usuario.first_name = user_data["first_name"]
            self.instance.usuario.last_name = user_data["last_name"]
            self.instance.usuario.email = user_data["email"]
            if password:
                self.instance.usuario.set_password(password)
            self.instance.usuario.save()
        else:
            user = User.objects.create_user(**user_data, password=password)
            self.instance.usuario = user

        return super().save(commit)


class VeterinarioForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = Veterinario
        fields = ["identificacion", "telefono", "especializacion", "disponibilidad"]

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            email=self.cleaned_data["email"],
        )
        veterinario = super().save(commit=False)
        veterinario.usuario = user
        veterinario.activo = True

        if commit:
            veterinario.save()
        return veterinario
