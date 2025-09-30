## 1. Descripción del Proyecto

Este proyecto es una **plataforma de gestión de vacantes laborales** desarrollada con **Django (backend)** y **React (frontend)**. Permite a los **reclutadores** publicar, editar y eliminar ofertas de empleo, mientras que los **usuarios registrados** pueden explorar detalles de cada vacante.

El sistema incluye:
- Autenticación mediante tokens (Django REST Framework).
- Control de permisos para operaciones sensibles.
- Un frontend interactivo construido con React y React Router.
- Interacción entre frontend y backend a través de peticiones HTTP seguras.

> **Enfoque en Ciencia de Datos:**  
> El proyecto está orientado a desarrollar un sistema inteligente de **profiling de usuarios**, basado en sus respuestas a preguntas contextuales (formato tipo popup, no invasivo) y en sus patrones de interacción (por ejemplo, likes o visualizaciones). Esto permitirá hacer recomendaciones precisas tanto de **vacantes relevantes** como del **perfil profesional** ideal que el usuario busca desarrollar.

## 2. Funcionalidades Principales

### Autenticación y Gestión de Usuarios
- Registro de usuarios con campos personalizados (¿Es reclutador?).
- Login con autenticación por token (DRF TokenAuth).
- Visualización del usuario actual desde frontend.

### Gestión de Vacantes (CRUD)
- Crear, leer, actualizar y eliminar vacantes.
- Solo los reclutadores pueden crear y administrar vacantes.
- Las vacantes están asociadas al reclutador que las crea.

### Control de Permisos
- Las acciones sensibles (editar/eliminar vacantes) están restringidas al reclutador propietario.
- Los usuarios no reclutadores no pueden ver botones de edición o eliminación.
- Validaciones visuales que muestran mensajes amigables si se intenta acceder a funcionalidades sin permisos.

### Interfaz de Usuario
- Interfaz React con rutas protegidas.
- Botones y acciones que se muestran/ocultan dinámicamente según el rol del usuario y su relación con la vacante.

### Enfoque Inteligente de Recomendación (futuro)
- Integración futura con sistema de recomendaciones basado en:
  - Preguntas contextuales y no invasivas (popups).
  - Comportamiento del usuario (likes, visualizaciones).
  - Algoritmos de análisis de datos para generar perfiles y sugerencias personalizadas.

## 4. Tecnologías Utilizadas

Este proyecto está construido con una arquitectura **Full Stack** moderna:

### Backend
- **Python 3**
- **Django**: Framework web robusto y escalable.
- **Django REST Framework (DRF)**: Para crear la API RESTful.
- **Token Authentication**: Para la autenticación segura de usuarios.
- **SQLite3** (modo desarrollo): Base de datos simple y ligera.

### Frontend
- **React.js**: Biblioteca para construir interfaces de usuario dinámicas.
- **React Router DOM**: Manejo de rutas y navegación protegida.
- **Axios**: Cliente HTTP para conectar con la API de Django.

### Herramientas adicionales
- **Postman**: Para testear endpoints de la API.
- **Vite**: Para el entorno de desarrollo React (rápido y moderno).
- **VSCode + ESLint/Prettier**: Para asegurar buena calidad de código.

### Enfoque futuro
- **Machine Learning / Data Science** para el sistema de recomendación.
- Posible uso de **Pandas, Scikit-learn, NLP**, o frameworks como **TensorFlow o PyTorch** para hacer *profiling* y matching inteligente de usuarios y vacantes.

## 5. Instalación y Configuración

### Backend (Django)

1. **Clona el repositorio**:
```bash
git clone https://github.com/sherrerah3/profile-flow-arquitectura
cd profile-flow-arquitectura
```

2. **Crea un entorno virtual**:
```bash
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
```

3. **Instala las dependencias**:
```bash
pip install -r requirements.txt
```

4. **Realiza las migraciones**:
```bash
python manage.py migrate
```

5. **Crea un superusuario (opcional para admin)**:
```bash
python manage.py createsuperuser
```

6. **Inicia el servidor**:
```bash
python manage.py runserver
```

### Frontend (React)

1. **Ve al directorio del frontend**:
```bash
cd profile-flow-frontend
```

2. **Instala las dependencias**:
```bash
npm install
```

3. **Inicia el servidor de desarrollo**:
```bash
npm start
```

## 6. Uso y Ejemplos de Endpoints

### Autenticación

- **Registro**  
  `POST /api/users/register/`  
  Cuerpo (JSON):
  ```json
  {
    "username": "usuario123",
    "password": "contraseña_segura",
    "is_recruiter": true
  }
  ```

- **Login**  
  `POST /api/users/login/`  
  Cuerpo (JSON):
  ```json
  {
  "username": "usuario123",
  "password": "contraseña_segura"
  }
  ```
  Respuesta:
  ```json
  {
  "token": "abc123...",
    "user": {
      "id": 1,
      "username": "usuario123",
      "is_recruiter": true
    }
  }
  ```

---

### Vacantes (Jobs)

> Todos estos endpoints requieren autenticación (Token en el header).

- **Listar vacantes**  
  `GET /api/jobs/`  
  Devuelve una lista de vacantes. Si el usuario es reclutador, ve solo las suyas.

- **Crear vacante**  
  `POST /api/jobs/`  
  Solo disponible para usuarios con `is_recruiter = true`.  
  Cuerpo de ejemplo:
  ```json
  {
    "title": "Backend Developer",
    "description": "Descripción del puesto",
    "location": "Remoto",
    "company": "Tech Corp"
  }
  ```

- **Detalle de vacante**  
  `GET /api/jobs/<id>/`  
  Devuelve los datos de una vacante específica.
  Solo usuarios autenticados pueden acceder.

- **Actualizar vacante**  
  `PUT /api/jobs/<id>/`  
  Solo disponible para el reclutador que creó la vacante.
  Cuerpo igual al de creación.

- **Eliminar vacante**  
  `DELETE /api/jobs/<id>/`  
  Solo disponible para el reclutador que creó la vacante.

# . Licencia

Este proyecto está bajo la licencia [MIT](https://opensource.org/licenses/MIT), lo que significa que podés usarlo, modificarlo y distribuirlo libremente, siempre que mantengas los créditos originales.
