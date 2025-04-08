// src/pages/VacanteDetalle.js
import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

const VacanteDetalle = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [vacante, setVacante] = useState(null);
  const [usuarioActual, setUsuarioActual] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchVacanteYUsuario = async () => {
      try {
        const token = localStorage.getItem("token");

        const [vacanteRes, userRes] = await Promise.all([
          axios.get(`http://localhost:8000/api/jobs/${id}/`, {
            headers: { Authorization: `Token ${token}` },
          }),
          axios.get(`http://localhost:8000/api/users/me/`, {
            headers: { Authorization: `Token ${token}` },
          }),
        ]);

        setVacante(vacanteRes.data);
        setUsuarioActual(userRes.data);
      } catch (err) {
        console.error(err);
        setError("Error al cargar la vacante o el usuario.");
      }
    };

    fetchVacanteYUsuario();
  }, [id]);

  const handleEliminar = async () => {
    const confirmar = window.confirm("¿Estás seguro de que quieres eliminar esta vacante?");
    if (!confirmar) return;

    try {
      const token = localStorage.getItem("token");
      await axios.delete(`http://localhost:8000/api/jobs/${id}/`, {
        headers: { Authorization: `Token ${token}` },
      });
      navigate("/vacantes");
    } catch (error) {
      console.error("Error al eliminar la vacante:", error);
      setError("No se pudo eliminar la vacante.");
    }
  };

  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!vacante || !usuarioActual) return <p>Cargando...</p>;

  const esReclutadorDueño = usuarioActual?.id === vacante.recruiter;

  return (
    <div style={{ padding: "2rem" }}>
      <h2>{vacante.title}</h2>
      <p><strong>Empresa:</strong> {vacante.company}</p>
      <p><strong>Ubicación:</strong> {vacante.location}</p>
      <p><strong>Descripción:</strong> {vacante.description}</p>

      {esReclutadorDueño ? (
        <>
          <button
            onClick={() => navigate(`/vacantes/${vacante.id}/editar`)}
            style={{ marginTop: "1rem" }}
          >
            Editar vacante
          </button>

          <button
            onClick={handleEliminar}
            style={{
              marginTop: "1rem",
              marginLeft: "1rem",
              backgroundColor: "red",
              color: "white",
              border: "none",
              padding: "0.5rem 1rem",
              cursor: "pointer"
            }}
          >
            Eliminar vacante
          </button>
        </>
      ) : (
        <p style={{ marginTop: "1rem", color: "gray" }}>
          Solo el reclutador que creó esta vacante puede editarla o eliminarla.
        </p>
      )}
    </div>
  );
};

export default VacanteDetalle;
