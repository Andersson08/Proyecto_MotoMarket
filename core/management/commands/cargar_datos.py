from django.core.management.base import BaseCommand

from catalogo.models import Categoria, ImagenMoto, Marca, Moto

MARCAS = {
    "Yamaha": "Japón",
    "Honda": "Japón",
    "Suzuki": "Japón",
    "Kawasaki": "Japón",
    "KTM": "Austria",
    "Bajaj": "India",
    "Royal Enfield": "India",
    "Super Soco": "China",
}

CATEGORIAS = {
    "Urbana": "Motos económicas y livianas para moverse por la ciudad.",
    "Naked": "Motos deportivas sin carenado, cómodas y ágiles.",
    "Deportiva": "Motos con carenado pensadas para velocidad y desempeño.",
    "Scooter": "Motos automáticas, prácticas y fáciles de manejar.",
    "Clásica": "Estilo retro con tecnología actual.",
    "Eléctrica": "Cero emisiones y bajo costo de uso.",
}

MOTOS = [
    ("Yamaha", "FZ 2.0", "Naked", 2026, 149, 12.2, "gasolina", "manual", "Rojo", 11_900_000, 8, True,
     "La naked más vendida de su segmento: motor de 149 cc con inyección electrónica, freno de disco delantero y bajo consumo."),
    ("Yamaha", "MT-03", "Naked", 2026, 321, 41.4, "gasolina", "manual", "Amarillo", 29_990_000, 4, True,
     "Bicilíndrica de 321 cc del lado oscuro de Japón: frenos ABS, tablero digital y posición de manejo erguida."),
    ("Yamaha", "NMAX 155", "Scooter", 2026, 155, 15.1, "gasolina", "automatica", "Negro mate", 15_490_000, 6, False,
     "Scooter premium con motor Blue Core, ABS de doble canal, control de tracción y espacio bajo el asiento."),
    ("Honda", "CB 190R", "Naked", 2026, 184, 15.5, "gasolina", "manual", "Repsol", 11_290_000, 7, True,
     "Motor de 184 cc confiable y económico, suspensión delantera invertida y diseño agresivo."),
    ("Honda", "Navi 110", "Scooter", 2026, 109, 8.0, "gasolina", "automatica", "Rojo", 6_590_000, 10, False,
     "Divertida, económica y automática. Ideal para tu primera moto en la ciudad."),
    ("Suzuki", "Gixxer 150", "Naked", 2026, 155, 14.0, "gasolina", "manual", "Azul/Negro", 10_590_000, 5, False,
     "Motor SEP de 155 cc con inyección, frenos de disco y excelente relación precio–desempeño."),
    ("Suzuki", "GN 125F", "Urbana", 2026, 124, 11.0, "gasolina", "manual", "Negro", 6_990_000, 12, False,
     "La clásica de trabajo: resistente, fácil de mantener y con un consumo muy bajo."),
    ("KTM", "390 Duke", "Naked", 2026, 399, 44.0, "gasolina", "manual", "Blanco/Naranja", 31_990_000, 3, True,
     "Monocilíndrica de 399 cc, ABS con modo supermoto, control de tracción y pantalla TFT."),
    ("Kawasaki", "Ninja 400", "Deportiva", 2026, 399, 45.0, "gasolina", "manual", "Verde lima", 36_490_000, 2, True,
     "Deportiva bicilíndrica ligera, con embrague asistido y deslizante y frenos ABS."),
    ("Royal Enfield", "Classic 350", "Clásica", 2026, 349, 20.2, "gasolina", "manual", "Granate", 21_990_000, 4, False,
     "Diseño retro inspirado en 1948, motor J-series suave y ABS de doble canal."),
    ("Bajaj", "Pulsar NS 200", "Naked", 2026, 199, 24.5, "gasolina", "manual", "Amarillo", 12_490_000, 9, False,
     "Motor de 199 cc refrigerado por líquido, suspensión invertida y ABS de un canal."),
    ("Super Soco", "TC Max", "Eléctrica", 2026, 0, 6.7, "electrica", "automatica", "Negro", 15_900_000, 3, False,
     "Eléctrica de 5 kW con autonomía de hasta 110 km, batería de litio extraíble y carga en casa."),
]

IA = "Imagen ilustrativa generada con IA (Gemini)"

FOTOS = {
    "FZ 2.0": "fz20",
    "MT-03": "mt03",
    "NMAX 155": "nmax155",
    "Gixxer 150": "gixxer150",
    "CB 190R": "cb190r",
    "Navi 110": "navi",
    "GN 125F": "gn125",
    "390 Duke": "duke390",
    "Ninja 400": "ninja400",
    "Classic 350": "classic350",
    "Pulsar NS 200": "pulsarns200",
    "TC Max": "tcmax",
}


class Command(BaseCommand):
    help = "Carga marcas, categorías y motos de ejemplo (se puede ejecutar varias veces)."

    def handle(self, *args, **options):
        marcas = {n: Marca.objects.get_or_create(nombre=n, defaults={"pais_origen": p})[0] for n, p in MARCAS.items()}
        categorias = {
            n: Categoria.objects.get_or_create(nombre=n, defaults={"descripcion": d})[0] for n, d in CATEGORIAS.items()
        }
        creadas = 0
        for (marca, modelo, cat, anio, cc, hp, comb, trans, color, precio, stock, destacada, desc) in MOTOS:
            moto, creada = Moto.objects.get_or_create(
                marca=marcas[marca],
                modelo=modelo,
                anio=anio,
                defaults=dict(
                    categoria=categorias[cat], cilindraje=cc, potencia_hp=hp, combustible=comb,
                    transmision=trans, color=color, precio=precio, stock=stock, destacada=destacada,
                    descripcion=desc,
                ),
            )
            creadas += creada
            if modelo in FOTOS:
                ruta = f"img/motos/final/{FOTOS[modelo]}.webp"
                if not moto.imagenes.filter(url=ruta).exists():
                    moto.imagenes.filter(url__startswith="img/motos/").delete()
                    ImagenMoto.objects.create(moto=moto, url=ruta, credito=IA, principal=True)
        self.stdout.write(self.style.SUCCESS(f"Listo: {creadas} motos nuevas, {Moto.objects.count()} en total."))
