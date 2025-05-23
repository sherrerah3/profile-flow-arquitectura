import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Vacantes.css";
import { useNavigate } from "react-router-dom";

function Recomendaciones() {
  const [recomendaciones, setRecomendaciones] = useState([]);
  const [usuarioActual, setUsuarioActual] = useState(null);
  const [cargando, setCargando] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDatos = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          navigate("/");
          return;
        }

        const [recoRes, userRes] = await Promise.all([
          axios.get("http://localhost:8000/api/recommendations/", {
            headers: { Authorization: `Token ${token}` },
          }),
          axios.get("http://localhost:8000/api/users/me/", {
            headers: { Authorization: `Token ${token}` },
          }),
        ]);

        const usuario = userRes.data;
        setUsuarioActual(usuario);

        if (usuario.is_recruiter) {
          navigate("/vacantes-publicadas");
          return;
        }

        setRecomendaciones(recoRes.data);
      } catch (error) {
        console.error("Error al obtener recomendaciones:", error);
      } finally {
        setCargando(false);
      }
    };

    fetchDatos();
  }, [navigate]);

  if (cargando) {
    return <p style={{ padding: "2rem" }}>Cargando recomendaciones...</p>;
  }

  if (recomendaciones.length === 0) {
    return (
      <p style={{ padding: "2rem" }}>No hay recomendaciones disponibles.</p>
    );
  }
  console.log(recomendaciones);

  return (
    <div className="vacantes-container">
      <h1>
        <strong>Vacantes Recomendadas</strong>
      </h1>

      <div className="vacantes-grid">
        {recomendaciones.map((vacante) => (
          <div className="vacante-card" key={vacante.id}>
            <div className="vacante-img">
              <img src="/vacante.png" alt="vacante" />
            </div>

            <div className="vacante-content">
              <div className="vacante-info">
                <h3>{vacante.title}</h3>
                <p>
                  <strong>Descripción:</strong> {vacante.description}
                </p>
                <p>
                  <strong>Ubicación:</strong> {vacante.location}
                </p>
                <p>
                  <strong>Empresa:</strong> {vacante.company}
                </p>

                <button
                  className="vacante-btn"
                  onClick={() => navigate(`/vacantes/${vacante.id}`)}
                >
                  Ver detalle
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Recomendaciones;
