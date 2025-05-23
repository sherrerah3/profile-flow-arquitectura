import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Vacantes.css";

const MisLikes = () => {
  const [likes, setLikes] = useState([]);
  const [error, setError] = useState("");
  const [mensaje, setMensaje] = useState(""); // 👈 mensaje temporal

  const fetchLikes = async () => {
    try {
      const token = localStorage.getItem("token");
      const res = await axios.get(
        "http://localhost:8000/api/interactions/mis/?interaction_type=like",
        {
          headers: { Authorization: `Token ${token}` },
        }
      );
      setLikes(res.data);
    } catch (err) {
      console.error(err);
      setError("Error al cargar tus likes.");
    }
  };

  const handleEliminarLike = async (interactionId) => {
    const confirmar = window.confirm(
      "¿Estás seguro de que quieres quitar el like?"
    );
    if (!confirmar) return;

    try {
      const token = localStorage.getItem("token");
      await axios.delete(
        `http://localhost:8000/api/interactions/${interactionId}/`,
        {
          headers: { Authorization: `Token ${token}` },
        }
      );

      setLikes((prev) => prev.filter((like) => like.id !== interactionId));
      setMensaje("Like eliminado correctamente ✅");

      // Elimina el mensaje después de 3 segundos
      setTimeout(() => setMensaje(""), 3000);
    } catch (err) {
      console.error(err);
      alert("No se pudo quitar el like.");
    }
  };

  useEffect(() => {
    fetchLikes();
  }, []);

  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div className="vacantes-container">
      <h1>
        <strong>Vacantes que te gustaron</strong>
      </h1>

      {/* Banner temporal de mensaje */}
      {mensaje && (
        <div
          style={{
            backgroundColor: "#d4edda",
            color: "#155724",
            padding: "1rem",
            borderRadius: "5px",
            marginBottom: "1rem",
            border: "1px solid #c3e6cb",
          }}
        >
          {mensaje}
        </div>
      )}

      {likes.length === 0 ? (
        <p>No has dado like a ninguna vacante.</p>
      ) : (
        <div className="vacantes-grid">
          {likes.map((like) => (
            <div className="vacante-card" key={like.id}>
              <div className="vacante-img">
                <img src="/vacante.png" alt="vacante" />
              </div>

              <div
                className="vacante-content"
                style={{
                  display: "flex",
                  flex: 1,
                  justifyContent: "space-between",
                  alignItems: "flex-start",
                }}
              >
                <div className="vacante-info">
                  <h3>{like.job_details?.title}</h3>
                  <p>
                    <strong>Empresa:</strong> {like.job_details?.company}
                  </p>
                  <p>
                    <strong>Ubicación:</strong> {like.job_details?.location}
                  </p>

                  <button
                    className="vacante-btn"
                    onClick={() =>
                      (window.location.href = `/vacantes/${like.job_details?.id}`)
                    }
                  >
                    Ver detalle
                  </button>
                </div>

                <button
                  className="like-btn"
                  onClick={() => handleEliminarLike(like.id)}
                  aria-label="Quitar like"
                >
                  <img
                    src="/liked.png"
                    alt="Quitar like"
                    className="like-icon"
                  />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MisLikes;
