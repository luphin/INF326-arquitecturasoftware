# Crear equipo Barcelona
curl -X POST http://localhost:5002/teams \
-H "Content-Type: application/json" \
-d '{
  "team_id": "66ba5abbcbe14991232f41a3",
  "name": "Club de Deportes San Luis de Quillota",
  "country": "Chile",
  "description": "Club chileno fundado en 1919. Estadio Bicentenario Lucio Fariña."
}'


# Crear equipo Barcelona
curl -X POST http://localhost:5002/teams \
-H "Content-Type: application/json" \
-d '{
  "team_id": "66ba5abbcbe14991232f41b1",
  "name": "Fútbol Club Barcelona",
  "country": "España",
  "description": "Club español fundado en 1899. Estadio Camp Nou."
}'

# Crear equipo Real Madrid
curl -X POST http://localhost:5002/teams \
-H "Content-Type: application/json" \
-d '{
  "team_id": "66ba5abbcbe14991232f41b2",
  "name": "Real Madrid Club de Fútbol",
  "country": "España",
  "description": "Club español fundado en 1902. Estadio Santiago Bernabéu."
}'
