#!/bin/bash

# Levantar los contenedores
docker-compose up -d --build

# Esperar a que el contenedor de la aplicación esté listo
echo "Esperando a que el contenedor de la aplicación esté listo..."
until docker-compose exec app bash -c 'exit 0' 2>/dev/null; do
    sleep 1
done

# Ejecutar app.py
docker-compose exec app python app.py

# Ejecutar mongo_neo.py después de que app.py haya terminado
docker-compose exec app python import.py