from catalogo.models import Categoria

TIENDA = {
    "nombre": "MotoMarket",
    "eslogan": "Tu próxima moto está a un clic. Compra en línea, agenda tu prueba de manejo y recíbela lista para rodar.",
    "direccion": "Carrera 27 # 36-14, Bucaramanga, Santander",
    "telefono": "+57 607 644 5566",
    "whatsapp": "573001234567",
    "whatsapp_visible": "+57 300 123 4567",
    "correo": "contacto@motomarket.co",
    "horario": "Lunes a sábado de 8:00 a. m. a 6:00 p. m.",
    "redes": [
        ("Instagram", "bi-instagram", "https://www.instagram.com/"),
        ("Facebook", "bi-facebook", "https://www.facebook.com/"),
        ("TikTok", "bi-tiktok", "https://www.tiktok.com/"),
        ("YouTube", "bi-youtube", "https://www.youtube.com/"),
    ],
}


def tienda(request):
    return {"tienda": TIENDA, "categorias_pie": Categoria.objects.all()}
