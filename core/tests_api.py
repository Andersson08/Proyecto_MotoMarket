from django.core.management import call_command
from django.test import Client, TestCase

from catalogo.models import Categoria, Moto
from usuarios.models import Usuario


class ApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("cargar_datos", verbosity=0)
        Usuario.objects.create_user("jefe", "jefe@correo.com", "ClaveSegura123", is_staff=True)
        Usuario.objects.create_user("ana", "ana@correo.com", "ClaveSegura123")

    def setUp(self):
        self.navegador = Client(enforce_csrf_checks=True)

    def token(self):
        return self.navegador.get("/api/auth/csrf/").json()["csrfToken"]

    def entrar(self, usuario="jefe"):
        respuesta = self.navegador.post(
            "/api/auth/login/",
            {"usuario": usuario, "clave": "ClaveSegura123"},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.token(),
        )
        self.assertEqual(respuesta.status_code, 200)
        return respuesta.json()

    def test_catalogo_publico_filtra_por_categoria(self):
        categoria = Categoria.objects.first()
        motos = self.navegador.get(f"/api/motos/?categoria={categoria.id}").json()
        self.assertTrue(motos)
        self.assertTrue(all(moto["categoria"] == categoria.id for moto in motos))

    def test_login_sin_token_csrf_es_rechazado(self):
        respuesta = self.navegador.post(
            "/api/auth/login/",
            {"usuario": "jefe", "clave": "ClaveSegura123"},
            content_type="application/json",
        )
        self.assertEqual(respuesta.status_code, 403)

    def test_crear_moto_sin_token_csrf_es_rechazado(self):
        self.entrar()
        respuesta = self.navegador.post(
            "/api/categorias/", {"nombre": "Prueba"}, content_type="application/json"
        )
        self.assertEqual(respuesta.status_code, 403)
        self.assertFalse(Categoria.objects.filter(nombre="Prueba").exists())

    def test_visitante_no_puede_crear(self):
        respuesta = self.navegador.post(
            "/api/categorias/",
            {"nombre": "Prueba"},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.token(),
        )
        self.assertIn(respuesta.status_code, (401, 403))

    def test_cliente_no_admin_no_puede_crear(self):
        self.assertFalse(self.entrar("ana")["es_admin"])
        respuesta = self.navegador.post(
            "/api/categorias/",
            {"nombre": "Prueba"},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.token(),
        )
        self.assertEqual(respuesta.status_code, 403)

    def test_crud_completo_de_moto_con_html_limpio(self):
        self.entrar()
        token = self.token()
        datos = {
            "marca": Moto.objects.first().marca_id,
            "categoria": Categoria.objects.first().id,
            "modelo": "<script>alert('xss')</script>Raptor",
            "anio": 2026,
            "precio": 15000000,
            "stock": 3,
            "imagen_url": "https://example.com/raptor.webp",
        }
        creada = self.navegador.post(
            "/api/motos/", datos, content_type="application/json", HTTP_X_CSRFTOKEN=token
        )
        self.assertEqual(creada.status_code, 201)
        moto = creada.json()
        self.assertEqual(moto["modelo"], "alert('xss')Raptor")
        self.assertEqual(moto["imagen"], "https://example.com/raptor.webp")

        editada = self.navegador.patch(
            f"/api/motos/{moto['id']}/", {"precio": 14000000}, content_type="application/json", HTTP_X_CSRFTOKEN=token
        )
        self.assertEqual(editada.json()["precio"], "14000000")

        borrada = self.navegador.delete(f"/api/motos/{moto['id']}/", HTTP_X_CSRFTOKEN=token)
        self.assertEqual(borrada.status_code, 204)
        self.assertFalse(Moto.objects.filter(pk=moto["id"]).exists())

    def test_no_se_elimina_categoria_con_motos(self):
        self.entrar()
        categoria = Moto.objects.first().categoria
        respuesta = self.navegador.delete(f"/api/categorias/{categoria.id}/", HTTP_X_CSRFTOKEN=self.token())
        self.assertEqual(respuesta.status_code, 409)

    def test_logout_cierra_la_sesion(self):
        self.entrar()
        self.navegador.post("/api/auth/logout/", HTTP_X_CSRFTOKEN=self.token())
        self.assertFalse(self.navegador.get("/api/auth/sesion/").json()["autenticado"])
