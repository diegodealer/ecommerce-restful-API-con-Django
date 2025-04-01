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
                messages.error(request, "Usuario no encontrado")
            else:
                messages.error(request, "Contraseña incorrecta")
    
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('login')

# Vistas de Productos
def busqueda_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    query = request.POST.get('nombre', '').strip() if request.method == 'POST' else ''
    productos = Producto.objects.filter(nombre__icontains=query) if query else Producto.objects.all()
    
    carrito_items = []
    if request.user.is_authenticated:
        carrito_items = Carrito.objects.filter(usuario=request.user).select_related('producto')
    
    return render(request, 'busqueda.html', {
        'productos': productos,
        'carrito': carrito_items,
        'query': query
    })

@login_required
def subir_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.vendedor = request.user
            producto.save()
            print("Producto subido con éxito.")
            return redirect('busqueda')
    else:
        form = ProductoForm()
    
    return render(request, 'subir_producto.html', {'form': form})

# Vistas de Carrito
@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get('cantidad', 1))
    
    item, created = Carrito.objects.get_or_create(
        usuario=request.user,
        producto=producto,
        defaults={'cantidad': cantidad}
    )
    
    if not created:
        item.cantidad += cantidad
        item.save()
    
    messages.success(request, f"'{producto.nombre}' agregado al carrito.")
    return redirect('busqueda')

@login_required
def modificar_item_carrito(request, id):
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
    item = get_object_or_404(Carrito, id=id, usuario=request.user)
    item.delete()
    messages.success(request, "Producto eliminado del carrito.")
    return redirect('busqueda')

# Vistas de Usuarios
@login_required
def modificar_usuario(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.email = request.POST.get('email', user.email)
        password = request.POST.get('password')
        
        try:
            if password:
                user.set_password(password)
            
            user.save()
            
            if password:
                user = authenticate(username=user.email, password=password)
                if user:
                    login(request, user)
            
            print(request, 'Perfil actualizado correctamente.')
            return redirect('busqueda')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {str(e)}')
    
    return render(request, 'modificar.html', {'user': request.user})

# Vista de Mapa
def iniciarMapa(request):
    lat = 28.6408325  
    lon = -106.1485902
    
    if request.method == 'POST' :
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        print(f"Latitud recibida en la vista: {lat}, Longitud recibida en la vista: {lon}")

        try:
            lat = float(request.POST.get('lat', lat))
            lon = float(request.POST.get('lon', lon))
            print(f"Coordenadas recibidas: {lat}, {lon}")
            Coordenadas.objects.create(
                latitud=lat,
                longitud=lon
            )
            messages.success(request, "Coordenadas guardadas correctamente.")
        except ValueError:
            messages.error(request, "Latitud o longitud inválidas.")
    return render(request, "mapas.html", {"lat": lat, "lon": lon})