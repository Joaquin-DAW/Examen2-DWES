from django.urls import path
from .import views


urlpatterns = [
    path('', views.index, name='index'),
    
    path('promocion/create/',views.promocion_create,name='promocion_create'),
    path('promocion/',views.listar_promociones,name='listar_promociones'),
    path('promocion/buscar_avanzado/', views.promocion_buscar_avanzado, name='promocion_buscar_avanzado'),
    path('promocion/editar/<int:promocion_id>', views.promocion_editar, name='promocion_editar'),
    path('promocion/eliminar/<int:promocion_id>/', views.promocion_eliminar, name='promocion_eliminar'),
    
]