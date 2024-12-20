from django.db import models, IntegrityError
from django.db.models import Sum
from decimal import Decimal
from aplication.core.models import Paciente, Diagnostico, Medicamento, Doctor
from doctor.const import CITA_CHOICES, DIA_SEMANA_CHOICES, EXAMEN_CHOICES

# Modelo que representa los días y horas de atención de un doctor.
# Incluye los días de la semana, la hora de inicio y la hora de fin de la atención.
class HorarioAtencion(models.Model):
    # Días de la semana en los que el doctor atiende
    dia_semana = models.CharField(max_length=10, choices=DIA_SEMANA_CHOICES, verbose_name="Día de la Semana",unique=True)
    # Hora de inicio de atención del doctor
    hora_inicio = models.TimeField(verbose_name="Hora de Inicio")
    # Hora de fin de atención del doctor
    hora_fin = models.TimeField(verbose_name="Hora de Fin")
    # Inicio de descanso de atención del doctor
    Intervalo_desde=models.TimeField(verbose_name="Intervalo desde")
     # Fin de descanso de atención del doctor
    Intervalo_hasta=models.TimeField(verbose_name="Intervalo Hasta")

    activo = models.BooleanField(default=True,verbose_name="Activo")
    
    def __str__(self):
        return f"{self.dia_semana}"

    class Meta:
        # Nombre singular y plural del modelo en la interfaz administrativa
        verbose_name = "Horario de Atención Doctor"
        verbose_name_plural = "Horarios de Atención de los Doctores"

# modelo que almacena los datos de la cita de los pacientes
class CitaMedica(models.Model):
 
     # Relación con el modelo Paciente, indica qué paciente ha reservado la cita
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, verbose_name="Paciente",related_name="pacientes_citas")
     # Fecha de la cita médica
    fecha = models.DateField(verbose_name="Fecha de la Cita")
    # Hora de la cita médica
    hora_cita = models.TimeField(verbose_name="Hora de la Cita")
    # Estado de la cita (ej. Programada, Cancelada, Realizada)
    estado = models.CharField(
        max_length=1,
        choices=CITA_CHOICES,
        verbose_name="Estado de la Cita"
    )

    def __str__(self):
        return f"Cita {self.paciente} el {self.fecha} a las {self.hora_cita}"

    class Meta:
        # Ordena las citas por fecha y hora
        ordering = ['fecha', 'hora_cita']
        indexes = [
            models.Index(fields=['fecha', 'hora_cita'], name='idx_fecha_hora'),
        ]
        # Nombre singular y plural del modelo en la interfaz administrativa
        verbose_name = "Cita Médica"
        verbose_name_plural = "Citas Médicas"
        
    @staticmethod
    def cantidad_cita():
       return CitaMedica.objects.all().count()

# Modelo que representa los costos asociados a una atención médica,
# incluyendo consulta, servicios adicionales (exámenes, procedimientos), y otros costos.
class CostosAtencion(models.Model):
    atencion = models.ForeignKey('Atencion', on_delete=models.PROTECT, related_name="costos")
    costo_consulta = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo de la Consulta", default=10.00)
    descripcion = models.TextField(null=True, blank=True, verbose_name="Descripción de los Costos")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total", default=0.00)  # Valor predeterminado
    fecha_pago = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Pago")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return f"{self.atencion} - Total: {self.total}"

    def calcular_total(self):
        """
        Calcula el total basado en los servicios adicionales, exámenes y medicamentos relacionados.
        """
        total = Decimal(self.costo_consulta)
        if self.pk:  # Solo calcular si la instancia tiene clave primaria
            total += sum(Decimal(servicio.costo_servicio) for servicio in self.servicios.all())
            total += sum(Decimal(detalle.calcular_costo_examen()) for detalle in self.atencion.detalles.all())
            total += sum(Decimal(detalle.medicamento.precio) * Decimal(detalle.cantidad) for detalle in self.atencion.detalles.all())
        return total

    def save(self, *args, **kwargs):
        if not self.pk and CostosAtencion.objects.filter(atencion=self.atencion).exists():
            raise IntegrityError("Ya existe un costo asociado a esta atención.")
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-fecha_pago']
        verbose_name = "Costo de Atención"
        verbose_name_plural = "Costos de Atención"

