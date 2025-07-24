from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from featureFlags.models import Project, FeatureFlag, FlagScheduler
from django.utils.timezone import now


class LoginView(TemplateView):
    template_name = "paginasweb/login.html"

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        senha = request.POST.get("senha")
        user = authenticate(request, username=username, password=senha)
        if user:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "Usuário ou senha inválidos.")
        return render(request, self.template_name)


class SignupView(TemplateView):
    template_name = "paginasweb/signup.html"

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmacao = request.POST.get("confirmacao")

        if senha != confirmacao:
            messages.error(request, "As senhas não coincidem.")
            return render(request, self.template_name)

        if User.objects.filter(username=username).exists():
            messages.error(request, "Esse nome de usuário já existe.")
            return render(request, self.template_name)

        user = User.objects.create_user(username=username, email=email, password=senha)
        login(request, user)
        return redirect("dashboard")


def logout_view(request):
    logout(request)
    return redirect("login")


class PaginaInicial(TemplateView):
    template_name = 'paginasweb/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Página Inicial'
        return context


class SobreView(TemplateView):
    template_name = 'paginasweb/sobre.html'


@method_decorator(login_required(login_url='login'), name='dispatch')
class DashboardView(TemplateView):
    template_name = "paginasweb/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_projetos"] = Project.objects.count()
        context["total_flags_ativas"] = FeatureFlag.objects.filter(state="ENABLED").count()
        context["flags_recentes"] = FeatureFlag.objects.order_by("-created_at")[:5]
        context["agendamentos_proximos"] = FlagScheduler.objects.filter(scheduled_time__gte=now()).order_by("scheduled_time")[:3]
        return context
