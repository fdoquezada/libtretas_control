from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='conductores/home'),
    path('dashboard', views.dashboard, name='conductores/dashboard'),
    path('cargar/', views.cargar, name='conductores/cargar'),
    path('editar-estado/<int:registro_id>/', views.editar_estado, name='editar_estado'),
    path('cargar-conductor/', views.cargar_conductor, name='conductores/cargar_conductor'),
]