# Modelo que representa un servicio adicional ofrecido durante una atención médica.
# Puede incluir exámenes, procedimientos, o cualquier otro servicio.
class ServiciosAdicionales(models.Model):
    nombre_servicio = models.CharField(max_length=255, verbose_name="Nombre del Servicio")
    costo_servicio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo del Servicio")
    descripcion = models.TextField(null=True, blank=True, verbose_name="Descripción del Servicio")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    costo_atencion = models.ForeignKey(
        CostosAtencion,
        on_delete=models.CASCADE,
        verbose_name="Costo Atención",
        related_name="servicios"
    )

    def __str__(self):
        return self.nombre_servicio

    class Meta:
        ordering = ['nombre_servicio']
        verbose_name = "Servicio Adicional"
        verbose_name_plural = "Servicios Adicionales"



# Modelo que representa los detalles de los costos asociados a una atención médica
class CostoAtencionDetalle(models.Model):
    costo_atencion = models.ForeignKey(CostosAtencion, on_delete=models.PROTECT, verbose_name="Costo Atención", related_name="costos_atenciones")
    servicios_adicionales = models.ForeignKey(ServiciosAdicionales, on_delete=models.PROTECT, verbose_name="Servicios Adicionales", related_name="servicios_adicionales")
    costo_servicio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo del Servicio")

    def __str__(self):
        return f"{self.servicios_adicionales} - Costo: {self.costo_servicio}"  # Obtener costo desde ServiciosAdicionales

    class Meta:
        verbose_name = "Costo detalle Atención"
        verbose_name_plural = "Costos detalles Atención"

# Modelo que representa los exámenes solicitados durante una atención médica.
class ExamenSolicitado(models.Model):
    nombre_examen = models.CharField(max_length=255, verbose_name="Nombre del Examen")
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, verbose_name="Paciente", related_name="examenes")
    fecha_solicitud = models.DateField(auto_now_add=True, verbose_name="Fecha de Solicitud")
    atencion = models.ForeignKey('Atencion', on_delete=models.PROTECT, verbose_name="Atención Médica", related_name="examenes", null=True, blank=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo del Examen")
    resultado = models.FileField(upload_to='resultados_examenes/', null=True, blank=True, verbose_name="Resultado del Examen")
    comentario = models.TextField(null=True, blank=True, verbose_name="Comentario")
    estado = models.CharField(max_length=20, choices=EXAMEN_CHOICES, verbose_name="Estado del Examen")

    def __str__(self):
        return f"Examen {self.nombre_examen}"

    class Meta:
        ordering = ['-fecha_solicitud']
        verbose_name = "Examen Médico"
        verbose_name_plural = "Exámenes Médicos"

# Modelo que representa los detalles de una atención médica.
# Relaciona cada atención con los medicamentos recetados y su cantidad.
class DetalleAtencion(models.Model):
    atencion = models.ForeignKey('Atencion', on_delete=models.CASCADE, verbose_name="Atención", related_name="detalles")
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, verbose_name="Medicamento", related_name="detalles_atencion")
    examen_solicitado = models.ForeignKey(
        ExamenSolicitado, on_delete=models.CASCADE, verbose_name="Examen Solicitado", related_name="detalles_atencion", null=True, blank=True
    )
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    prescripcion = models.TextField(verbose_name="Prescripción")
    duracion_tratamiento = models.PositiveIntegerField(verbose_name="Duración del Tratamiento (días)", null=True, blank=True)

    def calcular_costo_examen(self):
        """
        Calcula el costo del examen asociado, si lo hay.
        """
        if self.examen_solicitado:
            return self.examen_solicitado.costo
        return Decimal(0)

    def save(self, *args, **kwargs):
        # Validar que el examen esté asociado al paciente correcto
        if self.examen_solicitado and self.atencion.paciente != self.examen_solicitado.paciente:
            raise IntegrityError("El examen solicitado no pertenece al paciente de esta atención.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Detalle de {self.medicamento} para {self.atencion}"

    class Meta:
        ordering = ['atencion']
        verbose_name = "Detalle de Atención"
        verbose_name_plural = "Detalles de Atención"



# Modelo que representa la cabecera de una atención médica.
# Contiene la información general del paciente, diagnóstico, motivo de consulta y tratamiento.
class Atencion(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, verbose_name="Paciente", related_name="doctores_atencion")
    fecha_atencion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Atención")
    presion_arterial = models.CharField(max_length=20, null=True, blank=True, verbose_name="Presión Arterial")
    pulso = models.IntegerField(null=True, blank=True, verbose_name="Pulso (ppm)")
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Temperatura (°C)")
    frecuencia_respiratoria = models.IntegerField(null=True, blank=True, verbose_name="Frecuencia Respiratoria(rpm)")
    saturacion_oxigeno = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Saturación de Oxígeno (%)")
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)")
    altura = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Altura (m)")
    motivo_consulta = models.TextField(verbose_name="Motivo de Consulta")
    sintomas = models.TextField(verbose_name="Sintomas")
    tratamiento = models.TextField(verbose_name="Plan de Tratamiento")
    diagnostico = models.ManyToManyField(Diagnostico, verbose_name="Diagnósticos", related_name="diagnosticos_atencion")
    examen_fisico = models.TextField(null=True, blank=True, verbose_name="Examen Físico")
    examenes_enviados = models.ManyToManyField(ExamenSolicitado, blank=True, verbose_name="Exámenes Enviados", related_name="atenciones_examenes") 
    comentario_adicional = models.TextField(null=True, blank=True, verbose_name="Comentario")

    @property
    def get_diagnosticos(self):
        return " - ".join([c.descripcion for c in self.diagnostico.all().order_by('descripcion')])
    
    @staticmethod
    def cantidad_atenciones():
       return Atencion.objects.all().count()
    
    @property
    def calcular_imc(self):
        if self.peso and self.altura and self.altura > 0:
            return round(float(self.peso) / (float(self.altura) ** 2), 2)
        else:
            return None
        
    def __str__(self):
        return f"Atención de {self.paciente} el {self.fecha_atencion}"

    class Meta:
        ordering = ['-fecha_atencion']
        verbose_name = "Atención"
        verbose_name_plural = "Atenciones"


