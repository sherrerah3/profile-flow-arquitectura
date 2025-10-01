// src/pages/Login.js
import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./Login.css"; // Usa el mismo css que el register

const Login = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [authType, setAuthType] = useState("username");
  const [authMessage, setAuthMessage] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setAuthMessage("");

    try {
      // Preparar datos según el tipo de autenticación (Factory Pattern)
      const authData = {
        auth_type: authType,
        password: password,
      };

      // Agregar username o email según la estrategia seleccionada
      if (authType === "email") {
        authData.email = email;
      } else {
        authData.username = username;
      }

      const response = await axios.post(
        "http://localhost:8000/api/users/login/",
        authData
      );

      // Mostrar mensaje del Factory Pattern
      if (response.data.message) {
        setAuthMessage(response.data.message);
      }

      localStorage.setItem("token", response.data.token);
      localStorage.setItem("user", JSON.stringify(response.data.user));

      // Pequeño delay para mostrar el mensaje del Factory
      setTimeout(() => {
        navigate("/vacantes");
      }, 1500);
    } catch (err) {
      if (err.response?.data?.available_strategies) {
        setError(
          `${
            err.response.data.error
          }\nEstrategias disponibles: ${err.response.data.available_strategies.join(
            ", "
          )}`
        );
      } else {
        setError("Credenciales inválidas");
      }
    }
  };

  return (
    <div className="login-container">
      <img
        src="/logo_magneto.png"
        alt="Logo Magneto Empleos"
        className="logo"
      />
      <div className="login-box">
        <h1 className="welcome-title">Bienvenido!</h1>
        <form onSubmit={handleLogin}>
          {/* Factory Pattern Demo - Selector de Estrategia */}
          <div className="factory-label">
            <span className="factory-text">Factory Pattern Demo</span>
          </div>
          <select
            value={authType}
            onChange={(e) => setAuthType(e.target.value)}
            className="login-input auth-selector"
          >
            <option value="username">Autenticación por Usuario</option>
            <option value="email">Autenticación por Email</option>
          </select>

          {/* Input dinámico según la estrategia */}
          {authType === "email" ? (
            <input
              type="email"
              placeholder="Correo electrónico"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="login-input dynamic-input"
            />
          ) : (
            <input
              type="text"
              placeholder="Nombre de usuario"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="login-input dynamic-input"
            />
          )}

          <input
            type="password"
            placeholder="Contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="login-input"
          />
          <button type="submit" className="login-button">
            Iniciar Sesión
          </button>
          <button
            type="button"
            className="register-button"
            onClick={() => navigate("/register")}
          >
            Registrarse
          </button>

          {/* Mensajes del Factory Pattern */}
          {authMessage && (
            <div className="factory-success-message">{authMessage}</div>
          )}

          {error && <div className="factory-error-message">{error}</div>}
        </form>
      </div>
    </div>
  );
};

export default Login;
