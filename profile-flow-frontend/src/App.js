import React, { useEffect, useState } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from "react-router-dom";
import Login from "./pages/Login";
import Vacantes from "./pages/Vacantes";
import Register from "./pages/Register";
import PrivateRoute from "./components/PrivateRoute";
import CrearVacante from "./pages/CrearVacante";
import VacanteDetalle from "./pages/VacanteDetalle";
import EditarVacante from "./pages/EditarVacante";
import Navbar from "./components/Navbar";
import MisLikes from "./pages/MisLikes";
import Perfil from "./pages/Perfil";
import MisVacantesPublicadas from "./pages/MisVacantesPublicadas";
import Recomendaciones from "./pages/Recomendaciones";

const AppContent = () => {
  const location = useLocation();
  const hideNavbarRoutes = ["/", "/register"];
  const hideNavbar = hideNavbarRoutes.includes(location.pathname);

  return (
    <>
      {!hideNavbar && <Navbar />}
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Rutas protegidas */}
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
        <Route
          path="/mis-likes"
          element={
            <PrivateRoute>
              <MisLikes />
            </PrivateRoute>
          }
        />
        <Route
          path="/perfil"
          element={
            <PrivateRoute>
              <Perfil />
            </PrivateRoute>
          }
        />
        <Route
          path="/vacantes-publicadas"
          element={
            <PrivateRoute>
              <MisVacantesPublicadas />
            </PrivateRoute>
          }
        />
        <Route
          path="/recomendaciones"
          element={
            <PrivateRoute>
              <Recomendaciones />
            </PrivateRoute>
          }
        />
      </Routes>
    </>
  );
};

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
