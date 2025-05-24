from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout,  get_user_model
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from tienda_app.models import CustomUser, Carrito, Producto, Coordenadas
from django.contrib import messages
from .forms import ProductoForm 

# Vistas de Autenticación
def registro(request):

    """
    registro maneja el registro de nuevos usuarios, esta funcion 
    tambien se encarga de verificar si los datos requeridos estan presentes, 
    si hay datos repetidos, usuarios repetidos o si no se ingresa nada de datos en el
    forms de html.
    """
    if request.method == 'POST':
        nombre = request.POST.get('first_name', '').strip()
        email = request.POST.get('email', '').strip().lower() 
        contrasena = request.POST.get('password', '').strip()

        # Validaciones básicas
        if not all([nombre, email, contrasena]):
            messages.error(request, "Todos los campos son obligatorios")
            return render(request, 'registro.html')

        # Validación de email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Por favor ingresa un email válido")
            return render(request, 'registro.html')

        # Verificar si el email ya existe
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            messages.error(request, "Este email ya está registrado")
            return render(request, 'registro.html')

        try:
            # Crear usuario usando el email como username
            CustomUser = User.objects.create_user(
                username=email,  # Usamos el email como username
                first_name=nombre,
                email=email,
                password=contrasena
            )
            messages.success(request, "¡Registro exitoso! Por favor inicia sesión")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error al registrar: {str(e)}")
            # Log del error para diagnóstico
            import logging
            logging.error(f"Error en registro: {str(e)}", exc_info=True)
    return render(request, 'registro.html')

