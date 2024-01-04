from django.contrib import admin
from django.urls import path
from App.views import paleta_colores, procesar_imagen, mejorar_imagen, generar_qr, index, pruebas
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('paleta_colores/', paleta_colores, name='paleta_colores'),
    path('procesar_imagen/', procesar_imagen, name='procesar_imagen'),
    path('mejorar_imagen/', mejorar_imagen, name='mejorar_imagen'),
    path('generar_qr/', generar_qr, name='generar_qr'),
    path('index/', index, name='index'),
    path('pruebas/', pruebas, name='pruebas'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
