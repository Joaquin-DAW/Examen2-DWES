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
            "esta_activa": forms.CheckboxInput(),  # Widget para booleano
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
        esta_activa = self.cleaned_data.get('esta_activa')
 
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
        if fecha_inicio and fecha_fin and fecha_inicio >= fecha_fin:
            self.add_error('fecha_inicio', 'La fecha de inicio debe ser anterior a la fecha de fin.')

        
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data


class BusquedaAvanzadaPromocionForm(forms.Form):
    nombre_descripcion = forms.CharField(
        required=False,
        label="Nombre o descripción",
        widget=forms.TextInput(attrs={"placeholder": "Nombre o descripción de la promoción"})
    )
    descuento = forms.IntegerField(
        required=False,
        label="Descuento a buscar",
        widget=forms.NumberInput(attrs={"placeholder": "Descuento a buscar"})
    )
    fecha_inicio = forms.DateField(
        label="Fecha desde",
        required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
    )
    fecha_fin = forms.DateField(
        label="Fecha hasta",
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
    usuarios = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.all(),
        required=False,
        label="Usuarios",
        widget=forms.SelectMultiple(attrs={"placeholder": "Seleccione uno o más usuarios"})
    )

    def clean(self):
        super().clean()
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_fin = self.cleaned_data.get('fecha_fin')

        # Validación: fecha_fin no puede ser menor que fecha_inicio
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            self.add_error('fecha_inicio', "La fecha fin no puede ser menor que la fecha inicio.")
            self.add_error('fecha_fin', "La fecha fin no puede ser menor que la fecha inicio.")

        return self.cleaned_data