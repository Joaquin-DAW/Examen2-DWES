from django.db import models

# Create your models here.

class Usuario(models.Model):    
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    puede_tener_promociones = models.BooleanField()

    def __str__(self):
        return self.nombre

class Promocion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=200)
    descuento = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    esta_activa = models.BooleanField(default=True)
    usuario = models.ManyToManyField(Usuario, related_name="promociones")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="promociones")
    
    def __str__(self):
        return self.nombre