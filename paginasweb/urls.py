from django.urls import path
from .views import *

urlpatterns = [
    path("", DashboardView.as_view(), name="index"),
    path("about/", SobreView.as_view(), name="about"),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
