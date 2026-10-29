import { useEffect, useState } from "react";

const CLAVE = "motomarket-carrito";

function leer() {
  try {
    const guardado = JSON.parse(localStorage.getItem(CLAVE));
    return Array.isArray(guardado) ? guardado : [];
  } catch {
    return [];
  }
}

export const pesos = new Intl.NumberFormat("es-CO", {
  style: "currency",
  currency: "COP",
  maximumFractionDigits: 0,
});

export function calcularTotal(items) {
  return items.reduce((suma, item) => suma + Number(item.precio) * item.cantidad, 0);
}

export function useCarrito() {
  const [items, setItems] = useState(leer);

  useEffect(() => {
    try {
      localStorage.setItem(CLAVE, JSON.stringify(items));
    } catch {
      return;
    }
  }, [items]);

  const agregar = (moto) =>
    setItems((actuales) => {
      const existente = actuales.find((item) => item.id === moto.id);
      if (existente) {
        return actuales.map((item) =>
          item.id === moto.id ? { ...item, cantidad: Math.min(item.cantidad + 1, item.stock) } : item
        );
      }
      return [
        ...actuales,
        {
          id: moto.id,
          nombre: `${moto.marca_nombre} ${moto.modelo} ${moto.anio}`,
          precio: Number(moto.precio),
          imagen: moto.imagen,
          stock: moto.stock,
          cantidad: 1,
        },
      ];
    });

  const cambiarCantidad = (id, cantidad) =>
    setItems((actuales) =>
      actuales.map((item) =>
        item.id === id ? { ...item, cantidad: Math.max(1, Math.min(cantidad, item.stock)) } : item
      )
    );

  const quitar = (id) => setItems((actuales) => actuales.filter((item) => item.id !== id));

  const vaciar = () => setItems([]);

  return {
    items,
    agregar,
    cambiarCantidad,
    quitar,
    vaciar,
    total: calcularTotal(items),
    unidades: items.reduce((suma, item) => suma + item.cantidad, 0),
  };
}
