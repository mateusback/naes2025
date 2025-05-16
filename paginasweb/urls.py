from django.urls import path
from .views import PaginaInicial, SobreView, DashboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="index"),
    path("sobre/", SobreView.as_view(), name="sobre"),
]
