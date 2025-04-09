import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";

const MisVacantesPublicadas = () => {
  const [vacantes, setVacantes] = useState([]);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const fetchMisVacantes = async () => {
    try {
      const token = localStorage.getItem("token");
      const res = await axios.get("http://localhost:8000/api/jobs/mias/publicadas/", {
        headers: { Authorization: `Token ${token}` },
      });
      setVacantes(res.data);
    } catch (err) {
      console.error(err);
      setError("No se pudieron cargar tus vacantes.");
    }
  };

  useEffect(() => {
    fetchMisVacantes();
  }, []);

  const handleCrearVacante = () => {
    navigate("/crear-vacante");
  };

  const handleEliminar = async (id) => {
    const confirmar = window.confirm("¿Estás seguro de que quieres eliminar esta vacante?");
    if (!confirmar) return;

    try {
      const token = localStorage.getItem("token");
      await axios.delete(`http://localhost:8000/api/jobs/${id}/`, {
        headers: { Authorization: `Token ${token}` },
      });      
      setVacantes((prev) => prev.filter((vacante) => vacante.id !== id));
    } catch (err) {
      console.error(err);
      alert("Error al eliminar la vacante.");
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>Mis vacantes publicadas</h2>

      <button onClick={handleCrearVacante} style={buttonStyle}>
        Crear nueva vacante
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {vacantes.length === 0 ? (
        <p>Aún no has publicado vacantes.</p>
      ) : (
        <ul>
          {vacantes.map((job) => (
            <li key={job.id} style={cardStyle}>
              <strong>{job.title}</strong> - {job.company} ({job.location})
              <br />
              <div style={{ marginTop: "0.5rem" }}>
                <Link to={`/vacantes/${job.id}/editar`} style={editLinkStyle}>
                  Editar
                </Link>
                <button onClick={() => handleEliminar(job.id)} style={deleteButtonStyle}>
                  Eliminar
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

const buttonStyle = {
  padding: "0.5rem 1rem",
  marginBottom: "1.5rem",
  backgroundColor: "#007bff",
  color: "white",
  border: "none",
  borderRadius: "4px",
  cursor: "pointer",
};

const cardStyle = {
  border: "1px solid #ccc",
  borderRadius: "8px",
  padding: "1rem",
  marginBottom: "1rem",
  backgroundColor: "#f9f9f9",
};

const editLinkStyle = {
  marginRight: "1rem",
  textDecoration: "none",
  color: "#007bff",
};

const deleteButtonStyle = {
  padding: "0.3rem 0.7rem",
  backgroundColor: "#dc3545",
  color: "white",
  border: "none",
  borderRadius: "4px",
  cursor: "pointer",
};

export default MisVacantesPublicadas;
