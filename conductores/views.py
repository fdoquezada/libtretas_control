from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Conductor, RegistroSemanal
from .forms import RegistroSemanalForm, ConductorForm
from django.utils import timezone
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'conductores/home.html')

@login_required
def cargar_conductor(request):
    if request.method == 'POST':
        form = ConductorForm(request.POST)
        if form.is_valid():
            try:
                conductor = form.save()
                messages.success(request, 'Conductor registrado exitosamente.')
                return redirect('conductores/dashboard')
            except Exception as e:
                messages.error(request, f'Error al registrar conductor: {str(e)}')
    else:
        form = ConductorForm()
    
    context = {
        'form': form,
        'titulo': 'Registrar Nuevo Conductor'
    }
    return render(request, 'conductores/cargar_conductor.html', context)


@login_required
def dashboard(request):
    # Obtener parámetros de filtro
    conductor_id = request.GET.get('conductor')
    semana = request.GET.get('semana')
    año = request.GET.get('año')
    entregado = request.GET.get('entregado')
    
    # Iniciar el queryset base
    registros = RegistroSemanal.objects.select_related('conductor').order_by('-fecha_entrega')
    
    # Aplicar filtros si están presentes
    if conductor_id:
        registros = registros.filter(conductor_id=conductor_id)
    if semana:
        registros = registros.filter(semana=semana)
    if año:
        registros = registros.filter(año=año)
    if entregado:
        registros = registros.filter(entregado=entregado=='True')
    
    # Obtener conductores para el dropdown
    conductores = Conductor.objects.all().order_by('nombre')
    
    # Obtener años únicos para el dropdown
    años = RegistroSemanal.objects.values_list('año', flat=True).distinct().order_by('-año')
    
    context = {
        'registros': registros,
        'conductores': conductores,
        'años': años,
        'total_registros': registros.count(),
        'total_conductores': conductores.count(),
        # Mantener los filtros seleccionados
        'filtros': {
            'conductor': conductor_id,
            'semana': semana,
            'año': año,
            'entregado': entregado,
        }
    }
    
    return render(request, 'conductores/dashboard.html', context)

@login_required
def cargar(request):
    if request.method == 'POST':
        form = RegistroSemanalForm(request.POST)
        if form.is_valid():
            try:
                registro = form.save()
                messages.success(request, 'Registro guardado exitosamente.')
                return redirect('dashboard')  # Asegúrate que este sea el nombre correcto en urls.py
            except Exception as e:
                messages.error(request, f'Error al guardar el registro: {str(e)}')
                return render(request, 'conductores/cargar.html', {'form': form})
    else:
        form = RegistroSemanalForm()
        
    context = {
        'form': form,
        'titulo': 'Cargar Nuevo Registro'
    }
    
    return render(request, 'conductores/cargar.html', context)

def editar_estado(request, registro_id):
    registro = get_object_or_404(RegistroSemanal, id=registro_id)
    
    if request.method == 'POST':
        try:
            registro.entregado = not registro.entregado  # Cambia el estado
            if registro.entregado:
                registro.fecha_entrega = date.today()  # Actualiza la fecha si está entregado
            else:
                registro.fecha_entrega = None  # Limpia la fecha si no está entregado
            registro.save()
            messages.success(request, 'Estado actualizado correctamente.')
        except Exception as e:
            messages.error(request, f'Error al actualizar el estado: {str(e)}')
    
    return redirect('conductores/dashboard')