def login_view(request):

    """
    La funcion login view verifica que los datos ingresados sean correctos
    y esten registrados en la base de datos, en este caso username y password, en caso de 
    que sean incorrectos los datos comparados se enviara un mensaje de erro, por ultimo verifica si el 
    usuario este registrado y exista en casi de que no exista tambien enviara un mensaje de advertencia
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, "Usuario y contraseña son requeridos")
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenido, {user.first_name}!")
            return redirect('busqueda')
        else:
            # Verifica si el usuario existe 
            User = get_user_model()
            if not User.objects.filter(username=username).exists():
                messages.error(request, "Contraseña o usuario incorrecto")
            else:
                messages.error(request, "Contraseña o usuario incorrecto")
    
    return render(request, 'login.html')

@login_required
def logout_view(request):
    """
    La funcion logout envia una peticion para cerrar la sesion manda un mensaje de que se ha cerrado sesion
    y te redirije al login
    """
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('login')

# Vistas de Productos
def busqueda_view(request):
    # Permite buscar productos por nombre.
    # Muestra todos los productos si no hay búsqueda y el contenido del carrito del usuario autenticado.
    if not request.user.is_authenticated:
        return redirect('login')  # Redirige si el usuario no está autenticado.
    
    query = request.POST.get('nombre', '').strip() if request.method == 'POST' else ''
    productos = Producto.objects.filter(nombre__icontains=query) if query else Producto.objects.all()
    carrito_items = Carrito.objects.filter(usuario=request.user).select_related('producto') if request.user.is_authenticated else []
    
    return render(request, 'busqueda.html', {'productos': productos, 'carrito': carrito_items, 'query': query})

@login_required
def subir_producto(request):
    # Permite a usuarios autenticados subir nuevos productos con imágenes.
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.vendedor = request.user
            producto.save()  # Guarda el nuevo producto asociado al usuario.
            print("Producto subido con éxito.")
            return redirect('busqueda')
    else:
        form = ProductoForm()
    
    return render(request, 'subir_producto.html', {'form': form})

# Vistas de Carrito
@login_required
def agregar_al_carrito(request, producto_id):
    # Agrega un producto al carrito del usuario o incrementa su cantidad.
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get('cantidad', 1))
    item, created = Carrito.objects.get_or_create(
        usuario=request.user, producto=producto, defaults={'cantidad': cantidad}
    )
    if not created:
        item.cantidad += cantidad
        item.save()
    messages.success(request, f"'{producto.nombre}' agregado al carrito.")
    return redirect('busqueda')

# vista modificar item del carrito
@login_required
def modificar_item_carrito(request, id):
    # Modifica la cantidad de un producto en el carrito o lo elimina si la cantidad es cero.
    item = get_object_or_404(Carrito, id=id, usuario=request.user)
    if request.method == 'POST':
        nueva_cantidad = int(request.POST.get('cantidad', 1))
        if nueva_cantidad > 0:
            item.cantidad = nueva_cantidad
            item.save()
            messages.success(request, "Cantidad actualizada.")
        else:
            item.delete()
            messages.success(request, "Producto eliminado.")
    return redirect('busqueda')

@login_required
def eliminar_producto_carrito(request, id):
    # Elimina un producto específico del carrito del usuario.
    item = get_object_or_404(Carrito, id=id, usuario=request.user)
    item.delete()
    messages.success(request, "Producto eliminado del carrito.")
    return redirect('busqueda')

# Vistas de Usuarios
@login_required
def modificar_usuario(request):

    """
    Esta funcion Permite a los usuarios autenticados modificar su información personal.
    - Actualiza nombre, email y contraseña según lo proporcionado en el formulario.
    - Si se actualiza la contraseña, autentica nuevamente al usuario para mantener la sesión activa.
    """
    if request.method == 'POST': # Verifica si bel formulario fue enviado
        user = request.user # obtiene el usuario actualmente autenticado 

        #actualiza los valores proporcionados por el usuario 
        user.first_name = request.POST.get('first_name', user.first_name)
        user.email = request.POST.get('email', user.email)
        password = request.POST.get('password')
        
        try:
            if password:
                user.set_password(password) # Guarda la contraseña del usuario 
            
            user.save() # Guarda los cambios realizados en la base de datos 

            # Si se cambió la contraseña, autentica nuevamente al usuario.

            if password:
                user = authenticate(username=user.email, password=password)
                if user:
                    login(request, user)

            # Inicia sesión nuevamente con las nuevas credenciales.
            
            # Muestra un mensaje de éxito y redirige a la vista de búsqueda.
            
            print(request, 'Perfil actualizado correctamente.')
            return redirect('busqueda')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {str(e)}')
    
    # En caso de error, muestra un mensaje y lo registra.

    # Renderiza la página de modificación del perfil con los datos actuales del usuario.
    return render(request, 'modificar.html', {'user': request.user})

    
# Vista de Mapa
def iniciarMapa(request):
    """Esta funcion renderiza una vista del mapa por default"""
    lat = 28.6408325  
    lon = -106.1485902
    # inicializa el mapa con dos coordenadas por default
    
    if request.method == 'POST' :
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        print(f"Latitud recibida en la vista: {lat}, Longitud recibida en la vista: {lon}")

        # Recibe nuevas coordenadas a traves del metodo post y las guarda en la base de datos 
        # si se ingresaron correctamente las imprime 

        try:
            lat = float(request.POST.get('lat', lat))
            lon = float(request.POST.get('lon', lon))
            print(f"Coordenadas recibidas: {lat}, {lon}")
            Coordenadas.objects.create(
                latitud=lat,
                longitud=lon
            )
            messages.success(request, "Coordenadas guardadas correctamente.")
            # Al ingresar las coordenadas las evalua en un try en caso de haberlas recibidas e insertado correctamente
            # En la base de datos esta se guardan en un nuevo objeto y envia un mensajo de success diciendo que se 
            # Insertaron correctamente 
        except ValueError:
            messages.error(request, "Latitud o longitud inválidas.")
            # Se envia un mensaje de error en caso de que las coordenadas no sean validas
    return render(request, "mapas.html", {"lat": lat, "lon": lon})
    # Renderiza la pagina con las coordenadas ingresadas. 
