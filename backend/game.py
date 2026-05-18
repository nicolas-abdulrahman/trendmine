import json
import random
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from pprint import pprint
from typing import Dict, List

import requests
import wikipediaapi
from bs4 import BeautifulSoup

from data import GAME_DATA
import requests
import random
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass


@dataclass
class Item:
    name: str
    page: str
    score: int

@dataclass
class Data:
    page: str
    score: int


def get_query(seed: str, keys ) -> Item:
    """
    Selects a random item from target_sections[seed],
    fetches its display name and pageview score.
    """
    if seed not in GAME_DATA:
        raise ValueError(f"Seed '{seed}' not found in target sections.")

    # Get a random category/key from the seed
    random_key = random.choice(keys)

    # Get a random wikipedia slug from that category
    wikipedia_slug = random.choice(GAME_DATA[seed][random_key])
    score = wikipedia_slug.score
    
    name = wikipedia_slug.page.replace("_", " ")
 #   name = get_first_caption(wikipedia_slug, seed)
 #   score = get_pageviews(wikipedia_slug, seed)
    item = Item(
        name=name,
        page=wikipedia_slug.page,
        score=score
    )
    print(item)
    return item

