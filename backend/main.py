from rich.pretty import pprint
import json
import time
import uuid
from dataclasses import asdict, dataclass
from typing import Any, Dict
from game import get_query

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request, Response
from miner import SEEDS, mine
from pydantic import BaseModel
from pytrends.request import TrendReq
from fastapi.middleware.cors import CORSMiddleware  # ✅ correct
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, EmailStr
import db # Importa o arquivo criado acima


app = FastAPI(title="TrendMine API")
origins = [
    "http://localhost:5173",
    "http://127.0.0.1",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"], # Permite OPTIONS, POST, GET, etc.
    allow_headers=["*"], # Permite Content-Type, Authorization, etc.
)


pytrends = TrendReq(hl="pt-BR", tz=180)


@app.get("/seeds")
def list_seeds():
    """
    Retrieves all available seed topics.
    These seeds act as entry points for the data mining random walk.
    """
    return {"seeds": SEEDS}


from game import Item


@dataclass
class BattleOut:
    a: Item
    b: Item

@dataclass
class Session:
    battle: BattleOut
    seed: str
    timeout: int

class GuessPayload(BaseModel):
    battle_id: str
    guess: bool # True if user was correct, False otherwise

class PublicBattleOption(BaseModel):
    name: str
    page: str
    score: int

class PublicBattleOut(BaseModel):
    battle_id: str
    a: PublicBattleOption
    b: PublicBattleOption

active_battles: Dict[str, Session] = {}

defaults = {
    "football": ["Campeonato_Brasileiro_Série_A", "Brazil_Clubs"],
    "tech": ["Programming_languages"],
    "games": ["Category:Strategy_video_games", "Category:Adventure_games"]
}

def format_battle_response(battle_id: str, battle: BattleOut):
    """Helper to format internal dataclass to API response"""
    return {
        "battle_id": battle_id,
        "a": asdict(battle.a),
        "b": asdict(battle.b)
    }

@app.get("/battle", response_model=PublicBattleOut)
def get_battle(seed: str = Query(default="football")):
    if seed not in defaults:
        seed = "football"
    try:
        print("New Connection")
        opcao_a = get_query(seed, defaults[seed])
        opcao_b = get_query(seed, defaults[seed])

        while opcao_b.page == opcao_a.page:
            opcao_b = get_query(seed, defaults[seed])

        battle_id = str(uuid.uuid4())
        battle = BattleOut(a=opcao_a, b=opcao_b)

        active_battles[battle_id] = Session(battle, seed, 0)
        return format_battle_response(battle_id, battle)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/battle/guess", response_model=PublicBattleOut)
def resolve_guess(payload: GuessPayload):
    session = active_battles.get(payload.battle_id)
    if not session:
        # 402 as requested in your snippet
        raise HTTPException(status_code=402, detail="Battle session expired.")
    battle = session.battle
    seed = session.seed
    novo_a = get_query(seed, defaults[seed])
    novo_b = get_query(seed, defaults[seed])
    new_battle = BattleOut(novo_a, novo_b)
    session.battle = new_battle

    return format_battle_response(payload.battle_id, new_battle)


# --- Modelos Pydantic ---
class SignUpRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# --- Endpoints ---

@app.post("/sign_up")
def sign_up(payload: SignUpRequest):
    try:
        print("going to sign up", payload)
        pprint(payload)
        with db.get_db() as conn:
            cursor = conn.cursor()

            # 1. Inserir na tabela Account
            cursor.execute(
                "INSERT INTO Account (email, password) VALUES (?, ?)",
                (payload.email, payload.password)
            )
            account_id = cursor.lastrowid

            # 2. Inserir na tabela Profile vinculada ao account_id
            cursor.execute(
                "INSERT INTO Profile (name, score, account_id) VALUES (?, ?, ?)",
                (payload.name, 0, account_id)
            )

            conn.commit()
            print("signed in", account_id)
            return {"message": "Account created successfully", "account_id": account_id}

    except db.sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/log_in")
def log_in(payload: LoginRequest):
    with db.get_db() as conn:
        cursor = conn.cursor()

        # Busca a conta e o perfil em um único Join
        query = """
            SELECT Account.id, Account.email, Profile.name, Profile.score
            FROM Account
            JOIN Profile ON Account.id = Profile.account_id
            WHERE Account.email = ? AND Account.password = ?
        """
        cursor.execute(query, (payload.email, payload.password))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        return {
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "score": user["score"]
            }
        }
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
