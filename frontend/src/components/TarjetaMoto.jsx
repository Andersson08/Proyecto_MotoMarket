const pesos = new Intl.NumberFormat("es-CO", {
  style: "currency",
  currency: "COP",
  maximumFractionDigits: 0,
});

export default function TarjetaMoto({ moto }) {
  return (
    <article className="tarjeta">
      <div className="tarjeta__marco">
        {moto.imagen && (
          <img
            className="tarjeta__imagen"
            src={moto.imagen}
            alt={`${moto.marca_nombre} ${moto.modelo}`}
            loading="lazy"
          />
        )}
        <span className="tarjeta__categoria">{moto.categoria_nombre}</span>
      </div>
      <div className="tarjeta__cuerpo">
        <p className="tarjeta__marca">{moto.marca_nombre}</p>
        <h2 className="tarjeta__modelo">
          {moto.modelo} {moto.anio}
        </h2>
        <p className="tarjeta__ficha">
          {moto.cilindraje} cc · {moto.transmision} · {moto.color || "—"}
        </p>
        <div className="tarjeta__pie">
          <span className="tarjeta__precio">{pesos.format(Number(moto.precio))}</span>
          <span className={moto.disponible ? "tarjeta__stock" : "tarjeta__stock tarjeta__stock--agotada"}>
            {moto.disponible ? `${moto.stock} disponibles` : "Agotada"}
          </span>
        </div>
      </div>
    </article>
  );
}
