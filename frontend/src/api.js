export const API_URL = (import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api").replace(/\/$/, "");

async function pedir(ruta, parametros = {}) {
  const url = new URL(`${API_URL}${ruta}`);
  Object.entries(parametros).forEach(([clave, valor]) => {
    if (valor !== null && valor !== undefined && valor !== "") url.searchParams.set(clave, valor);
  });
  const respuesta = await fetch(url, { headers: { Accept: "application/json" } });
  if (!respuesta.ok) throw new Error(`La API respondió ${respuesta.status}`);
  return respuesta.json();
}

export const obtenerCategorias = () => pedir("/categorias/");

export const obtenerMotos = ({ categoria, buscar } = {}) => pedir("/motos/", { categoria, buscar });
