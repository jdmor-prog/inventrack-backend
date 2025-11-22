# 📘 Agrombia Backend

Agrombia Backend es una API desarrollada en **Python + FastAPI**
enfocada en la gestión agrícola, permitiendo administrar cultivos,
clima, noticias, reportes, usuarios y alertas.\
El proyecto utiliza una base de datos SQLite, autenticación JWT, un
sistema modular de routers y un entorno listo para producción mediante
Docker.

## 🚀 Características principales

-   **FastAPI** como framework principal.
-   **Autenticación JWT** para usuarios.
-   **Módulo de clima** para obtener y registrar condiciones climáticas.
-   **Gestión de cultivos**, reportes, tareas y alertas.
-   **Sistema de usuarios** con registros, login y permisos.
-   **Base de datos SQLite** con ORM de SQLAlchemy.
-   **Rutas totalmente modularizadas** dentro de `app/routers/`.
-   **Dockerfile + docker-compose** para despliegue sencillo.
-   **Script de seed** para cargar datos iniciales.

## 🗂️ Estructura del Proyecto

    agrombia-backend/
    │
    ├── .env.example
    ├── .gitignore
    ├── agrombia.db
    ├── docker-compose.yml
    ├── Dockerfile
    ├── requirements.txt
    ├── seed.py
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
            ├── alerts.py
            ├── auth.py
            ├── climate.py
            ├── crops.py
            ├── news.py
            ├── reports.py
            ├── tasks.py
            └── users.py

## ⚙️ Requisitos

-   Python **3.10+**
-   pip
-   (Opcional) Docker y Docker Compose

## 🔧 Instalación manual

``` bash
git clone <url-del-repo>
cd agrombia-backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🐳 Instalación con Docker

``` bash
docker-compose up --build
```

## 🌱 Seed

``` bash
python seed.py
```

## 📌 Documentación

-   Swagger: http://localhost:8000/docs
-   ReDoc: http://localhost:8000/redoc
