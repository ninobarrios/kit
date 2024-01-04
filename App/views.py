from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rembg import remove
import os
from datetime import datetime  
import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans
import cv2
import qrcode
from io import BytesIO
import base64


def paleta_colores(request):
    return render(request, 'paleta_colores.html')


def procesar_imagen(request):
    original_image_url = None
    processed_image_url = None

    try:
        if request.method == 'POST' and 'origen_imagen' in request.FILES:
            origen_imagen = request.FILES['origen_imagen']
                
            
            print("Formulario POST recibido y origen_imagen en request.FILES")

            # Guarda la imagen original
            original_image_path = default_storage.save('imagenes/imagen_entrada.jpg', ContentFile(origen_imagen.read()))
            original_image_url = default_storage.url(original_image_path)

            # Procesa la imagen
            with default_storage.open(original_image_path, 'rb') as i:
                input_data = i.read()
                output_data = remove(input_data)


            # Guarda la imagen procesada con el nombre único
            processed_image_path = default_storage.save(f'imagenes/imagen_resultado.png', ContentFile(output_data))
            processed_image_url = default_storage.url(processed_image_path)
        
    except Exception as e:
        print(f"Error al procesar la imagen: {e}")

    return render(request, 'procesar_imagen.html', {'original_image_url': original_image_url, 'processed_image_url': processed_image_url})


def paleta_colores(request):
    imagen_path = None
    numero = 0
    context = {'colores_hex': None}  # Inicializa el contexto
    if request.method == 'POST':
        numero = int(request.POST.get('numero', numero))

    try:
        if request.method == 'POST' and 'origen_imagen' in request.FILES:
            origen_imagen = request.FILES['origen_imagen']

            # Guarda la imagen original
            ruta_temporal = default_storage.save('imagenes/entrada.jpg', ContentFile(origen_imagen.read()))
            imagen_path = default_storage.url(ruta_temporal)

            # Procesamiento
            print("Ruta temporal:", ruta_temporal)
            print("Imagen path:", imagen_path)

            # Cargar la imagen usando la ruta directa (sin open)
            print("1")    
            imagen = cv2.imread(default_storage.path(ruta_temporal))
            print("2")    
            imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            print("3")

            # Procesamiento

            altura, ancho, _ = imagen.shape
            imagen_redimensionada = cv2.resize(imagen, (ancho // 2, altura // 2))
            píxeles = imagen_redimensionada.reshape((imagen_redimensionada.shape[0] * imagen_redimensionada.shape[1], 3))
            kmeans = MiniBatchKMeans(n_clusters=numero, n_init=3)  # Ajustar n_init
            kmeans.fit(píxeles)
            colores = kmeans.cluster_centers_.astype(int)

            # Convertir cada valor RGB a su representación hexadecimal
            colores_hex = ['#%02x%02x%02x' % (r, g, b) for (r, g, b) in colores]
            context = {'colores_hex': colores_hex}
            print (context)

    except Exception as e:
        print(f"Error al generar paleta de colores: {e}")

    return render(request, 'paleta_colores.html', context)




def mejorar_imagen(request):
    factor_aumento = 1  # Ajusta este valor según tus necesidades
    original_image_url = None
    processed_image_url = None

    if request.method == 'POST' and 'origen_imagen' in request.FILES:
        origen_imagen = request.FILES['origen_imagen']
        print("imagen guardada")

        # Guarda la imagen original
        original_image_path = default_storage.save('imagenes/ninolas.jpg', ContentFile(origen_imagen.read()))
        original_image_url = default_storage.url(original_image_path)
        print("imagen guardada")

        # Procesamiento
        print("1")    
        imagen = cv2.imread(default_storage.path(original_image_path))

        # Aplicar interpolación para aumentar la resolución
        imagen_aumentada = cv2.resize(imagen, None, fx=factor_aumento, fy=factor_aumento, interpolation=cv2.INTER_CUBIC)

        # Reducción de ruido mediante un filtro bilateral
        imagen_mejorada = cv2.bilateralFilter(imagen_aumentada, d=9, sigmaColor=75, sigmaSpace=75)

        # Guardar la imagen mejorada en formato PNG
        processed_image_path = default_storage.save('imagenes/ninolas_resultado.png', ContentFile(cv2.imencode('.png', imagen_mejorada)[1]))

        processed_image_url = default_storage.url(processed_image_path)

        print("mejora de imagen finalizada")

    return render(request, 'mejorar_imagen.html', {'original_image_url': original_image_url, 'processed_image_url': processed_image_url})


def generar_qr(request, enlace_web=None):
    nombre_archivo = "codigo_qr.png"
    processed_image_path = None
    imagen_html = ''  # Valor predeterminado
    imagen_base64 = ''  # Valor predeterminado

    if request.method == 'POST':
        # Obtener el enlace web del formulario
        enlace_web = request.POST.get('ingreso_link', enlace_web)
        print("link recibido", enlace_web)

        # Crear un objeto QRCode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        print("1")

        # Añadir la información al código QR
        qr.add_data(enlace_web)
        qr.make(fit=True)
        print("2")

        imagen_qr = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        imagen_qr.save(buffer, format="PNG")

        # Obtener los bytes de la imagen y codificarlos en base64
        imagen_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        # Construir la etiqueta de imagen HTML
        imagen_html = f'<img src="data:image/png;base64,{imagen_base64}" alt="Imagen QR">'

    return render(request, 'generar_qr.html', {'imagen_html': imagen_html, 'enlace_web': enlace_web, 'imagen_base64': imagen_base64})



def index(request):
    datos = {'mensaje': '¡Bienvenido a la página de inicio!'}
    return render(request, 'index.html', datos)



def pruebas(request, valor1=0, valor2=0):

    if request.method == 'POST':
        valor1 = int(request.POST.get('valor1', 0))
        valor2 = int(request.POST.get('valor2', 0))
        
    suma=valor1+valor2
    multiplicacion=valor1*valor2
    division=valor1/valor2
    resta=valor1-valor2

    datos = {
        'valor1':valor1,
        'valor2':valor2,
        'suma': suma,
        'multiplicacion': multiplicacion,
        'division':division,
        'resta': resta,
    }
    print(datos)

    return render(request, 'pruebas.html', datos)