import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./Login.css"; // Asegurate de tener este archivo

function Register() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    email: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:8000/api/users/register/", formData);
      alert("Registro exitoso. Inicia sesión.");
      navigate("/"); // o directamente a /vacantes si querés
    } catch (error) {
      console.error("Error al registrar:", error);
      alert("Hubo un error en el registro.");
    }
  };

  return (
    <div className="login-container">
      <img src="/logo.png" alt="Logo Magneto Empleos" className="logo" />
      <div className="login-box">
        <h1 className="welcome-title">Crea tu cuenta!</h1>
        <form onSubmit={handleSubmit}>
          <input
            className="login-input"
            type="text"
            name="username"
            placeholder="Nombre"
            value={formData.username}
            onChange={handleChange}
          /><br />
          <input
            className="login-input"
            type="email"
            name="email"
            placeholder="Correo"
            value={formData.email}
            onChange={handleChange}
          /><br />
          <input
            className="login-input"
            type="password"
            name="password"
            placeholder="Contraseña"
            value={formData.password}
            onChange={handleChange}
          /><br />
          <button className="login-button" type="submit">
            Registrarse
          </button>
        </form>
      </div>
    </div>
  );
}

export default Register;
