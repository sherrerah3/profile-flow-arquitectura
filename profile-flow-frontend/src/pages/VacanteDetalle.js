import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

const VacanteDetalle = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [vacante, setVacante] = useState(null);
  const [usuarioActual, setUsuarioActual] = useState(null);
  const [error, setError] = useState("");
  const [yaDioLike, setYaDioLike] = useState(false);
  const [idInteraccionLike, setIdInteraccionLike] = useState(null);

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

    const registrarVistaYVerificarLike = async () => {
      const token = localStorage.getItem("token");

      // Registrar vista
      try {
        await axios.post(
          `http://localhost:8000/api/interactions/`,
          { job: id, interaction_type: "view" },
          { headers: { Authorization: `Token ${token}` } }
        );
        console.log("Vista registrada");
      } catch (err) {
        if (err.response?.status === 400) {
          console.log("Ya se había registrado esta vista.");
        } else {
          console.error("Error al registrar vista:", err);
        }
      }

      // Verificar like
      try {
        const res = await axios.get(`http://localhost:8000/api/interactions/mis/?job=${id}&interaction_type=like`, {
          headers: { Authorization: `Token ${token}` },
        });

        if (res.data.length > 0) {
          setYaDioLike(true);
          setIdInteraccionLike(res.data[0].id);
        }
      } catch (err) {
        console.error("Error al verificar like:", err);
      }
    };

    fetchVacanteYUsuario();
    registrarVistaYVerificarLike();
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

  const handleLikeToggle = async () => {
    const token = localStorage.getItem("token");

    try {
      if (yaDioLike && idInteraccionLike) {
        // Quitar like
        await axios.delete(`http://localhost:8000/api/interactions/${idInteraccionLike}/`, {
          headers: { Authorization: `Token ${token}` },
        });
        setYaDioLike(false);
        setIdInteraccionLike(null);
      } else {
        // Dar like
        const res = await axios.post(
          `http://localhost:8000/api/interactions/`,
          { job: id, interaction_type: "like" },
          { headers: { Authorization: `Token ${token}` } }
        );
        setYaDioLike(true);
        setIdInteraccionLike(res.data.id);
      }
    } catch (err) {
      console.error("Error al alternar like:", err);
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
        <>
          <p style={{ marginTop: "1rem", color: "gray" }}>
            Solo el reclutador que creó esta vacante puede editarla o eliminarla.
          </p>
          <div onClick={handleLikeToggle} style={{ cursor: "pointer", marginTop: "2rem" }}>
            <img 
              src={yaDioLike ? "/liked.png" : "/like.png"} 
              alt={yaDioLike ? "Quitar like" : "Dar like"}
              style={{ width: "32px", height: "32px" }}
            />
          </div>
        </>
      )}
    </div>
  );
};

export default VacanteDetalle;
