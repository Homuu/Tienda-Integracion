from django.test import TestCase
from tienda.models import Producto
from django.urls import reverse

class CarritoTests(TestCase):
    def setUp(self):
        self.producto1 = Producto.objects.create(nombre="Producto A", precio=1000)
        self.producto2 = Producto.objects.create(nombre="Producto B", precio=2000)

    def test_producto_creado_correctamente(self):
        self.assertEqual(self.producto1.nombre, "Producto A")
        self.assertEqual(self.producto1.precio, 1000)

    def test_listado_productos(self):
        response = self.client.get(reverse('index'))  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Producto A")
        self.assertContains(response, "Producto B")

    def test_carrito_inicia_vacio(self):
        session = self.client.session
        self.assertFalse('carrito' in session)

    def test_agregar_producto_a_carrito(self):
        session = self.client.session
        session['carrito'] = {}
        session.save()

        carrito = session['carrito']
        carrito[str(self.producto1.id)] = {'cantidad': 1}
        session['carrito'] = carrito
        session.save()

        self.assertIn(str(self.producto1.id), session['carrito'])
        self.assertEqual(session['carrito'][str(self.producto1.id)]['cantidad'], 1)

    def test_incrementar_cantidad_producto(self):
        session = self.client.session
        session['carrito'] = {str(self.producto1.id): {'cantidad': 1}}
        session.save()

        carrito = session['carrito']
        carrito[str(self.producto1.id)]['cantidad'] += 1
        session['carrito'] = carrito
        session.save()

        self.assertEqual(session['carrito'][str(self.producto1.id)]['cantidad'], 2)

    def test_disminuir_cantidad_producto(self):
        session = self.client.session
        session['carrito'] = {str(self.producto1.id): {'cantidad': 2}}
        session.save()

        carrito = session['carrito']
        carrito[str(self.producto1.id)]['cantidad'] -= 1
        session['carrito'] = carrito
        session.save()

        self.assertEqual(session['carrito'][str(self.producto1.id)]['cantidad'], 1)

    def test_quitar_producto_si_cantidad_llega_a_cero(self):
        session = self.client.session
        session['carrito'] = {str(self.producto1.id): {'cantidad': 1}}
        session.save()

        carrito = session['carrito']
        carrito.pop(str(self.producto1.id))
        session['carrito'] = carrito
        session.save()

        self.assertNotIn(str(self.producto1.id), session['carrito'])

    def test_total_del_carrito(self):
        session = self.client.session
        session['carrito'] = {
            str(self.producto1.id): {'cantidad': 2},
            str(self.producto2.id): {'cantidad': 1}
        }
        session.save()

        total = (
            self.producto1.precio * session['carrito'][str(self.producto1.id)]['cantidad'] +
            self.producto2.precio * session['carrito'][str(self.producto2.id)]['cantidad']
        )
        self.assertEqual(total, 4000)

    def test_finalizar_compra_redirecciona(self):
        response = self.client.post(reverse('pago'), {'total': 4000})
        self.assertEqual(response.status_code, 302)  # espera redirección a Webpay

    def test_producto_con_imagen(self):
        self.producto1.imagen = "productos/imagen.jpg"
        self.producto1.save()
        self.assertTrue("imagen.jpg" in self.producto1.imagen.name)
