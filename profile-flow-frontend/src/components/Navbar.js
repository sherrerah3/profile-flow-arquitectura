import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import "./Navbar.css";

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
    <nav className="navbar">
      <div className="navbar-left">
        <Link to="/vacantes" className="navbar-logo">
          ProfileFlow
        </Link>
      </div>
      <div className="navbar-right">
        {usuario ? (
          <>
            <Link to="/perfil" className="navbar-link">
              Perfil
            </Link>

            {!usuario.is_recruiter && (
              <Link to="/vacantes" className="navbar-link">
                Vacantes
              </Link>
            )}

            {usuario.is_recruiter ? (
              <Link to="/vacantes-publicadas" className="navbar-link">
                Vacantes publicadas
              </Link>
            ) : (
              <Link to="/mis-likes" className="navbar-link">
                Mis likes
              </Link>
            )}

            {!usuario.is_recruiter && (
              <Link to="/recomendaciones" className="navbar-link">
                Recomendaciones
              </Link>
            )}

            <button onClick={handleLogout} className="navbar-button">
              Cerrar sesión
            </button>
          </>
        ) : (
          <>
            <Link to="/" className="navbar-link">
              Login
            </Link>
            <Link to="/registro" className="navbar-link">
              Registro
            </Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
