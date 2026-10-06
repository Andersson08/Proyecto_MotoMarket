export default function Categorias({ categorias, activa, alElegir }) {
  const opciones = [{ id: null, nombre: "Todas" }, ...categorias];

  return (
    <nav className="categorias" aria-label="Categorías">
      {opciones.map((categoria) => (
        <button
          key={categoria.id ?? "todas"}
          type="button"
          className={
            categoria.id === activa
              ? "categorias__boton categorias__boton--activa"
              : "categorias__boton"
          }
          onClick={() => alElegir(categoria.id)}
        >
          {categoria.nombre}
          {categoria.total_motos !== undefined && (
            <span className="categorias__total">{categoria.total_motos}</span>
          )}
        </button>
      ))}
    </nav>
  );
}
