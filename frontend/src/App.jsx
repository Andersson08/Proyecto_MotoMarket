import { useEffect, useState } from "react";

import { API_URL, obtenerCategorias, obtenerMotos } from "./api.js";
import Categorias from "./components/Categorias.jsx";
import TarjetaMoto from "./components/TarjetaMoto.jsx";

export default function App() {
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
      <header className="cabecera">
        <a className="cabecera__marca" href="/">
          MOTO<span>MARKET</span>
        </a>
        <input
          className="cabecera__buscar"
          type="search"
          placeholder="Buscar moto o marca"
          value={texto}
          onChange={(evento) => setTexto(evento.target.value)}
        />
      </header>

      <main className="contenido">
        <section className="titular">
          <p className="titular__sobre">Catálogo</p>
          <h1 className="titular__titulo">{actual ? actual.nombre : "Todas las motos"}</h1>
          <p className="titular__resumen">
            {!cargando && !error && `${motos.length} ${motos.length === 1 ? "moto" : "motos"}`}
          </p>
        </section>

        <Categorias categorias={categorias} activa={categoria} alElegir={setCategoria} />

        <p className="estado" role="status">
          {aviso}
        </p>
        {!error && (
          <section className="rejilla">
            {motos.map((moto) => (
              <TarjetaMoto key={moto.id} moto={moto} />
            ))}
          </section>
        )}
      </main>

      <footer className="pie">
        <span>MotoMarket · Frontend en React consumiendo la API REST</span>
        <a href={`${API_URL}/docs/`} target="_blank" rel="noopener">
          Documentación de la API
        </a>
      </footer>
    </>
  );
}
