import { useEffect, useState } from "react";

import { cerrarSesion, consultarSesion, crear, editar, eliminar, iniciarSesion, listar } from "../api.js";
import { pesos } from "../carrito.js";

const RECURSOS = {
  motos: {
    titulo: "Motos",
    singular: "moto",
    columnas: [
      ["Moto", (m) => `${m.marca_nombre} ${m.modelo} ${m.anio}`],
      ["Categoría", (m) => m.categoria_nombre],
      ["Precio", (m) => pesos.format(Number(m.precio))],
      ["Stock", (m) => m.stock],
      ["Visible", (m) => (m.activa ? "Sí" : "No")],
    ],
    campos: [
      { nombre: "marca", etiqueta: "Marca", tipo: "relacion", recurso: "marcas", requerido: true },
      { nombre: "categoria", etiqueta: "Categoría", tipo: "relacion", recurso: "categorias", requerido: true },
      { nombre: "modelo", etiqueta: "Modelo", requerido: true },
      { nombre: "anio", etiqueta: "Año", tipo: "number", requerido: true, inicial: new Date().getFullYear() },
      { nombre: "precio", etiqueta: "Precio (COP)", tipo: "number", requerido: true },
      { nombre: "stock", etiqueta: "Unidades disponibles", tipo: "number", inicial: 1 },
      { nombre: "cilindraje", etiqueta: "Cilindraje (cc)", tipo: "number", inicial: 0 },
      { nombre: "potencia_hp", etiqueta: "Potencia (HP)", tipo: "number", inicial: 0 },
      {
        nombre: "combustible",
        etiqueta: "Combustible",
        tipo: "opciones",
        opciones: [["gasolina", "Gasolina"], ["electrica", "Eléctrica"]],
        inicial: "gasolina",
      },
      {
        nombre: "transmision",
        etiqueta: "Transmisión",
        tipo: "opciones",
        opciones: [["manual", "Manual"], ["automatica", "Automática"], ["semiautomatica", "Semiautomática"]],
        inicial: "manual",
      },
      { nombre: "color", etiqueta: "Color" },
      { nombre: "imagen_url", etiqueta: "Foto (enlace https, opcional)", tipo: "url" },
      { nombre: "descripcion", etiqueta: "Descripción", tipo: "textarea" },
      { nombre: "destacada", etiqueta: "Destacada en la portada", tipo: "checkbox", inicial: false },
      { nombre: "activa", etiqueta: "Visible en el catálogo", tipo: "checkbox", inicial: true },
    ],
  },
  categorias: {
    titulo: "Categorías",
    singular: "categoría",
    columnas: [
      ["Nombre", (c) => c.nombre],
      ["Descripción", (c) => c.descripcion || "—"],
      ["Motos", (c) => c.total_motos],
    ],
    campos: [
      { nombre: "nombre", etiqueta: "Nombre", requerido: true },
      { nombre: "descripcion", etiqueta: "Descripción", tipo: "textarea" },
    ],
  },
  marcas: {
    titulo: "Marcas",
    singular: "marca",
    columnas: [
      ["Nombre", (m) => m.nombre],
      ["País de origen", (m) => m.pais_origen || "—"],
    ],
    campos: [
      { nombre: "nombre", etiqueta: "Nombre", requerido: true },
      { nombre: "pais_origen", etiqueta: "País de origen" },
    ],
  },
};

function valoresIniciales(campos, registro) {
  return Object.fromEntries(
    campos.map((campo) => {
      if (campo.nombre === "imagen_url") return [campo.nombre, ""];
      const valor = registro?.[campo.nombre] ?? campo.inicial ?? "";
      return [campo.nombre, valor];
    })
  );
}

