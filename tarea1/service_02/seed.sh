#!/bin/bash

# Crear equipos en service_02 con IDs fijos

# Palestino
curl -X POST http://localhost:5002/teams \
-H "Content-Type: application/json" \
-d '{
  "team_id": "66ba5abbcbe14991232f41a6",
  "name": "Club Deportivo Palestino S.A.D.P",
  "country": "Chile",
	"description": "Club chileno fundado en 8 Agosto 1920. Estadio Municial de la Cisterna"
}'

# Colo-Colo
curl -X POST http://localhost:5002/teams \
-H "Content-Type: application/json" \
-d '{
  "team_id": "66ba5a9ccbe14991232f41a1",
  "name": "Club Social y Deportivo Colo-Colo",
  "country": "Chile",
	"description": "Club chileno fundado en 19 Abril 1925. Estadio Monumental (Metro Pedrero, Macul, Santiago)"
}'

