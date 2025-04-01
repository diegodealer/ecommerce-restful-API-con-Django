from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveBigIntegerField(default=1)
    imagen = models.ImageField(upload_to='productos', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveBigIntegerField(default=1) 

    class Meta:
        unique_together = ('usuario', 'producto')

    def __str__(self):
        return f'{self.usuario} - {self.producto}'

class Coordenadas(models.Model):
    latitud = models.FloatField()
    longitud = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)  
    
    def __str__(self):
        return f"Lat: {self.latitud}, Lon: {self.longitud}"