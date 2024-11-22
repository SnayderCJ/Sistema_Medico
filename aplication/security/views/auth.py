from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from aplication.security.forms.forms import CustomUserCreationForm, CustomUserUpdateForm, CustomPasswordChangeForm
from django.contrib.auth.models import User


class ProfileView(View):
    def get(self, request):
        data = {
            "title1": "IC - Perfil",
            "title2": "Perfil de Usuario"
        }
        return render(request, 'profile.html', data)


class UpdateProfileView(View):
    def get(self, request):
        data = {
            "title1": "IC - Actualizar Perfil",
            "title2": "Actualizar Perfil"
        }
        form = CustomUserUpdateForm(instance=request.user)
        return render(request, 'update_profile.html', {'form': form, **data})

    def post(self, request):
        data = {
            "title1": "IC - Actualizar Perfil",
            "title2": "Actualizar Perfil"
        }
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado exitosamente!')
            return redirect('security:auth_profile')
        return render(request, 'update_profile.html', {'form': form, **data})


class SignupView(View):
    def get(self, request):
        data = {
            "title1": "IC - Registro",
            "title2": "Registro de Administradores"
        }
        form = CustomUserCreationForm()
        return render(request, "signup.html", {"form": form, **data})

    def post(self, request):
        data = {
            "title1": "IC - Registro",
            "title2": "Registro de Usuarios"
        }
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, '¡Registro exitoso! Por favor, inicia sesión.')
            return redirect("security:auth_login")
        else:
            error_messages = []
            for field in form:
                for error in field.errors:
                    error_messages.append(f"{field.label}: {error}")
            for error in form.non_field_errors():
                error_messages.append(error)
            data["errors"] = error_messages
            return render(request, "signup.html", {"form": form, **data})


from django.contrib.auth import get_user_model

class SigninView(LoginView):
    template_name = 'signin.html'
    success_url = reverse_lazy('security:modules_list')
    redirect_authenticated_user = True
    form_class = AuthenticationForm
    extra_context = {
        "title1": "Login",
        "title2": "Inicio de Sesión"
    }

    def form_valid(self, form):
        email = form.cleaned_data.get('username')  # 'username' en el formulario se debe interpretar como 'email'
        password = form.cleaned_data.get('password')
        print(f"Intentando autenticar con: {email} / {password}")  # Depuración

        # Buscar al usuario por el correo electrónico
        User = get_user_model()
        try:
            user = User.objects.get(email=email)  # Buscamos el usuario por su correo electrónico
        except User.DoesNotExist:
            user = None

        # Intentamos autenticar el usuario con el correo electrónico y la contraseña
        if user is not None and user.check_password(password):
            if user.is_active:  # Verifica si el usuario está activo
                login(self.request, user)
                return redirect(self.success_url)
            else:
                form.add_error(None, "El usuario está inactivo.")
        else:
            form.add_error(None, "El correo electrónico o la contraseña son incorrectos.")

        return self.render_to_response(self.get_context_data(form=form))




class SignoutView(LogoutView):
    next_page = 'core:home'


class ChangePasswordView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'reseteo.html'
    success_url = reverse_lazy('security:auth_profile')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title1'] = "IC - Cambiar Contraseña"
        return data

    def form_valid(self, form):
        messages.success(self.request, '¡Tu contraseña ha sido actualizada exitosamente!')
        return super().form_valid(form)
