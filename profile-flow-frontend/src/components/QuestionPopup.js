import React, { useEffect, useState } from "react";

export default function QuestionPopup() {
  const [question, setQuestion] = useState(null);
  const [selectedOption, setSelectedOption] = useState(null);
  const [error, setError] = useState("");
  const [showPopup, setShowPopup] = useState(false);

  useEffect(() => {
    // Al cargar el componente, traer pregunta del día
    fetch("/api/questions/next/", {
      headers: {
        "Content-Type": "application/json",
        // Asume que tienes el token en localStorage o similar
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((res) => {
        if (res.status === 204) {
          // Ya respondió o no hay pregunta, no mostrar popup
          setShowPopup(false);
          return null;
        }
        return res.json();
      })
      .then((data) => {
        if (data) {
          setQuestion(data);
          setShowPopup(true);
        }
      })
      .catch(() => {
        setError("Error al cargar la pregunta.");
      });
  }, []);

  function handleSubmit() {
    if (!selectedOption) {
      setError("Por favor, selecciona una opción.");
      return;
    }

    fetch("/api/questions/answer/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({
        question_id: question.id,
        selected_option: selectedOption,
      }),
    })
      .then((res) => {
        if (res.ok) {
          setShowPopup(false);
          setError("");
          alert("Respuesta guardada, gracias!");
        } else {
          return res.json().then((data) => {
            setError(data.error || "Error al guardar la respuesta.");
          });
        }
      })
      .catch(() => {
        setError("Error en la conexión.");
      });
  }

  if (!showPopup || !question) return null;

  return (
    <div
      style={{
        position: "fixed",
        top: 0, left: 0, right: 0, bottom: 0,
        backgroundColor: "rgba(0,0,0,0.5)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 9999,
      }}
    >
      <div
        style={{
          backgroundColor: "white",
          padding: 20,
          borderRadius: 8,
          maxWidth: 400,
          width: "90%",
          boxShadow: "0 0 10px rgba(0,0,0,0.25)",
        }}
      >
        <h3>Pregunta del día</h3>
        <p>{question.text}</p>

        {question.options && question.options.length > 0 ? (
          <div>
            {question.options.map((option, idx) => (
              <label key={idx} style={{ display: "block", margin: "8px 0" }}>
                <input
                  type="radio"
                  name="option"
                  value={option}
                  checked={selectedOption === option}
                  onChange={() => setSelectedOption(option)}
                />
                {" "}{option}
              </label>
            ))}
          </div>
        ) : (
          <p>No hay opciones disponibles.</p>
        )}

        {error && <p style={{ color: "red" }}>{error}</p>}

        <button onClick={handleSubmit} style={{ marginTop: 12 }}>
          Aceptar
        </button>
      </div>
    </div>
  );
}
