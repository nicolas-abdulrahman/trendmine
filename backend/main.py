from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pytrends.request import TrendReq
from miner import mine, SEEDS
import time

app = FastAPI(title="TrendMine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

pytrends = TrendReq(hl='pt-BR', tz=180)


@app.get("/seeds")
def list_seeds():
    """List all available seeds (entry points for the random walk)."""
    return {"seeds": SEEDS}


@app.get("/battle")
def get_battle(
    seed: str = Query(default=None, description="Optional seed topic. Random if omitted."),
    depth: int = Query(default=2, ge=1, le=4, description="Walk depth (1-4). Higher = more diverse."),
):
    """
    Run the data mining algorithm and return a battle pair.

    The algorithm:
      1. Starts from seed (or picks random)
      2. Walks the pytrends suggestion graph
      3. Scores all found candidates mathematically (mean, std, CV)
      4. Weighted-samples 2 using CV as weight

    Returns the pair + their trend stats.
    """
    try:
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
        pytrends.build_payload([a, b], timeframe='now 7-d', geo='BR')
        df = pytrends.interest_over_time()

        if df.empty:
            raise HTTPException(status_code=404, detail="No trend data found for this pair.")

        score_a = round(float(df[a].mean()), 1)
        score_b = round(float(df[b].mean()), 1)
        draw    = score_a == score_b
        winner  = None if draw else (a if score_a > score_b else b)

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
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)