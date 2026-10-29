import { useEffect, useState } from "react";

import { API_URL, obtenerCategorias, obtenerMotos } from "./api.js";
import { useCarrito } from "./carrito.js";
import Carrito from "./components/Carrito.jsx";
import Categorias from "./components/Categorias.jsx";
import Panel from "./components/Panel.jsx";
import TarjetaMoto from "./components/TarjetaMoto.jsx";

const rutaActual = () => window.location.hash.replace(/^#/, "") || "/";

function Catalogo({ carrito }) {
  const [categorias, setCategorias] = useState([]);
  const [categoria, setCategoria] = useState(null);
  const [texto, setTexto] = useState("");
  const [buscar, setBuscar] = useState("");
  const [motos, setMotos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    obtenerCategorias()
      .then(setCategorias)
      .catch((fallo) => setError(fallo.message));
  }, []);

  useEffect(() => {
    const espera = setTimeout(() => setBuscar(texto.trim()), 300);
    return () => clearTimeout(espera);
  }, [texto]);

  useEffect(() => {
    let vigente = true;
    setCargando(true);
    obtenerMotos({ categoria, buscar })
      .then((datos) => {
        if (!vigente) return;
        setMotos(datos);
        setError("");
      })
      .catch((fallo) => vigente && setError(fallo.message))
      .finally(() => vigente && setCargando(false));
    return () => {
      vigente = false;
    };
  }, [categoria, buscar]);

  const actual = categorias.find((item) => item.id === categoria);

  let aviso = "";
  if (error) aviso = `No se pudo consultar la API (${error}).`;
  else if (cargando) aviso = "Cargando motos…";
  else if (!motos.length) aviso = "No hay motos para mostrar.";

  return (
    <>
      <section className="titular">
        <p className="titular__sobre">Catálogo</p>
        <h1 className="titular__titulo">{actual ? actual.nombre : "Todas las motos"}</h1>
        <p className="titular__resumen">
          {!cargando && !error && `${motos.length} ${motos.length === 1 ? "moto" : "motos"}`}
        </p>
      </section>

      <input
        className="buscador"
        type="search"
        placeholder="Buscar moto o marca"
        aria-label="Buscar moto o marca"
        value={texto}
        onChange={(evento) => setTexto(evento.target.value)}
      />

      <Categorias categorias={categorias} activa={categoria} alElegir={setCategoria} />

      <p className="estado" role="status">
        {aviso}
      </p>
      {!error && (
        <section className="rejilla">
          {motos.map((moto) => (
            <TarjetaMoto
              key={moto.id}
              moto={moto}
              enCarrito={carrito.items.find((item) => item.id === moto.id)?.cantidad || 0}
              alAgregar={carrito.agregar}
            />
          ))}
        </section>
      )}
    </>
  );
}

export default function App() {
  const [ruta, setRuta] = useState(rutaActual);
  const carrito = useCarrito();

  useEffect(() => {
    const alCambiar = () => {
      setRuta(rutaActual());
      window.scrollTo(0, 0);
    };
    window.addEventListener("hashchange", alCambiar);
    return () => window.removeEventListener("hashchange", alCambiar);
  }, []);

  const enlace = (destino, texto) => (
    <a href={`#${destino}`} className={ruta === destino ? "menu__enlace menu__enlace--activo" : "menu__enlace"}>
      {texto}
    </a>
  );

  let pagina = <Catalogo carrito={carrito} />;
  if (ruta === "/carrito") pagina = <Carrito carrito={carrito} />;
  else if (ruta === "/panel") pagina = <Panel />;

  return (
    <>
      <header className="cabecera">
        <a className="cabecera__marca" href="#/">
          MOTO<span>MARKET</span>
        </a>
        <nav className="menu" aria-label="Principal">
          {enlace("/", "Catálogo")}
          {enlace("/carrito", <>Carrito <span className="menu__contador">{carrito.unidades}</span></>)}
          {enlace("/panel", "Administrador")}
        </nav>
      </header>

      <main className="contenido">{pagina}</main>

      <footer className="pie">
        <span>MotoMarket · Frontend en React consumiendo la API REST</span>
        <a href={import.meta.env.VITE_DOCS_URL || `${API_URL}/docs/`} target="_blank" rel="noopener">
          Documentación de la API (Swagger)
        </a>
      </footer>
    </>
  );
}
