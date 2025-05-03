from django.shortcuts import render, redirect
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType 
import random
import string


def pago(request):
    if request.method == 'POST':
        total = request.POST.get('total')
        if not total:
            return render(request, 'error.html', {'mensaje': 'Total no proporcionado'})

        # Configurar Transbank en entorno de prueba
        options = WebpayOptions(
            commerce_code="597055555532",
            api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
            integration_type=IntegrationType.TEST
        )

        # Crear transacción con valores básicos de prueba
        buy_order = "orden_" + str('22')
        session_id = request.session.session_key or 'session123'
        amount = int(float(total))
        return_url = request.build_absolute_uri('/retorno/')

        response = Transaction(options).create(buy_order, session_id, amount, return_url)

        # Redirigir a Transbank
        return redirect(response['url'] + '?token_ws=' + response['token'])
    else:
        return render(request, 'rechazo.html', {'mensaje': 'Método no permitido'})

# Vista para el retorno de Webpay (cuando el pago es exitoso o fallido)
def retorno(request):
    token = request.GET.get("token_ws")
    if token:
        options = WebpayOptions(
            commerce_code="597055555532",
            api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
            integration_type=IntegrationType.TEST
        )

        response = Transaction(options).commit(token)

        if response['status'] == 'AUTHORIZED':
            return render(request, 'retorno.html', {'respuesta': response})
        else:
            return render(request, 'rechazo.html', {'respuesta': response})
    else:
        return render(request, 'rechazo.html', {'mensaje': 'Token no recibido'})

# Vista de confirmación de pago (transacción exitosa)
def confirmacion(request):
    return render(request, 'tienda/confirmacion.html')

# Vista de rechazo de pago (cuando el pago falla)
def rechazo(request):
    return render(request, 'tienda/rechazo.html')


from django.shortcuts import render
from .models import Producto
import locale

# Configurar la localización para CLP
locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')  # Puede variar según tu entorno

def index(request):
    # Obtener todos los productos
    productos = Producto.objects.all()
    
    # Formatear el precio en CLP
    for producto in productos:
        # Convertir el precio a formato CLP
        producto.precio_formateado = locale.currency(producto.precio, grouping=True)
    
    return render(request, 'tienda/index.html', {'productos': productos})