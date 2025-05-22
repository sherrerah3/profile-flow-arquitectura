import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

const Navbar = () => {
  const [usuario, setUsuario] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUsuario = async () => {
      const token = localStorage.getItem("token");
      if (!token) return;

      try {
        const res = await axios.get("http://localhost:8000/api/users/me/", {
          headers: { Authorization: `Token ${token}` },
        });
        setUsuario(res.data);
      } catch (err) {
        console.error("Error obteniendo usuario:", err);
        localStorage.removeItem("token");
        navigate("/");
      }
    };

    fetchUsuario();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <nav style={{ padding: "1rem", borderBottom: "1px solid #ccc" }}>
      {usuario ? (
        <>
          <Link to="/perfil" style={linkStyle}>Inicio</Link>

          {/* Solo los no-reclutadores ven el botón "Vacantes" */}
          {!usuario.is_recruiter && (
            <Link to="/vacantes" style={linkStyle}>Vacantes</Link>
          )}

          {usuario.is_recruiter ? (
            <Link to="/vacantes-publicadas" style={linkStyle}>Vacantes publicadas</Link>
          ) : (
            <Link to="/mis-likes" style={linkStyle}>Mis likes</Link>
          )}

          <button onClick={handleLogout} style={buttonStyle}>Cerrar sesión</button>
        </>
      ) : (
        <>
          <Link to="/" style={linkStyle}>Login</Link>
          <Link to="/registro" style={linkStyle}>Registro</Link>
        </>
      )}
    </nav>
  );
};

const linkStyle = {
  marginRight: "1rem",
  textDecoration: "none",
  color: "#333",
};

const buttonStyle = {
  marginLeft: "1rem",
  backgroundColor: "#02295e",
  color: "white",
  border: "none",
  padding: "0.4rem 0.8rem",
  cursor: "pointer"
};

export default Navbar;
