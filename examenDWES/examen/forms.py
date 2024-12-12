from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime

# Formulario para promocion
class PromocionModelForm(ModelForm):
    class Meta:
        model = Promocion
        fields = ['nombre', 'descripcion', 'descuento', 'fecha_inicio', 'fecha_fin', 'esta_activa', 'producto']
        labels = {
            "nombre": "Nombre de la promocion",
            "descripcion": "Descripción de la promoción",
            "descuento": "Descuento que se le aplique, entre 0 y 10",
            "fecha_inicio": "Fecha de inicio de la promoción",
            "fecha_fin": "Fecha de fin de la promoción",
            "esta_activa": "Indica si la promo esta activa",
            "producto": "Indica el producto al que aplicar la promocion",
        }
        help_texts = {
            "nombre": "Nombre de la promocion (máximo 100 caracteres).",
            "descripcion": "Descripción de la promoción.",
            "descuento": "Cantidad que se va a descontar, entre 0 y 10",
            "fecha_inicio": "Fecha en la que comienza la promoción.",
            "fecha_fin": "Fecha en la que finaliza la promoción.",
            "esta_activa": "Nos avisa de si la promoción esta activa",
            "producto": "Indica el producto al que aplicar la promocion",
        }
        widgets = {
            "fecha_inicio": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "fecha_fin": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "descripcion": forms.Textarea(attrs={"rows": 3, "placeholder": "Añade una breve descripción de la promoción."}),
        }
        localized_fields = ["fecha_inicio", "fecha_fin"]
        
    def clean(self):
 
        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        descuento = self.cleaned_data.get('descuento')
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_fin = self.cleaned_data.get('fecha_fin')
 
        #Comprobamos que no exista una promocion con ese nombre y que no sea mayor a 100 caracteres
        if len(nombre) > 100:
                self.add_error('nombre', 'El nombre no puede superar los 100 caracteres.')
                
        promocionNombre = Promocion.objects.filter(nombre=nombre).first()
        if(not promocionNombre is None
           ):
             if(not self.instance is None and promocionNombre.id == self.instance.id):
                 pass
             else:
                self.add_error('nombre','Ya existe una promoción con ese nombre')
                
        #Comprobamos que el campo descripción no tenga menos de 100 caracteres        
        if descripcion and len(descripcion) < 100:
            self.add_error('descripcion','Al menos debes indicar 100 caracteres')
                
        #Comprobamos que el campo descuento este entre 0 y 10  
        if descuento is not None and (descuento <= 0 or descuento > 11):
            self.add_error('descuento', 'El descuento debe ser un número entre 0 y 10.')
            
        # Validar que la fecha de inicio no sea mayor que la fecha de fin
        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            self.add_error('fecha_inicio', 'La fecha de inicio debe ser anterior a la fecha de fin.')
            
        # Validar que la fecha de fin no sea menor que la fecha de inicio
        if fecha_fin and fecha_inicio and fecha_inicio < fecha_fin:
            self.add_error('fecha_inicio', 'La fecha de fin debe ser posterior a la fecha de inicio.')
        
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data


class BusquedaAvanzadaPromocionForm(forms.Form):
    nombre_descripcion = forms.CharField(
        required=False, 
        label="Escriba el nombre o la descripción de una promocion",
        widget=forms.TextInput(attrs={"placeholder": "Nombre o descripción de la promocion"})
    )
    descuento = forms.IntegerField(
        required=False,
        label="Cantidad de descuento",
        widget=forms.NumberInput(attrs={"placeholder": "Cantidad de descuento"})
    )
    fecha_inicio = forms.DateField(
        label="Fecha Desde",
        required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
    )
    fecha_fin = forms.DateField(
        label="Fecha Hasta",
        required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
    )
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        required=False,
        label="Producto",
        empty_label="Seleccione un producto"
    )
    esta_activa = forms.ChoiceField(
        required=False,
        label="Estado de la promoción",
        choices=[
            ('', 'Seleccione un estado'),
            (True, 'Activa'),
            (False, 'Inactiva')
        ]
    )

    def clean(self):
        super().clean()
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        descuento_min = self.cleaned_data.get('descuento_min')
        descuento_max = self.cleaned_data.get('descuento_max')
        fecha_inicio = self.cleaned_data.get('fecha_desde')
        fecha_fin = self.cleaned_data.get('fecha_hasta')
        producto = self.cleaned_data.get('producto')
        esta_activa = self.cleaned_data.get('esta_activa')

        # Validación: al menos un campo debe estar lleno
        if not any([nombre, descripcion, descuento_min, descuento_max, fecha_inicio, fecha_fin, producto, esta_activa]):
            raise forms.ValidationError("Debe llenar al menos un campo del formulario para realizar la búsqueda avanzada.")

        # Validación: descuento_max no puede ser menor que descuento_min
        if descuento_min is not None and descuento_max is not None and descuento_max < descuento_min:
            self.add_error('descuento_min', "El descuento máximo no puede ser menor que el descuento mínimo.")
            self.add_error('descuento_max', "El descuento máximo no puede ser menor que el descuento mínimo.")

        # Validación: fecha_fin no puede ser menor que fecha_inicio
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            self.add_error('fecha_inicio', "La fecha fin no puede ser menor que la fecha inicio.")
            self.add_error('fecha_fin', "La fecha fin no puede ser menor que la fecha inicio.")

        return self.cleaned_data

    