class Certificado(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, verbose_name="Paciente")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="Doctor")
    diagnostico = models.ManyToManyField(Diagnostico, verbose_name="Diagnósticos", related_name="certificados_diagnosticos")
    fecha_emision = models.DateField(auto_now_add=True, verbose_name="Fecha de Emisión")
    tipo_certificado = models.CharField(max_length=100, verbose_name="Tipo de Certificado")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")

    def __str__(self):
        return f"Certificado de {self.paciente} - {self.tipo_certificado}"

    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"

# Modelo que representa el pago realizado para una atención médica.
class Pago(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, verbose_name="Paciente")
    costo_atencion = models.OneToOneField(CostosAtencion, on_delete=models.PROTECT, verbose_name="Costo Atención")
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto", editable=False)
    metodo_pago = models.CharField(max_length=50, choices=[
        ('Efectivo', 'Efectivo'),
        ('PayPal', 'PayPal')
    ], verbose_name="Método de Pago")
    pagado = models.BooleanField(default=False, verbose_name="Pagado")
    fecha_pago = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Pago")

    def __str__(self):
        return f"{self.paciente} - {self.costo_atencion} - {self.monto} - {self.metodo_pago}"

    def calcular_monto_total(self):
        total_atencion = self.costo_atencion.total
        total_servicios = ServiciosAdicionales.objects.filter(
            costos_atenciones__costo_atencion=self.costo_atencion
        ).aggregate(Sum('costo_servicio'))['costo_servicio__sum'] or 0
        total_examenes = ExamenSolicitado.objects.filter(
            atencion=self.costo_atencion.atencion
        ).aggregate(Sum('costo'))['costo__sum'] or 0

        return total_atencion + total_servicios + total_examenes

    def save(self, *args, **kwargs):
        if not self.monto:
            self.monto = self.calcular_monto_total()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