function Formulario({ config, registro, relaciones, alGuardar, alCancelar }) {
  const [valores, setValores] = useState(() => valoresIniciales(config.campos, registro));
  const [error, setError] = useState("");
  const [guardando, setGuardando] = useState(false);

  const cambiar = (nombre, valor) => setValores((actuales) => ({ ...actuales, [nombre]: valor }));

  const enviar = async (evento) => {
    evento.preventDefault();
    setGuardando(true);
    setError("");
    try {
      await alGuardar(valores);
    } catch (fallo) {
      setError(fallo.message);
      setGuardando(false);
    }
  };

  return (
    <form className="formulario" onSubmit={enviar}>
      <h2 className="formulario__titulo">
        {registro ? `Editar ${config.singular}` : `Nueva ${config.singular}`}
      </h2>
      <div className="formulario__campos">
        {config.campos.map((campo) => {
          const id = `campo-${campo.nombre}`;
          const comunes = {
            id,
            required: campo.requerido,
            value: valores[campo.nombre],
            onChange: (evento) => cambiar(campo.nombre, evento.target.value),
          };
          let control;
          if (campo.tipo === "textarea") control = <textarea rows="3" {...comunes} />;
          else if (campo.tipo === "checkbox")
            control = (
              <input
                id={id}
                type="checkbox"
                checked={Boolean(valores[campo.nombre])}
                onChange={(evento) => cambiar(campo.nombre, evento.target.checked)}
              />
            );
          else if (campo.tipo === "relacion" || campo.tipo === "opciones") {
            const opciones =
              campo.tipo === "relacion"
                ? (relaciones[campo.recurso] || []).map((item) => [item.id, item.nombre])
                : campo.opciones;
            control = (
              <select {...comunes}>
                <option value="">Seleccione…</option>
                {opciones.map(([valor, texto]) => (
                  <option key={valor} value={valor}>
                    {texto}
                  </option>
                ))}
              </select>
            );
          } else control = <input type={campo.tipo || "text"} min={campo.tipo === "number" ? 0 : undefined} {...comunes} />;

          return (
            <label
              key={campo.nombre}
              htmlFor={id}
              className={`formulario__campo formulario__campo--${campo.tipo || "text"}`}
            >
              <span>{campo.etiqueta}</span>
              {control}
            </label>
          );
        })}
      </div>
      {error && (
        <p className="aviso aviso--error" role="alert">
          {error}
        </p>
      )}
      <div className="formulario__acciones">
        <button type="submit" className="boton boton--lleno" disabled={guardando}>
          {guardando ? "Guardando…" : "Guardar"}
        </button>
        <button type="button" className="boton" onClick={alCancelar}>
          Cancelar
        </button>
      </div>
    </form>
  );
}

