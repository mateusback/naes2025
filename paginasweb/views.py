from turtle import home
from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class PaginaInicial(TemplateView):
    template_name = 'paginasweb/index.html'

    def get_context_data(self, **kwargs):
        context = super(PaginaInicial, self).get_context_data(**kwargs)
        context['titulo'] = 'Pagina Inicial'
        return context


class SobreView(TemplateView):
    template_name = 'paginasweb/sobre.html'
