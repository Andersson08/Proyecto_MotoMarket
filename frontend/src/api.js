export const API_URL = (import.meta.env.VITE_API_URL || "/api").replace(/\/$/, "");

let tokenCsrf = "";

async function obtenerTokenCsrf() {
  if (!tokenCsrf) {
    const respuesta = await fetch(`${API_URL}/auth/csrf/`, { credentials: "include" });
    tokenCsrf = (await respuesta.json()).csrfToken;
  }
  return tokenCsrf;
}

function mensajeDeError(datos, estado) {
  if (!datos) return `La API respondió ${estado}`;
  if (typeof datos.detail === "string") return datos.detail;
  return Object.entries(datos)
    .map(([campo, errores]) => `${campo}: ${[].concat(errores).join(" ")}`)
    .join(" · ");
}

async function pedir(ruta, { metodo = "GET", parametros = {}, cuerpo } = {}) {
  const url = new URL(`${API_URL}${ruta}`, window.location.origin);
  Object.entries(parametros).forEach(([clave, valor]) => {
    if (valor !== null && valor !== undefined && valor !== "") url.searchParams.set(clave, valor);
  });
  const cabeceras = { Accept: "application/json" };
  if (metodo !== "GET") {
    cabeceras["X-CSRFToken"] = await obtenerTokenCsrf();
    cabeceras["Content-Type"] = "application/json";
  }
  const respuesta = await fetch(url, {
    method: metodo,
    headers: cabeceras,
    credentials: "include",
    body: cuerpo === undefined ? undefined : JSON.stringify(cuerpo),
  });
  if (respuesta.status === 204) return null;
  const datos = await respuesta.json().catch(() => null);
  if (!respuesta.ok) throw new Error(mensajeDeError(datos, respuesta.status));
  return datos;
}

export const obtenerCategorias = () => pedir("/categorias/");

export const obtenerMotos = ({ categoria, buscar } = {}) =>
  pedir("/motos/", { parametros: { categoria, buscar } });

export const listar = (recurso) => pedir(`/${recurso}/`);
export const crear = (recurso, datos) => pedir(`/${recurso}/`, { metodo: "POST", cuerpo: datos });
export const editar = (recurso, id, datos) =>
  pedir(`/${recurso}/${id}/`, { metodo: "PATCH", cuerpo: datos });
export const eliminar = (recurso, id) => pedir(`/${recurso}/${id}/`, { metodo: "DELETE" });

export const consultarSesion = () => pedir("/auth/sesion/");

export async function iniciarSesion(usuario, clave) {
  tokenCsrf = "";
  const datos = await pedir("/auth/login/", { metodo: "POST", cuerpo: { usuario, clave } });
  tokenCsrf = "";
  return datos;
}

export async function cerrarSesion() {
  const datos = await pedir("/auth/logout/", { metodo: "POST" });
  tokenCsrf = "";
  return datos;
}