function Gestion({ recurso }) {
  const config = RECURSOS[recurso];
  const [registros, setRegistros] = useState([]);
  const [relaciones, setRelaciones] = useState({});
  const [editando, setEditando] = useState(null);
  const [aviso, setAviso] = useState(null);

  const cargar = () =>
    listar(recurso)
      .then(setRegistros)
      .catch((fallo) => setAviso({ tipo: "error", texto: fallo.message }));

  useEffect(() => {
    setEditando(null);
    setAviso(null);
    cargar();
    const necesarias = config.campos.filter((campo) => campo.tipo === "relacion").map((campo) => campo.recurso);
    Promise.all(necesarias.map((nombre) => listar(nombre))).then((listas) =>
      setRelaciones(Object.fromEntries(necesarias.map((nombre, i) => [nombre, listas[i]])))
    );
  }, [recurso]);

  const guardar = async (valores) => {
    const datos = { ...valores };
    if (!datos.imagen_url) delete datos.imagen_url;
    if (editando === "nuevo") await crear(recurso, datos);
    else await editar(recurso, editando.id, datos);
    setAviso({ tipo: "ok", texto: `La ${config.singular} se guardó correctamente.` });
    setEditando(null);
    cargar();
  };

  const borrar = async (registro) => {
    if (!window.confirm(`¿Eliminar esta ${config.singular}? Esta acción no se puede deshacer.`)) return;
    try {
      await eliminar(recurso, registro.id);
      setAviso({ tipo: "ok", texto: `La ${config.singular} se eliminó.` });
      cargar();
    } catch (fallo) {
      setAviso({ tipo: "error", texto: fallo.message });
    }
  };

  if (editando) {
    return (
      <Formulario
        key={editando === "nuevo" ? "nuevo" : editando.id}
        config={config}
        registro={editando === "nuevo" ? null : editando}
        relaciones={relaciones}
        alGuardar={guardar}
        alCancelar={() => setEditando(null)}
      />
    );
  }

  return (
    <section>
      <div className="panel__barra">
        <h2>
          {config.titulo} <small>({registros.length})</small>
        </h2>
        <button type="button" className="boton boton--lleno" onClick={() => setEditando("nuevo")}>
          + Agregar {config.singular}
        </button>
      </div>
      {aviso && (
        <p className={`aviso aviso--${aviso.tipo}`} role="status">
          {aviso.texto}
        </p>
      )}
      <div className="tabla">
        <table>
          <thead>
            <tr>
              {config.columnas.map(([titulo]) => (
                <th key={titulo}>{titulo}</th>
              ))}
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {registros.map((registro) => (
              <tr key={registro.id}>
                {config.columnas.map(([titulo, valor]) => (
                  <td key={titulo} data-titulo={titulo}>
                    {valor(registro)}
                  </td>
                ))}
                <td className="tabla__acciones">
                  <button type="button" className="boton" onClick={() => setEditando(registro)}>
                    Editar
                  </button>
                  <button type="button" className="boton boton--peligro" onClick={() => borrar(registro)}>
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function Login({ alEntrar }) {
  const [usuario, setUsuario] = useState("");
  const [clave, setClave] = useState("");
  const [error, setError] = useState("");
  const [enviando, setEnviando] = useState(false);

  const enviar = async (evento) => {
    evento.preventDefault();
    setEnviando(true);
    setError("");
    try {
      const sesion = await iniciarSesion(usuario, clave);
      if (!sesion.es_admin) {
        await cerrarSesion();
        throw new Error("Este usuario no es administrador.");
      }
      alEntrar(sesion);
    } catch (fallo) {
      setError(fallo.message);
      setEnviando(false);
    }
  };

  return (
    <form className="formulario formulario--login" onSubmit={enviar}>
      <h2 className="formulario__titulo">Ingreso de administrador</h2>
      <label className="formulario__campo" htmlFor="usuario">
        <span>Usuario o correo</span>
        <input id="usuario" autoComplete="username" required value={usuario} onChange={(e) => setUsuario(e.target.value)} />
      </label>
      <label className="formulario__campo" htmlFor="clave">
        <span>Contraseña</span>
        <input
          id="clave"
          type="password"
          autoComplete="current-password"
          required
          value={clave}
          onChange={(e) => setClave(e.target.value)}
        />
      </label>
      {error && (
        <p className="aviso aviso--error" role="alert">
          {error}
        </p>
      )}
      <button type="submit" className="boton boton--lleno" disabled={enviando}>
        {enviando ? "Ingresando…" : "Ingresar"}
      </button>
    </form>
  );
}

export default function Panel() {
  const [sesion, setSesion] = useState(null);
  const [recurso, setRecurso] = useState("motos");

  useEffect(() => {
    consultarSesion()
      .then(setSesion)
      .catch(() => setSesion({ autenticado: false }));
  }, []);

  const salir = async () => setSesion(await cerrarSesion());

  return (
    <>
      <section className="titular">
        <p className="titular__sobre">Administración</p>
        <h1 className="titular__titulo">Panel</h1>
        <p className="titular__resumen">
          {sesion?.es_admin && (
            <>
              Sesión iniciada como <strong>{sesion.usuario}</strong> ·{" "}
              <button type="button" className="enlace" onClick={salir}>
                Cerrar sesión
              </button>
            </>
          )}
        </p>
      </section>

      {!sesion ? (
        <p className="estado">Verificando sesión…</p>
      ) : !sesion.es_admin ? (
        <Login alEntrar={setSesion} />
      ) : (
        <div className="panel">
          <nav className="categorias" aria-label="Secciones del panel">
            {Object.entries(RECURSOS).map(([clave, config]) => (
              <button
                key={clave}
                type="button"
                className={clave === recurso ? "categorias__boton categorias__boton--activa" : "categorias__boton"}
                onClick={() => setRecurso(clave)}
              >
                {config.titulo}
              </button>
            ))}
          </nav>
          <Gestion recurso={recurso} />
        </div>
      )}
    </>
  );
}
