# � Inventrack Backend

Inventrack es una API desarrollada en **Python + FastAPI** enfocada en la **gestión de inventarios**, permitiendo administrar productos, bodegas (almacenes), movimientos de stock (entradas y salidas), usuarios y roles.

El proyecto utiliza una base de datos **SQLite**, autenticación **JWT**, un sistema modular de routers y un entorno listo para producción mediante Docker.

## 🚀 Características principales

-   **FastAPI** como framework principal de alto rendimiento.
-   **Autenticación JWT** segura para usuarios.
-   **Gestión de Roles y Usuarios** (RBAC).
-   **Gestión de Productos** con detalles y precios.
-   **Gestión de Bodegas** (Almacenes) para ubicación física del stock.
-   **Control de Movimientos**: Registro de Entradas y Salidas de mercancía.
-   **Cálculo de Stock** en tiempo real.
-   **Base de datos SQLite** (`inventrack.db`) con ORM de **SQLAlchemy**.
-   **Rutas modularizadas** para un código limpio y escalable.
-   **Docker + Docker Compose** para despliegue rápido.
-   **Script de seed** para poblar la base de datos con datos de prueba.

## 🗂️ Estructura del Proyecto

    inventrack-backend/
    │
    ├── .env.example
    ├── .gitignore
    ├── inventrack.db      <-- Base de datos SQLite
    ├── docker-compose.yml
    ├── Dockerfile
    ├── requirements.txt
    ├── seed.py            <-- Script de población de datos
    │
    └── app/
        ├── __init__.py
        ├── auth.py
        ├── crud.py
        ├── database.py
        ├── deps.py
        ├── main.py
        ├── models.py
        ├── schemas.py
        │
        └── routers/
            ├── auth.py
            ├── users.py
            ├── products.py (ejemplo)
            ├── warehouses.py (ejemplo)
            └── ...

## ⚙️ Requisitos

-   Python **3.10+**
-   pip
-   (Opcional) Docker y Docker Compose

## 🔧 Instalación manual

1.  **Clonar el repositorio:**

    ```bash
    git clone <url-del-repo>
    cd agrombia-backend
    ```

2.  **Crear y activar entorno virtual:**

    ```bash
    python -m venv .venv
    # En Linux/Mac:
    source .venv/bin/activate
    # En Windows:
    # .venv\Scripts\activate
    ```

3.  **Instalar dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar la aplicación:**

    ```bash
    uvicorn app.main:app --reload
    ```

    La API estará disponible en `http://localhost:8000`.

## 🐳 Instalación con Docker

Para levantar todo el entorno con Docker Compose:

```bash
docker-compose up --build
```

## 🌱 Seed (Datos de prueba)

Para cargar datos iniciales en la base de datos:

```bash
python seed.py
```

## 📌 Documentación

Una vez corriendo la aplicación, puedes acceder a la documentación interactiva:

-   **Swagger UI:** http://localhost:8000/docs
-   **ReDoc:** http://localhost:8000/redoc
