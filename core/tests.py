from datetime import date, timedelta

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from carrito.models import ItemCarrito
from catalogo.models import Moto, Resena
from pedidos.models import Pedido
from pruebas.models import SolicitudPrueba
from usuarios.models import Usuario


class FlujoCompraTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("cargar_datos", verbosity=0)
        cls.cliente = Usuario.objects.create_user("ana", "ana@correo.com", "ClaveSegura123", first_name="Ana")
        cls.moto = Moto.objects.get(modelo="FZ 2.0")

    def setUp(self):
        self.client.force_login(self.cliente)

    def comprar(self, cantidad=1, tarjeta="4111111111111111"):
        for _ in range(cantidad):
            self.client.post(reverse("carrito:agregar", args=[self.moto.pk]))
        self.client.post(
            reverse("pedidos:checkout"),
            {"direccion_entrega": "Cra 27 #10-20", "ciudad": "Bucaramanga", "telefono": "3001234567"},
        )
        pedido = Pedido.objects.latest("fecha")
        self.client.post(
            reverse("pedidos:pagar", args=[pedido.pk]),
            {"metodo": "tarjeta", "titular": "Ana", "numero_tarjeta": tarjeta, "vencimiento": "12/28", "cvv": "123"},
        )
        pedido.refresh_from_db()
        return pedido

    def test_paginas_publicas(self):
        self.client.logout()
        for url in [reverse("core:inicio"), reverse("catalogo:lista"), self.moto.get_absolute_url(),
                    reverse("usuarios:login"), reverse("usuarios:registro")]:
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_registro_e_ingreso_con_correo(self):
        self.client.logout()
        r = self.client.post(reverse("usuarios:registro"), {
            "username": "luis", "first_name": "Luis", "last_name": "Pérez", "email": "luis@correo.com",
            "telefono": "", "ciudad": "", "acepta_datos": "on",
            "password1": "MotoMarket2026!", "password2": "MotoMarket2026!",
        })
        self.assertRedirects(r, reverse("core:inicio"))
        self.client.logout()
        self.assertTrue(self.client.login(username="luis@correo.com", password="MotoMarket2026!"))

    def test_filtros_del_catalogo(self):
        r = self.client.get(reverse("catalogo:lista"), {"q": "yamaha", "precio_max": 20_000_000})
        modelos = {m.modelo for m in r.context["motos"]}
        self.assertEqual(modelos, {"FZ 2.0", "NMAX 155"})

    def test_compra_aprobada_descuenta_stock(self):
        stock = self.moto.stock
        pedido = self.comprar(cantidad=2)
        self.assertEqual(pedido.estado, "pagado")
        self.assertEqual(pedido.total, self.moto.precio * 2)
        self.moto.refresh_from_db()
        self.assertEqual(self.moto.stock, stock - 2)
        self.assertFalse(ItemCarrito.objects.filter(carrito__usuario=self.cliente).exists())

    def test_pago_rechazado_no_descuenta_stock(self):
        stock = self.moto.stock
        pedido = self.comprar(tarjeta="4111111111110000")
        self.assertEqual(pedido.estado, "pendiente")
        self.assertEqual(pedido.pago.estado, "rechazado")
        self.moto.refresh_from_db()
        self.assertEqual(self.moto.stock, stock)

    def test_no_se_agrega_mas_que_el_stock(self):
        self.moto.stock = 1
        self.moto.save()
        url = reverse("carrito:agregar", args=[self.moto.pk])
        self.client.post(url)
        self.client.post(url)
        self.assertEqual(ItemCarrito.objects.get(carrito__usuario=self.cliente).cantidad, 1)

    def test_resena_solo_despues_de_comprar(self):
        url = reverse("catalogo:resenar", args=[self.moto.slug])
        self.client.post(url, {"calificacion": 5, "comentario": "Excelente"})
        self.assertFalse(Resena.objects.exists())
        self.comprar()
        self.client.post(url, {"calificacion": 5, "comentario": "Excelente"})
        self.assertEqual(Resena.objects.count(), 1)

    def test_solicitud_prueba_manejo(self):
        fecha = date.today() + timedelta(days=2)
        if fecha.weekday() == 6:
            fecha += timedelta(days=1)
        self.client.post(reverse("pruebas:solicitar", args=[self.moto.pk]),
                         {"fecha": fecha.isoformat(), "hora": "10:00", "licencia": "123456"})
        self.assertEqual(SolicitudPrueba.objects.filter(usuario=self.cliente).count(), 1)
        self.client.post(reverse("pruebas:solicitar", args=[self.moto.pk]),
                         {"fecha": date.today().isoformat(), "hora": "10:00", "licencia": "123456"})
        self.assertEqual(SolicitudPrueba.objects.count(), 1)

    def test_pedidos_de_otro_usuario_no_son_visibles(self):
        pedido = self.comprar()
        otro = Usuario.objects.create_user("otro", "otro@correo.com", "ClaveSegura123")
        self.client.force_login(otro)
        self.assertEqual(self.client.get(reverse("pedidos:detalle", args=[pedido.pk])).status_code, 404)

    def test_reporte_solo_para_administradores(self):
        url = reverse("core:reporte_ventas")
        self.assertEqual(self.client.get(url).status_code, 302)
        self.comprar()
        admin = Usuario.objects.create_superuser("admin", "admin@correo.com", "ClaveSegura123")
        self.client.force_login(admin)
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context["unidades"], 1)
