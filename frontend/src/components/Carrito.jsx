import { pesos } from "../carrito.js";

export default function Carrito({ carrito }) {
  const { items, cambiarCantidad, quitar, vaciar, total, unidades } = carrito;

  return (
    <>
      <section className="titular">
        <p className="titular__sobre">Tu compra</p>
        <h1 className="titular__titulo">Carrito</h1>
        <p className="titular__resumen">
          {unidades} {unidades === 1 ? "unidad" : "unidades"}
        </p>
      </section>

      {!items.length ? (
        <p className="estado">
          El carrito está vacío. <a href="#/">Ver el catálogo</a>
        </p>
      ) : (
        <div className="carrito">
          <ul className="carrito__lista">
            {items.map((item) => (
              <li key={item.id} className="carrito__item">
                {item.imagen && <img className="carrito__imagen" src={item.imagen} alt="" />}
                <div className="carrito__datos">
                  <strong>{item.nombre}</strong>
                  <span className="carrito__unitario">{pesos.format(item.precio)} c/u</span>
                </div>
                <div className="carrito__cantidad">
                  <button
                    type="button"
                    className="boton boton--icono"
                    aria-label="Quitar una unidad"
                    disabled={item.cantidad <= 1}
                    onClick={() => cambiarCantidad(item.id, item.cantidad - 1)}
                  >
                    −
                  </button>
                  <input
                    type="number"
                    min="1"
                    max={item.stock}
                    value={item.cantidad}
                    aria-label={`Cantidad de ${item.nombre}`}
                    onChange={(evento) => cambiarCantidad(item.id, Number(evento.target.value) || 1)}
                  />
                  <button
                    type="button"
                    className="boton boton--icono"
                    aria-label="Agregar una unidad"
                    disabled={item.cantidad >= item.stock}
                    onClick={() => cambiarCantidad(item.id, item.cantidad + 1)}
                  >
                    +
                  </button>
                </div>
                <span className="carrito__subtotal">{pesos.format(item.precio * item.cantidad)}</span>
                <button type="button" className="boton boton--peligro" onClick={() => quitar(item.id)}>
                  Quitar
                </button>
              </li>
            ))}
          </ul>

          <aside className="carrito__resumen">
            <span>Total</span>
            <strong className="carrito__total">{pesos.format(total)}</strong>
            <button type="button" className="boton" onClick={vaciar}>
              Vaciar carrito
            </button>
          </aside>
        </div>
      )}
    </>
  );
}
