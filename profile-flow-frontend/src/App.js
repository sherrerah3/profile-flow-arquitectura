import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Vacantes from "./pages/Vacantes";
import Register from "./pages/Register";
import PrivateRoute from "./components/PrivateRoute";
import CrearVacante from "./pages/CrearVacante";
import VacanteDetalle from "./pages/VacanteDetalle";
import EditarVacante from "./pages/EditarVacante";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* 🔐 Rutas protegidas */}
        <Route
          path="/vacantes"
          element={
            <PrivateRoute>
              <Vacantes />
            </PrivateRoute>
          }
        />
        <Route
          path="/vacantes/:id"
          element={
            <PrivateRoute>
              <VacanteDetalle />
            </PrivateRoute>
          }
        />
        <Route
          path="/vacantes/:id/editar"
          element={
            <PrivateRoute>
              <EditarVacante />
            </PrivateRoute>
          }
        />
        <Route
          path="/crear-vacante"
          element={
            <PrivateRoute>
              <CrearVacante />
            </PrivateRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
