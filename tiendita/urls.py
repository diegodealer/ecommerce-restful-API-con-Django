from django.contrib import admin
from django.urls import path
from tienda_app import views
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', lambda request: redirect('registro'), name="inicio"),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('busqueda/', views.busqueda_view, name='busqueda'),
    path('modificar_usuario/', views.modificar_usuario, name='modificar_usuario'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('modificar_item_carrito/<int:id>/', views.modificar_item_carrito, name='modificar_item_carrito'),
    path('eliminar_producto/<int:id>/', views.eliminar_producto_carrito, name='eliminar_producto'),
    path('subir_producto/', views.subir_producto, name='subir_producto'),
    path('mapas/', views.iniciarMapa, name='mapas'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
