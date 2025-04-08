// src/pages/EditarVacante.js
import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";

const EditarVacante = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [titulo, setTitulo] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [empresa, setEmpresa] = useState('');
  const [ubicacion, setUbicacion] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchVacante = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`http://localhost:8000/api/jobs/${id}/`, {
          headers: {
            Authorization: `Token ${token}`,
          },
        });

        const data = response.data;
        setTitulo(data.title);
        setDescripcion(data.description);
        setEmpresa(data.company);
        setUbicacion(data.location);
      } catch (err) {
        console.error(err);
        setError('Error al cargar la vacante');
      }
    };

    fetchVacante();
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const token = localStorage.getItem('token');
      await axios.put(`http://localhost:8000/api/jobs/${id}/`, {
        title: titulo,
        description: descripcion,
        company: empresa,
        location: ubicacion,
      }, {
        headers: {
          Authorization: `Token ${token}`,
        },
      });

      navigate('/vacantes');
    } catch (err) {
      console.error(err);
      setError('Error al actualizar la vacante');
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Editar Vacante</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Título:</label><br />
          <input value={titulo} onChange={(e) => setTitulo(e.target.value)} required />
        </div>
        <div>
          <label>Descripción:</label><br />
          <textarea value={descripcion} onChange={(e) => setDescripcion(e.target.value)} required />
        </div>
        <div>
          <label>Empresa:</label><br />
          <input value={empresa} onChange={(e) => setEmpresa(e.target.value)} required />
        </div>
        <div>
          <label>Ubicación:</label><br />
          <input value={ubicacion} onChange={(e) => setUbicacion(e.target.value)} required />
        </div>
        <button type="submit">Actualizar Vacante</button>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </form>
    </div>
  );
};

export default EditarVacante;
