# DreamTeamETL

## Primer paso

1. Construir y levantar los servicios:

    ```sh
    docker-compose up -d --build
    ```

2. Ejecutar `app.py` dentro del contenedor `app`:

    ```sh
    docker-compose exec app python app.py
    ```

3. Ejecutar `import.py` dentro del contenedor `app`:

    ```sh
    docker-compose exec app python import.py
    ```

---

### Descripción

DreamTeamETL es un proyecto de extracción, transformación y carga (ETL) que transfiere datos de una base de datos MongoDB a una base de datos Neo4j. Sigue los pasos anteriores para construir y ejecutar los servicios Docker necesarios para el proyecto.

#### Requisitos

- Docker
- Docker Compose

#### Estructura del Proyecto

