from enum import Enum

import logging
import requests
from pymongo import MongoClient
from bson.objectid import ObjectId

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()
mongodb_client = MongoClient("service_02_mongodb", 27017)

# Configuración de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[
        # Volumen compartido
        logging.FileHandler("/logs/service_02.log"),
        logging.StreamHandler()  # Consola
    ]
)


class Player(BaseModel):
    id: str | None = None
    name: str
    age: int
    number: int
    team_id: str | None = None
    description: str = ""


class Country(str, Enum):
    chile = 'Chile'
    portugal = 'Portugal'
    españa = 'España'
    francia = "Francia"


class Team(BaseModel):
    team_id: str
    name: str
    country: Country
    description: str = ""


@app.get("/")
async def root():
    logging.info("Endpoint raíz accedido")
    return {"status": "ok"}


def get_players_of_a_team(team_id) -> list[Player]:
    url = f"http://service_01:80/players?team_id={team_id}"
    logging.info(f"Obteniendo jugadores para team_id={team_id} desde {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        players = response.json()
        logging.info(
            f"Se obtuvieron {len(players)} jugadores"
            f" para team_id={team_id}"
        )
        return players
    except requests.RequestException as e:
        logging.error(
            f"Error al obtener jugadores para team_id={team_id}: {e}")
        return []


@app.get("/teams")
def teams_all(expand: list[str] = Query(default=[])):
    logging.info("Listando todos los equipos")
    teams = [Team(**team).dict()
             for team in mongodb_client.service_02.teams.find({})]

    if expand and 'players' in expand:
        logging.warning("Problema n+1: obteniendo jugadores de cada equipo")
        for i, team in enumerate(teams):
            teams[i]["players"] = get_players_of_a_team(team['team_id'])
    logging.info(f"Total de equipos retornados: {len(teams)}")
    return teams


@app.get("/teams/{team_id}")
def teams_get(team_id: str, expand: list[str] = Query(default=[])):
    logging.info(f"Obteniendo equipo con team_id={team_id}")
    team_doc = mongodb_client.service_02.teams.find_one({"team_id": team_id})
    if not team_doc:
        logging.warning(f"Equipo no encontrado: {team_id}")
        return {"error": "Equipo no encontrado"}

    team = Team(**team_doc).dict()
    if expand and 'players' in expand:
        team["players"] = get_players_of_a_team(team_id)
    logging.info(f"Equipo obtenido: {team['name']}")
    return team


@app.delete("/teams/{team_id}")
def teams_delete(team_id: str):
    logging.info(f"Eliminando equipo con team_id={team_id}")
    result = mongodb_client.service_02.teams.delete_one({"team_id": team_id})
    if result.deleted_count == 0:
        logging.warning(f"No se eliminó ningún equipo para team_id={team_id}")
    else:
        logging.info(f"Equipo eliminado: {team_id}")
    return {"status": "ok"}


@app.post("/teams")
def teams_create(team: Team):
    logging.info(f"Creando nuevo equipo: {team.name}")
    inserted_id = mongodb_client.service_02.teams.insert_one(
        team.dict()).inserted_id
    new_team = Team(
        **mongodb_client.service_02.teams.find_one({"_id": ObjectId(inserted_id)}))
    logging.info(f"Nuevo equipo creado con team_id={new_team.team_id}")
    return new_team
