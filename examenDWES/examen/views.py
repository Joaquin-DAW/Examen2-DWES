from django.shortcuts import render,redirect
from django.db.models import Q, Avg
from datetime import date
from .models import *
from .forms import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html') 


#Listado de promociones
def listar_promociones(request):
    promociones = Promocion.objects.prefetch_related("usuario","producto").all()
    return render(request, "promocion/lista.html", {"promociones": promociones})

#Creación de promocion.
def promocion_create(request):
    if request.method == "POST":
        formulario = PromocionModelForm(request.POST)
        if formulario.is_valid():
            try:
                # Guarda la promocion en la base de datos
                formulario.save()
                messages.success(request, "La promocion se ha creado correctamente.")
                return redirect("promocion_lista")
            except Exception as error:
                print(error)
    else:
        formulario = PromocionModelForm()
          
    return render(request, 'promocion/create.html',{"formulario":formulario}) 

#Busqueda avanzada de promocion
def promocion_buscar_avanzado(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaPromocionForm(request.GET)

        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            QSpromociones = Promocion.objects.all()

            # Campos del formulario
            nombre_descripcion = formulario.cleaned_data.get('nombre_descripcion')
            descuento = formulario.cleaned_data.get('descuento')
            fecha_inicio = formulario.cleaned_data.get('fecha_inicio')
            fecha_fin = formulario.cleaned_data.get('fecha_fin')
            producto = formulario.cleaned_data.get('producto')
            esta_activa = formulario.cleaned_data.get('esta_activa')
            usuarios = formulario.cleaned_data.get('usuarios')

            # Filtro por nombre y descripción
            if nombre_descripcion:
                QSpromociones = QSpromociones.filter(
                    Q(nombre__icontains=nombre_descripcion) | Q(descripcion__icontains=nombre_descripcion)
                )
                mensaje_busqueda += f"Nombre o descripción contienen: {nombre_descripcion}\n"

            # Filtro por descuento
            if descuento:
                QSpromociones = QSpromociones.filter(descuento__gte=descuento)
                mensaje_busqueda += f"Descuento mayor o igual a: {descuento}\n"

            # Filtro por rango de fechas
            if fecha_inicio:
                QSpromociones = QSpromociones.filter(fecha_fin__gte=fecha_inicio)
                mensaje_busqueda += f"Fecha fin mayor o igual a: {fecha_inicio}\n"
            if fecha_fin:
                QSpromociones = QSpromociones.filter(fecha_fin__lte=fecha_fin)
                mensaje_busqueda += f"Fecha fin menor o igual a: {fecha_fin}\n"

            # Filtro por producto
            if producto:
                QSpromociones = QSpromociones.filter(producto=producto)
                mensaje_busqueda += f"Producto: {producto}\n"

            # Filtro por usuarios
            if usuarios:
                QSpromociones = QSpromociones.filter(usuario__in=usuarios)
                mensaje_busqueda += "Promociones asociadas a los usuarios seleccionados.\n"

            # Filtro por estado activo
            if esta_activa:
                QSpromociones = QSpromociones.filter(esta_activa=bool(esta_activa))
                mensaje_busqueda += f"Estado: {'Activa' if bool(esta_activa) else 'Inactiva'}\n"

            promociones = QSpromociones.distinct()

            return render(request, 'promocion/lista_busqueda.html', {
                "promociones": promociones,
                "mensaje_busqueda": mensaje_busqueda,
            })
    else:
        formulario = BusquedaAvanzadaPromocionForm()

    return render(request, 'promocion/busqueda_avanzada.html', {"formulario": formulario})

#Editar de promocion.
def promocion_editar(request, promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    formulario = PromocionModelForm(datosFormulario, instance=promocion)
    
    if request.method == "POST":
        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, f'Se ha editado la promocion {formulario.cleaned_data.get("titulo")} correctamente.')
                return redirect('listar_promociones')  
            except Exception as error:
                print(error)
                
    return render(request, 'promocion/actualizar.html', {"formulario": formulario, "promocion": promocion})

#Eliminar de Promocion
def promocion_eliminar(request, promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)
    
    try:
        promocion.delete()
        messages.success(request, f"Se ha eliminado la promocion '{promocion.titulo}' correctamente.")
    except Exception as error:
        print(error)
        
    return redirect('listar_promociones')
