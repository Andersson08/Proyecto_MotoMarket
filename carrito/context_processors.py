from .models import ItemCarrito


def carrito(request):
    if not request.user.is_authenticated:
        return {"carrito_cantidad": 0}
    cantidades = ItemCarrito.objects.filter(carrito__usuario=request.user).values_list("cantidad", flat=True)
    return {"carrito_cantidad": sum(cantidades)}
