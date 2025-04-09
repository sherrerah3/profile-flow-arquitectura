import React, { useEffect, useState } from "react";
import axios from "axios";

const Perfil = () => {
  const [usuario, setUsuario] = useState(null);
  const [mensaje, setMensaje] = useState("");
  const [error, setError] = useState("");

  const [form, setForm] = useState({
    username: "",
    email: "",
  });

  useEffect(() => {
    const fetchUsuario = async () => {
      const token = localStorage.getItem("token");
      if (!token) return;

      try {
        const res = await axios.get("http://localhost:8000/api/users/me/", {
          headers: { Authorization: `Token ${token}` },
        });
        setUsuario(res.data);
        setForm({
          username: res.data.username,
          email: res.data.email,
        });
      } catch (err) {
        console.error(err);
        setError("Error al obtener la información del usuario.");
      }
    };

    fetchUsuario();
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");

    try {
      await axios.put("http://localhost:8000/api/users/me/", form, {
        headers: { Authorization: `Token ${token}` },
      });
      setMensaje("Perfil actualizado correctamente ✅");
      setError("");

      setTimeout(() => setMensaje(""), 3000);
    } catch (err) {
      console.error(err);
      setError("No se pudo actualizar el perfil.");
    }
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "500px", margin: "0 auto" }}>
      <h2>Mi perfil</h2>

      {mensaje && <p style={{ color: "green" }}>{mensaje}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {usuario ? (
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: "1rem" }}>
            <label>Nombre de usuario:</label>
            <input
              type="text"
              name="username"
              value={form.username}
              onChange={handleChange}
              style={{ width: "100%", padding: "0.5rem" }}
            />
          </div>

          <div style={{ marginBottom: "1rem" }}>
            <label>Correo electrónico:</label>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              style={{ width: "100%", padding: "0.5rem" }}
            />
          </div>

          <button type="submit" style={{ padding: "0.5rem 1rem" }}>
            Guardar cambios
          </button>
        </form>
      ) : (
        <p>Cargando información...</p>
      )}
    </div>
  );
};

export default Perfil;
