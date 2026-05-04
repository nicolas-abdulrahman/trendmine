import json
import time
import uuid
from dataclasses import asdict, dataclass
from typing import Any, Dict
from game import get_query

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from miner import SEEDS, mine
from pydantic import BaseModel
from pytrends.request import TrendReq

app = FastAPI(title="TrendMine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
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
    guess: str


active_battles: Dict[str, Session] = {}


class PublicBattleOption(BaseModel):
    name: str
    page: str


class PublicBattleOut(BaseModel):
    battle_id: str
    a: PublicBattleOption
    b: PublicBattleOption


defaults = {
    "football": ["Campeonato_Brasileiro_Série_A", "Brazil_Clubs"],
    "tech":["Programming_languages", "Software_companies"],
    "games":["Category:Strategy_video_games" ,"Category:Adventure_games"]
}

@app.get("/battle", response_model=PublicBattleOut)
def get_battle(seed: str = Query(default=None), depth: int = Query(default=2)):
    """
    Initializes a new battle session.
    Generates two competitors, creates a unique battle ID, stores the session in memory,
    and returns the public-facing battle data (excluding the scores).
    """
    try:
        opcao_a = get_query(seed, defaults[seed])
        opcao_b = get_query(seed, defaults[seed])

        battle_id = str(uuid.uuid4())
        battle = BattleOut(a=opcao_a, b=opcao_b)

        battle_dict = asdict(battle)
        battle_dict["battle_id"] = battle_id

        session = Session(battle, seed,0 )
        active_battles[battle_id] = session

        return battle_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class GuessResultData(BaseModel):
    is_correct: bool
    correct_answer: str
    score_a: int
    score_b: int


class GuessResponse(BaseModel):
    result: GuessResultData
    next_battle: PublicBattleOut


@app.post("/battle/guess", response_model=GuessResponse)
def resolve_guess(payload: GuessPayload):
    session = active_battles.get(payload.battle_id)
    if not session:
        raise HTTPException(
            status_code=402, detail="Battle ID not found or already answered."
        )

    battle = session.battle
    seed = session.seed # Retrieve the seed used for this specific session

    score_a = battle.a.score
    score_b = battle.b.score

    # Determine winner
    if score_a >= score_b:
        correct_option = "a"
    else:
        correct_option = "b"

    is_correct = payload.guess == correct_option

    # Remove old session
    del active_battles[payload.battle_id]

    new_battle_id = str(uuid.uuid4())

    if is_correct:
        # User is correct: Keep the winner and get a new challenger
        winner = battle.a if correct_option == "a" else battle.b
        novo_desafiante = get_query(seed, defaults[seed])

        # Avoid duplicate
        while novo_desafiante.page == winner.page:
            novo_desafiante = get_query(seed, defaults[seed])

        new_battle = BattleOut(a=winner, b=novo_desafiante)
    else:
        # User is wrong: Reset with two completely new items
        novo_a = get_query(seed, defaults[seed])
        novo_b = get_query(seed, defaults[seed])
        new_battle = BattleOut(a=novo_a, b=novo_b)

    # Save new session (preserving the seed)
    active_battles[new_battle_id] = Session(battle=new_battle, seed=seed, timeout=0)

    return {
        "result": {
            "is_correct": is_correct,
            "correct_answer": correct_option,
            "score_a": score_a,
            "score_b": score_b,
        },
        "next_battle": {
            "battle_id": new_battle_id,
            "a": {"name": new_battle.a.name, "page": new_battle.a.page},
            "b": {"name": new_battle.b.name, "page": new_battle.b.page}
        },
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
