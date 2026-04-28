"""
Stochastic Data Miner
─────────────────────
Uses a random walk + mathematical scoring to discover
battle pairs organically from Google Trends data.

Algorithm:
  1. Pick a random seed from a diverse pool
  2. Use pytrends.suggestions() to explore neighbors (the graph walk)
  3. Fetch interest_over_time() for all candidates
  4. Score each with:
       • mean      → popularity
       • std       → volatility (how much it's trending)
       • CV        → coefficient of variation (std / mean) — the main weight
  5. Weighted random sample 2 candidates (high CV = more likely chosen)
  6. Return the pair + the detected theme
"""

import random
import time
from pathlib import Path
from pprint import pprint

import numpy as np
import pytrends
from pandas.io.api import read_json
from pytrends.request import TrendReq, json

pytrends = TrendReq(hl="pt-BR", tz=180)

# Small diverse seeds — just entry points for the walk, not the final pool
SEEDS = [
    "futebol",
    "música",
    "tecnologia",
    "cinema",
    "política",
    "games",
    "moda",
    "gastronomia",
    "esportes",
    "séries",
    "carros",
    "viagem",
    "celebridades",
    "economia",
    "saúde",
]


def _getzrelated_queries():
    file = read_json(Path(r".\data\04-27-2026-07-35\football_trends.json"))
    # sample = file[0]["relatedQueries_rising"].sample(5)

    def filter():
        from transformers import AutoModelForCausalLM, AutoTokenizer

        model_name = "Qwen/Qwen2.5-0.5B-Instruct"

        model = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype="auto", device_map="auto"
        )
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        messages = [
            # 1. The Rules (System)
            {
                "role": "system",
                "content": """You are a strict data extraction API for a Brazilian football game.
                RULES:
                1. If the query is related to football, set "relevant" to true and extract the core entities.
                2. If completely unrelated, set "relevant" to false and "core_query" to null.
                3. You MUST respond in pure JSON format.""",
            },
            # --- YOUR EXAMPLES START HERE ---
            # Example 1: A good query with filler words
            {
                "role": "user",
                "content": "onde assistir Sao paulo x palmeiras",
            },
            {
                "role": "assistant",
                "content": '{"relevant": true, "core_query": "Sao paulo x palmeiras"}',
            },
            {
                "role": "user",
                "content": "estatísticas de seleção brasileira x seleção francesa de futebol hoje",
            },
            {
                "role": "assistant",
                "content": '{"relevant": true, "core_query": "seleção brasileira x seleção francesa de futebol"}',
            },
        ]
        text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

        generated_ids = model.generate(**model_inputs, max_new_tokens=512)
        generated_ids = [
            output_ids[len(input_ids) :]
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[
            0
        ]
        return response_text

    return filter()


def get_related_queries(user):
    with open(Path(f"data/football.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    all_categories = list(data.keys())

    # 3. Pick one category at random
    chosen_category = random.choice(all_categories)

    # 4. Grab the list of words associated with that category
    category_words = data[chosen_category]
    return random.sample(category_words, 2)


def get_random_valid_topics(
    seed: str, depth: int, cookie: str, proxies
) -> list[object]:
    import requests

    kw_list = [seed]  # Futebol /m/02vx4

    session = requests.Session()
    session.headers.update({"Cookie": cookie})

    pytrend = TrendReq(hl="pt-BR", tz=180, proxies=proxies)
    pytrend.build_payload(kw_list, timeframe="today 12-m", geo="BR")

    original_get_data = pytrend._get_data

    def intercept_json(*args, **kwargs):
        raw_json = original_get_data(*args, **kwargs)
        print("\n--- RAW GOOGLE JSON RESPONSE ---")
        print(json.dumps(raw_json, indent=2))
        print("--------------------------------\n")
        # Return it back to pytrends so it can try (and possibly fail) to parse it
        return raw_json

    pytrend._get_data = intercept_json
    try:
        topics = pytrend.related_topics()
    except IndexError:
        print("crashed as expected")
    return []
    # top_football = topics["m/02vx4"]["top"]
    # return top_football.sample(10)


def walk(seed: str, depth: int = 2) -> list[dict]:
    """
    Random walk starting from seed using Google Trends suggestions.

    Args:
        seed:  Starting keyword for the walk (e.g. "futebol")
        depth: Number of hops to perform

    Returns:
        List of suggestion dicts e.g. [{"title": "Marta", "type": ""}, ...]
    """
    candidates = []
    current = seed

    for _ in range(depth):
        try:
            suggestions = pytrends.suggestions(current)
            if not suggestions:
                break

            # Filter out type == "Topic" noise, keep concrete entities
            valid = [s for s in suggestions if s.get("type") == ""]
            if not valid:
                valid = suggestions

            likely = random.choices(valid, weights=range(len(valid), 0, -1), k=5)
            candidates.extend(likely)

            current = likely[0]["title"]
            time.sleep(random.uniform(1.0, 2.5))

        except Exception:
            break

    return candidates


def score_candidates(titles: list[str]) -> dict[str, dict]:
    """
    Fetch interest_over_time for up to 5 candidates at once,
    compute statistical scores for each.

    Returns:
      { title: { mean, std, cv, raw } }

    CV (coefficient of variation) = std / mean
    High CV means the topic is volatile/trending — more interesting for battles.
    """
    scores = {}
    # pytrends accepts max 5 at once
    chunks = [titles[i : i + 5] for i in range(0, len(titles), 5)]

    for chunk in chunks:
        try:
            pytrends.build_payload(chunk, timeframe="now 7-d", geo="BR")
            df = pytrends.interest_over_time()

            if df.empty:
                continue

            for title in chunk:
                if title not in df.columns:
                    continue
                series = df[title].astype(float)
                mean = series.mean()
                std = series.std()
                cv = std / (mean + 1e-9)  # avoid div by zero

                scores[title] = {
                    "mean": round(mean, 2),
                    "std": round(std, 2),
                    "cv": round(cv, 4),
                }

            time.sleep(0.5)

        except Exception:
            continue

    return scores


def weighted_sample(scores: dict[str, dict], k: int = 2) -> list[str]:
    """
    Sample k candidates using their CV as weights.
    Higher CV → more likely to be picked.
    Ensures the two picks are different.
    """
    titles = list(scores.keys())
    weights = [scores[t]["cv"] + 0.01 for t in titles]  # +0.01 avoids zero weights

    # Normalize weights to probabilities
    total = sum(weights)
    probs = [w / total for w in weights]

    chosen = np.random.choice(titles, size=k, replace=False, p=probs).tolist()
    return chosen


def mine(seed: str = "", depth: int = 2) -> dict:
    """
    Full pipeline:
      seed → walk → score → sample → return battle pair
    """
    if seed is None:
        seed = random.choice(SEEDS)

    # 1. Walk the graph
    candidates_raw = walk(seed, depth=depth)

    print("Canditates raw:")
    pprint(candidates_raw, sort_dicts=False)
    print("--------------")
    if len(candidates_raw) < 2:
        # fallback: retry with a fresh seed
        return mine(depth=depth)

    # Deduplicate by title
    seen = set()
    unique = []
    for c in candidates_raw:
        t = c["title"]
        if t not in seen:
            seen.add(t)
            unique.append(t)

    # 2. Score them
    scores = score_candidates(unique)

    print("Scores:")
    pprint(scores, sort_dicts=False)
    print("--------------")

    # Need at least 2 scoreable candidates
    if len(scores) < 2:
        return mine(depth=depth)

    # 3. Weighted sample
    pair = weighted_sample(scores, k=2)

    print("Pair:")
    pprint(pair, sort_dicts=False)
    print("--------------")

    a, b = pair[0], pair[1]

    return {
        "seed": seed,
        "theme": seed.capitalize(),
        "competitor_a": {
            "name": a,
            "stats": scores[a],
        },
        "competitor_b": {
            "name": b,
            "stats": scores[b],
        },
        "all_candidates_scored": len(scores),
    }
