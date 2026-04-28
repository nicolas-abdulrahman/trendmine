import json
import time
from dataclasses import asdict, dataclass

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from miner import SEEDS, mine
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
    """List all available seeds (entry points for the random walk)."""
    return {"seeds": SEEDS}


@dataclass
class BattleOption:
    readable_name: str
    wikipedia_link: str
    score: int


@dataclass
class BattleOut:
    a: BattleOption
    b: BattleOption


@app.get("/battle")
def get_battle(
    seed: str = Query(
        default=None, description="Optional seed topic. Random if omitted."
    ),
    depth: int = Query(
        default=2, ge=1, le=4, description="Walk depth (1-4). Higher = more diverse."
    ),
):
    opcao_a = BattleOption(
        readable_name="Náutico", wikipedia_link="Clube_Náutico_Capibaribe", score=250
    )
    opcao_b = BattleOption(
        readable_name="Sport", wikipedia_link="Sport_Club_do_Recife", score=321
    )
    battle = BattleOut(a=opcao_a, b=opcao_b)
    try:
        return asdict(battle)
        return json.dumps(asdict(battle), indent=4, ensure_ascii=False)
        result = mine(seed=seed, depth=depth)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/result")
def get_result(a: str, b: str):
    """
    Compare 2 queries on Google Trends and return who won.
    Usage: /result?a=Neymar&b=Mbappé
    """
    try:
        time.sleep(1)
        pytrends.build_payload([a, b], timeframe="now 7-d", geo="BR")
        df = pytrends.interest_over_time()

        if df.empty:
            raise HTTPException(
                status_code=404, detail="No trend data found for this pair."
            )

        score_a = round(float(df[a].mean()), 1)
        score_b = round(float(df[b].mean()), 1)
        draw = score_a == score_b
        winner = None if draw else (a if score_a > score_b else b)

        return {
            "competitor_a": {"name": a, "score": score_a},
            "competitor_b": {"name": b, "score": score_b},
            "winner": winner,
            "draw": draw,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    print("Starting API on http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
