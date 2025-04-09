import React, { useEffect, useState } from "react";
import axios from "axios";

const MisLikes = () => {
  const [likes, setLikes] = useState([]);
  const [error, setError] = useState("");
  const [mensaje, setMensaje] = useState(""); // 👈 mensaje temporal

  const fetchLikes = async () => {
    try {
      const token = localStorage.getItem("token");
      const res = await axios.get("http://localhost:8000/api/interactions/mis/?interaction_type=like", {
        headers: { Authorization: `Token ${token}` },
      });
      setLikes(res.data);
    } catch (err) {
      console.error(err);
      setError("Error al cargar tus likes.");
    }
  };

  const handleEliminarLike = async (interactionId) => {
    const confirmar = window.confirm("¿Estás seguro de que quieres quitar el like?");
    if (!confirmar) return;

    try {
      const token = localStorage.getItem("token");
      await axios.delete(`http://localhost:8000/api/interactions/${interactionId}/`, {
        headers: { Authorization: `Token ${token}` },
      });

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
    <div style={{ padding: "2rem" }}>
      <h2>Vacantes que te gustaron</h2>

      {/* Banner temporal */}
      {mensaje && (
        <div style={{
          backgroundColor: "#d4edda",
          color: "#155724",
          padding: "1rem",
          borderRadius: "5px",
          marginBottom: "1rem",
          border: "1px solid #c3e6cb"
        }}>
          {mensaje}
        </div>
      )}

      {likes.length === 0 ? (
        <p>No has dado like a ninguna vacante.</p>
      ) : (
        <ul>
          {likes.map((like) => (
            <li key={like.id} style={{ marginBottom: "1rem" }}>
              <strong>{like.job_details?.title}</strong> - {like.job_details?.company} ({like.job_details?.location})
              <button
                onClick={() => handleEliminarLike(like.id)}
                style={{
                  marginLeft: "1rem",
                  backgroundColor: "red",
                  color: "white",
                  border: "none",
                  padding: "0.3rem 0.8rem",
                  cursor: "pointer"
                }}
              >
                Quitar like
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MisLikes;
