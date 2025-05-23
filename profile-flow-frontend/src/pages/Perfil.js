import React, { useEffect, useState } from "react";
import axios from "axios";
import './Perfil.css'; // Asegúrate de que este path es correcto

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
    <div className="perfil-container">
      <h2 className="perfil-title">Mi perfil</h2>

      {mensaje && <p className="perfil-msg">{mensaje}</p>}
      {error && <p className="perfil-error">{error}</p>}

      {usuario ? (
        <form onSubmit={handleSubmit} className="perfil-form">
          <div>
            <label>Nombre de usuario:</label>
            <input
              type="text"
              name="username"
              value={form.username}
              onChange={handleChange}
            />
          </div>

          <div>
            <label>Correo electrónico:</label>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
            />
          </div>

          <button type="submit">Guardar cambios</button>
        </form>
      ) : (
        <p>Cargando información...</p>
      )}
    </div>
  );
};

export default Perfil;
