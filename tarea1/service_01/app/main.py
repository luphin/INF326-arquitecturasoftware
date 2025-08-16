import logging
from time import sleep
from pymongo import MongoClient
from bson.objectid import ObjectId
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
mongodb_client = MongoClient("service_01_mongodb", 27017)

# Configuración de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[
        # Volumen compartido
        logging.FileHandler("/logs/service_01.log"),
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

    def __init__(self, **kargs):
        if "_id" in kargs:
            kargs["id"] = str(kargs["_id"])
        BaseModel.__init__(self, **kargs)


@app.get("/")
async def root():
    logging.info("Endpoint raíz accedido service 01")
    return {"status": "ok"}


@app.get("/players", response_model=list[Player])
def players_all(team_id: str | None = None):
    logging.info(f"Obteniendo todos los jugadores (team_id={team_id})")
    filters = {}

    sleep(3)

    if team_id:
        filters["team_id"] = team_id
        logging.info(f"Filtrando jugadores por team_id={team_id}")

    players = [Player(**player)
               for player in mongodb_client.service_01.players.find(filters)]
    logging.info(f"Total de jugadores retornados: {len(players)}")
    return players


@app.get("/players/{player_id}")
def players_get(player_id: str):
    logging.info(f"Obteniendo jugador con id={player_id}")
    player_doc = mongodb_client.service_01.players.find_one(
        {"_id": ObjectId(player_id)})
    if not player_doc:
        logging.warning(f"No se encontró jugador con id={player_id}")
        return {"error": "Jugador no encontrado"}
    return Player(**player_doc)


@app.delete("/players/{player_id}")
def players_delete(player_id: str):
    logging.info(f"Eliminando jugador con id={player_id}")
    result = mongodb_client.service_01.players.delete_one(
        {"_id": ObjectId(player_id)})
    if result.deleted_count == 0:
        logging.warning(f"No se eliminó ningún jugador con id={player_id}")
    else:
        logging.info(f"Jugador eliminado: {player_id}")
    return {"status": "ok"}


@app.post("/players")
def players_create(player: Player):
    logging.info(f"Creando nuevo jugador: {player.name}")
    inserted_id = mongodb_client.service_01.players.insert_one(
        player.dict()).inserted_id
    new_player = Player(
        **mongodb_client.service_01.players.find_one({"_id": ObjectId(inserted_id)}))
    logging.info(f"Nuevo jugador creado con id={new_player.id}")
    return new_player
