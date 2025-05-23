import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import QuestionPopup from "../components/QuestionPopup";
import "./Vacantes.css"; // Asegúrate de tener este archivo

function Vacantes() {
  const [vacantes, setVacantes] = useState([]);
  const [usuarioActual, setUsuarioActual] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [likes, setLikes] = useState({}); // {vacanteId: {yaDioLike: bool, idInteraccion: number}}
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDatos = async () => {
      try {
        const token = localStorage.getItem("token");

        const [vacantesRes, userRes] = await Promise.all([
          axios.get("http://localhost:8000/api/jobs/", {
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
        } else {
          setVacantes(vacantesRes.data);
          // Verificar likes para cada vacante
          verificarLikes(vacantesRes.data, token);
        }
      } catch (error) {
        console.error("Error al obtener datos:", error);
      } finally {
        setCargando(false);
      }
    };

    const verificarLikes = async (vacantes, token) => {
      try {
        const likesData = {};

        // Obtener todos los likes del usuario
        const res = await axios.get(
          "http://localhost:8000/api/interactions/mis/?interaction_type=like",
          { headers: { Authorization: `Token ${token}` } }
        );

        // Crear un mapa de vacantes con like
        const vacantesConLike = new Set(
          res.data.map((interaction) => interaction.job)
        );

        // Inicializar el estado de likes
        vacantes.forEach((vacante) => {
          likesData[vacante.id] = {
            yaDioLike: vacantesConLike.has(vacante.id),
            idInteraccion:
              res.data.find((i) => i.job === vacante.id)?.id || null,
          };
        });

        setLikes(likesData);
      } catch (err) {
        console.error("Error al verificar likes:", err);
      }
    };

    fetchDatos();
  }, [navigate]);

  const handleLikeToggle = async (vacanteId) => {
    const token = localStorage.getItem("token");
    const likeInfo = likes[vacanteId] || {
      yaDioLike: false,
      idInteraccion: null,
    };

    try {
      if (likeInfo.yaDioLike && likeInfo.idInteraccion) {
        // Quitar like
        await axios.delete(
          `http://localhost:8000/api/interactions/${likeInfo.idInteraccion}/`,
          {
            headers: { Authorization: `Token ${token}` },
          }
        );

        setLikes((prev) => ({
          ...prev,
          [vacanteId]: { yaDioLike: false, idInteraccion: null },
        }));
      } else {
        // Dar like
        const res = await axios.post(
          `http://localhost:8000/api/interactions/`,
          { job: vacanteId, interaction_type: "like" },
          { headers: { Authorization: `Token ${token}` } }
        );

        setLikes((prev) => ({
          ...prev,
          [vacanteId]: { yaDioLike: true, idInteraccion: res.data.id },
        }));
      }
    } catch (err) {
      console.error("Error al alternar like:", err);
    }
  };

  if (cargando) {
    return <p style={{ padding: "2rem" }}>Cargando vacantes...</p>;
  }

  return (
    <>
      <QuestionPopup />

      <div className="vacantes-container">
        <h1>
          <strong>Vacantes Disponibles</strong>
        </h1>

        <div className="vacantes-grid">
          {vacantes.map((vacante) => (
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

                <button
                  className="like-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleLikeToggle(vacante.id);
                  }}
                  aria-label={
                    likes[vacante.id]?.yaDioLike ? "Quitar like" : "Dar like"
                  }
                >
                  <img
                    src={
                      likes[vacante.id]?.yaDioLike ? "/liked.png" : "/like.png"
                    }
                    alt="like"
                    className="like-icon"
                  />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default Vacantes;
