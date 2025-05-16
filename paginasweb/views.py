from turtle import home
from django.shortcuts import render
from django.views.generic import TemplateView
from featureFlags.models import Project, FeatureFlag, FlagScheduler
from django.utils.timezone import now

# Create your views here.
class PaginaInicial(TemplateView):
    template_name = 'paginasweb/index.html'

    def get_context_data(self, **kwargs):
        context = super(PaginaInicial, self).get_context_data(**kwargs)
        context['titulo'] = 'Pagina Inicial'
        return context


class SobreView(TemplateView):
    template_name = 'paginasweb/sobre.html'


class DashboardView(TemplateView):
    template_name = "paginasweb/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_projetos"] = Project.objects.count()
        context["total_flags_ativas"] = FeatureFlag.objects.filter(state="ENABLED").count()
        context["flags_recentes"] = FeatureFlag.objects.order_by("-created_at")[:5]
        context["agendamentos_proximos"] = FlagScheduler.objects.filter(scheduled_time__gte=now()).order_by("scheduled_time")[:3]
        return context