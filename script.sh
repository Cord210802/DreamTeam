until nc -z neo4j 7687; do
  echo "Esperando a que Neo4j esté disponible..."
  sleep 2
done