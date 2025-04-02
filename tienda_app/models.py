from django.contrib.auth.models import AbstractUser
from django.db import models


"""
En este archivo agregamos o creamos nuestras clases basadas en la libreria models para insertar
tablas en la base de datos, en este caso creamos un usuario customizado con la clase AbstractUser, 
clase Producto, Carrito y Coordenadas, para que los cambios se reflejen se debe ejecutar 
'py manage.py migrate ' y 'py manage.py'  para que los datos se reflejen en la base de datos.
"""
# Create your models here.
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30) # atributo nombre
    email = models.EmailField(unique=True) # atributo email  
    
# Clase producto que hereda de models
class Producto(models.Model):
    nombre = models.CharField(max_length=50)  # atributo char nombre con limite de 50 caracteres
    descripcion = models.CharField(max_length=200) # atributo descripcion con limite de 200 caracteres
    precio = models.DecimalField(max_digits=10, decimal_places=2) # atributo decimal precio con limite de 10 digitos y 2 decimales
    cantidad = models.PositiveBigIntegerField(default=1) # atributo BigInteger con default 1
    imagen = models.ImageField(upload_to='productos', null=True, blank=True) 
    # Crea un atributo de tipo ImageField en el modelo que permite almacenar imágenes.
    # - 'upload_to='productos'' indica el directorio dentro de 'MEDIA_ROOT' donde se guardarán las imágenes.
    # - 'null=True' permite que el campo sea opcional a nivel de base de datos.
    # - 'blank=True' hace que el campo sea opcional a nivel de formulario.

    def __str__(self):
        # Método que define cómo se mostrará una instancia del modelo como cadena de texto.
        return self.nombre
        # Devuelve el nombre del producto como representación del objeto cuando se imprime o muestra.

class Carrito(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # Relación con el usuario; se elimina si el usuario es eliminado.
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    # Relación con un producto; se elimina si el producto es eliminado.
    cantidad = models.PositiveBigIntegerField(default=1)
    # Cantidad del producto en el carrito, debe ser un número positivo.

    class Meta:
        unique_together = ('usuario', 'producto')
        # Garantiza que no haya duplicados de un mismo producto por usuario.

    def __str__(self):
        return f'{self.usuario} - {self.producto}'
        # Representa el carrito como usuario-producto.

class Coordenadas(models.Model):
    latitud = models.FloatField()
    # Almacena la latitud como número decimal.
    longitud = models.FloatField()
    # Almacena la longitud como número decimal.
    fecha = models.DateTimeField(auto_now_add=True)
    # Guarda la fecha y hora automáticamente al crear el registro.

    def __str__(self):
        return f"Lat: {self.latitud}, Lon: {self.longitud}"
        # Representa las coordenadas como texto legible.