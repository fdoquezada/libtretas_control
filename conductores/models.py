from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Conductor(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    rut = models.CharField(max_length=20, unique=True, verbose_name="RUT")

    class Meta:
        verbose_name = "Conductor"
        verbose_name_plural = "Conductores"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class RegistroSemanal(models.Model):
    conductor = models.ForeignKey(
        Conductor, 
        on_delete=models.CASCADE,
        verbose_name="Conductor"
    )
    semana = models.IntegerField(
        validators=[
            MinValueValidator(1, 'La semana debe ser mayor a 0'),
            MaxValueValidator(53, 'La semana no puede ser mayor a 53')
        ],
        verbose_name="Semana"
    )
    año = models.IntegerField(
        default=timezone.now().year,
        validators=[
            MinValueValidator(2000, 'El año debe ser mayor a 2000')
        ],
        verbose_name="Año"
    )
    entregado = models.BooleanField(
        default=False,
        verbose_name="Entregado"
    )
    fecha_entrega = models.DateField(
        null=True, 
        blank=True,
        verbose_name="Fecha de entrega"
    )

    class Meta:
        verbose_name = "Registro Semanal"
        verbose_name_plural = "Registros Semanales"
        ordering = ['-año', '-semana', 'conductor']
        unique_together = ['conductor', 'semana', 'año']

    def __str__(self):
        return f"{self.conductor.nombre} - Semana {self.semana} ({self.año})"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.entregado and not self.fecha_entrega:
            raise ValidationError({
                'fecha_entrega': 'La fecha de entrega es requerida cuando el registro está marcado como entregado.'
            })
