import json
import random
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from pprint import pprint
from typing import Dict, List

import ollama
import requests
import wikipediaapi
from bs4 import BeautifulSoup

# Set language to Portuguese


class Game:
    category = "football"
    points = 0


wiki = wikipediaapi.Wikipedia(
    user_agent="MeuJogoDeFutebol/1.0 (contato@email.com)", language="pt"
)
target_sections = [
    "Carreira",
    "Clubes",
    "Seleção Brasileira",
    "Seleção Nacional",
    "Títulos",
    "Conquistas",
    "História",
    "Ídolos",
    "Jogadores notáveis",
    "Rivalidades",
    "Estatísticas",
    "Outros",
]

trivia_categories = {
    "football": {
        "Campeonato_Brasileiro_Série_A": [
            "Club_Athletico_Paranaense",
            "Clube_Atlético_Mineiro",
            "Esporte_Clube_Bahia",
            "Botafogo_FR",
            "Associação_Chapecoense_de_Futebol",
            "Sport_Club_Corinthians_Paulista",
            "Coritiba_Foot_Ball_Club",
            "Cruzeiro_EC",
            "CR_Flamengo",
            "Fluminense_FC",
            "Grêmio_FBPA",
            "SC_Internacional",
            "Mirassol_Futebol_Clube",
            "SE_Palmeiras",
            "Red_Bull_Bragantino",
            "Clube_do_Remo",
            "Santos_FC",
            "São_Paulo_FC",
            "CR_Vasco_da_Gama",
            "Esporte_Clube_Vitória"
        ],
        "Brazil_Clubs": [
            # Rio de Janeiro (The Giants)
            "CR_Flamengo", "Fluminense_FC", "Botafogo_de_Futebol_e_Regatas", "CR_Vasco_da_Gama",
            "Bangu_Atlético_Clube", "America_Football_Club_(Rio_de_Janeiro)", "Volta_Redonda_Futebol_Clube",

            # São Paulo (The Giants & Traditional)
            "Sport_Club_Corinthians_Paulista", "São_Paulo_FC", "SE_Palmeiras", "Santos_FC",
            "Associação_Portuguesa_de_Desportos", "Guarani_Futebol_Clube", "Associação_Atlética_Ponte_Preta",
            "Red_Bull_Bragantino", "Ituano_Futebol_Clube", "Botafogo_Futebol_Clube_(SP)",

            # Minas Gerais
            "Clube_Atlético_Mineiro", "Cruzeiro_Esporte_Clube", "América_Futebol_Clube_(MG)",
            "Tombense_Futebol_Clube", "Ipatinga_Esporte_Clube", "Villa_Nova_Atlético_Clube", "Tupi_Football_Club",

            # Rio Grande do Sul
            "Grêmio_Foot-Ball_Porto_Alegrense", "Sport_Club_Internacional", "Esporte_Clube_Juventude",
            "Sociedade_Esportiva_e_Recreativa_Caxias_do_Sul", "Brasil_de_Pelotas", "Ypiranga_Futebol_Clube",

            # Paraná
            "Club_Athletico_Paranaense", "Coritiba_Foot_Ball_Club", "Paraná_Clube",
            "Londrina_Esporte_Clube", "Operário_Ferroviário_Esporte_Clube", "Maringá_Futebol_Clube",

            # Pernambuco
            "Sport_Club_do_Recife", "Clube_Náutico_Capibaribe", "Santa_Cruz_Futebol_Clube",
            "Retrô_Futebol_Clube_Brasil", "Central_Sport_Club", "Salgueiro_Atlético_Clube",

            # Bahia
            "Esporte_Clube_Bahia", "Esporte_Clube_Vitória", "Associação_Desportiva_Bahia_de_Feira",
            "Fluminense_de_Feira_Futebol_Clube", "Sociedade_Desportiva_Juazeirense",

            # Ceará
            "Fortaleza_Esporte_Clube", "Ceará_Sporting_Club", "Ferroviário_Atlético_Clube_(CE)",
            "Icasa", "Floresta_Esporte_Clube",

            # Santa Catarina
            "Associação_Chapecoense_de_Futebol", "Avaí_FC", "Figueirense_Futebol_Clube",
            "Criciúma_Esporte_Clube", "Joinville_Esporte_Clube", "Brusque_Futebol_Clube",

            # Goiás
            "Goiás_Esporte_Clube", "Atlético_Clube_Goianiense", "Vila_Nova_Futebol_Clube",
            "Associação_Atlética_Aparecidense", "Anápolis_Futebol_Clube",

            # Others (Northeast & North)
            "Sampaio_Corrêa_Futebol_Clube", "Moto_Club_de_São_Luís", "Centro_Sportivo_Alagoano",
            "Clube_de_Regatas_Brasil", "ABC_Futebol_Clube", "América_Futebol_Clube_(RN)",
            "Paysandu_Sport_Club", "Clube_do_Remo", "Manaus_Futebol_Clube"
        ],
        "Campeonato_Brasileiro_Série_B": [
            "América_Futebol_Clube_(MG)",
            "Athletic_Club_(MG)",
            "Atlético_Clube_Goianiense",
            "Avaí_FC",
            "Botafogo_Futebol_Clube_(SP)",
            "Ceará_Sporting_Club",
            "Clube_de_Regatas_Brasil",
            "Criciúma_Esporte_Clube",
            "Cuiabá_Esporte_Clube",
            "Fortaleza_Esporte_Clube",
            "Goiás_Esporte_Clube",
            "Esporte_Clube_Juventude",
            "Londrina_Esporte_Clube",
            "Clube_Náutico_Capibaribe",
            "Grêmio_Novorizontino",
            "Operário_Ferroviário_Esporte_Clube",
            "Associação_Atlética_Ponte_Preta",
            "São_Bernardo_Futebol_Clube",
            "Sport_Club_do_Recife",
            "Vila_Nova_Futebol_Clube"
        ],
        "Global_Football_Teams": [
            "Argentina_national_football_team",
            "Bolivia_national_football_team",
            "Brazil_national_football_team",
            "Chile_national_football_team",
            "Colombia_national_football_team",
            "Ecuador_national_football_team",
            "Paraguay_national_football_team",
            "Peru_national_football_team",
            "Uruguay_national_football_team",
            "Venezuela_national_football_team",

            # UEFA (Europe)
            "Austria_national_football_team",
            "Belgium_national_football_team",
            "Croatia_national_football_team",
            "Czech_Republic_national_football_team",
            "Denmark_national_football_team",
            "England_national_football_team",
            "France_national_football_team",
            "Germany_national_football_team",
            "Hungary_national_football_team",
            "Italy_national_football_team",
            "Netherlands_national_football_team",
            "Norway_national_football_team",
            "Poland_national_football_team",
            "Portugal_national_football_team",
            "Scotland_national_football_team",
            "Serbia_national_football_team",
            "Spain_national_football_team",
            "Sweden_men's_national_football_team",
            "Switzerland_national_football_team",
            "Turkey_national_football_team",
            "Ukraine_national_football_team",

            # CAF (Africa)
            "Algeria_national_football_team",
            "Cameroon_national_football_team",
            "Egypt_national_football_team",
            "Ghana_national_football_team",
            "Ivory_Coast_national_football_team",
            "Morocco_national_football_team",
            "Nigeria_national_football_team",
            "Senegal_national_football_team",
            "South_Africa_national_football_team",
            "Tunisia_national_football_team",

            # AFC (Asia/Oceania)
            "Australia_national_football_team",
            "Iran_national_football_team",
            "Japan_national_football_team",
            "Qatar_national_football_team",
            "Saudi_Arabia_national_football_team",
            "South_Korea_national_football_team",

            # CONCACAF (North/Central America)
            "Canada_men's_national_soccer_team",
            "Costa_Rica_national_football_team",
            "Mexico_national_football_team",
            "United_States_men's_national_soccer_team"
        ]
    },
    "games": [
        "Category:Role-playing_video_games",
        "Category:Puzzle_video_games",
        "Category:Simulation_video_games",
        "Category:Adventure_games",
        "Category:Strategy_video_games"
    ],
    "tech": {
        "Programming_languages": [
            "C_(programming_language)",
            "C_Sharp_(programming_language)",
            "Clojure",
            "Elixir_(programming_language)",
            "Erlang_(programming_language)",
            "Go_(programming_language)",
            "Haskell",
            "Java_(programming_language)",
            "JavaScript",
            "Julia_(programming_language)",
            "Kotlin",
            "Lisp_(programming_language)",
            "Lua",
            "Nim_(programming_language)",
            "Perl",
            "PHP",
            "Python_(programming_language)",
            "Ruby_(programming_language)",
            "Swift_(programming_language)",
            "TypeScript",
            "Zig_(programming_language)",
            "Rust_(programming_language)",
            "Fortran",
            "COBOL",
            "Pascal_(programming_language)",
            "Objective-C",
            "Assembly_language",
            "Smalltalk",
            "Scala_(programming_language)",
            "Dart_(programming_language)",
            "OCaml"
        ],
        "software": [
            "1Password", "9GAG", "Adblock_Plus", "AllTrails", "Amazon_Prime_Video",
            "Amazon_Music", "Audible_(service)", "AutoCAD", "Avast_Antivirus",
            "Babbel", "BBC_iPlayer", "BitTorrent_(software)", "Bitwarden",
            "Blogger_(service)", "CamScanner", "CapCut", "ChatGPT_(mobile_app)",
            "Chess.com", "Crunchyroll", "Discord", "Disney+", "DeepL_Translator",
            "DuckDuckGo", "Duolingo", "eBay", "ES_File_Explorer", "Evernote",
            "FaceApp", "Facebook", "Firefox_for_Android", "Fitbit", "Flickr",
            "Flipboard", "Gboard", "Google_Assistant", "Google_Earth",
            "Google_Gemini", "Google_Maps", "HBO_Max", "Hulu", "IBeer",
            "Instagram", "Jamboard", "Kodi_(software)", "Krita", "Last.fm",
            "Lyft", "Malwarebytes_(software)", "Mercado_Libre", "Microsoft_Copilot",
            "Microsoft_Teams", "Musical.ly", "MX_Player", "MyFitnessPal",
            "Myspace", "Netflix", "Notion_(productivity_software)", "Obsidian_(software)",
            "OkCupid", "OneDrive", "OpenTable", "Pandora_(service)"
        ],
        "Software_companies": [
            "Adobe_Inc.", "Alphabet_Inc.", "Amazon_(company)", "Apple_Inc.",
            "Asana,_Inc.", "Autodesk", "Automattic", "Backblaze", "BMC_Software",
            "Box,_Inc.", "Cadence_Design_Systems", "Citrix_Systems", "Cloudera",
            "Cloudflare", "Coursera", "Datadog", "Google", "Intuit", "Microsoft",
            "Oracle_Corporation", "Docker,_Inc.", "Docusign", "Dropbox",
            "ElevenLabs", "Epic_Systems", "Esri", "F5,_Inc.", "Fastly",
            "HashiCorp", "Hewlett_Packard_Enterprise", "HP_Inc.", "HubSpot",
            "IBM", "Intel", "ITA_Software", "iZotope", "Jamf", "Joyent",
            "JW_Player", "MathWorks", "McAfee", "MongoDB_Inc.", "Mozilla_Corporation",
            "New_Relic", "Okta,_Inc.", "Palantir", "Panic_Inc.", "PARC_(company)",
            "Perforce", "Perplexity_AI", "Plex", "Pluralsight", "PreSonus",
            "Puppet_(software)", "Qualtrics", "Red_Hat"
        ],
        "programming_concepts": [
            "Bubble_sort", "Quicksort", "Insertion_sort", "Merge_sort",
            "Binary_search_algorithm", "Dijkstra's_algorithm", "A*_search_algorithm",
            "Big_O_notation", "Time_complexity", "Space_complexity",
            "Dynamic_programming", "Greedy_algorithm",
            "Inheritance_(object-oriented_programming)",
            "Polymorphism_(computer_science)",
            "Encapsulation_(computer_programming)",
            "Abstraction_(computer_science)",
            "Class_(computer_programming)",
            "Object_(computer_science)",
            "Method_(computer_programming)",
            "Interface_(object-oriented_programming)",
            "Constructor_(object-oriented_programming)",
            "Destructor_(computer_science)",
            "Instance_variable",
            "Method_overriding",
            "Method_overloading",
            "Associative_array",
            "Array_(data_structure)",
            "Linked_list",
            "Stack_(abstract_data_type)",
            "Queue_(abstract_data_type)",
            "Set_(abstract_data_type)",
            "Binary_tree",
            "B-tree",
            "Hash_table",
            "Graph_(abstract_data_type)",
            "Heap_(data_structure)",
            "Recursion_(computer_science)",
            "Closure_(computer_programming)",
            "Functional_programming",
            "Object-oriented_programming",
            "Asynchronous_I/O",
            "Multithreading_(computer_architecture)",
            "Concurrency_(computer_science)",
            "Deadlock_(computer_science)",
            "Garbage_collection_(computer_science)",
            "Memory_leak",
            "Application_programming_interface",
            "Regular_expression",
            "Dependency_injection",
            "Compiler",
            "Interpreter_(computing)",
            "Virtual_machine"
        ]
    }
}



teams = {
    "Pernambucano - Série A1": [
        "Sport Club do Recife",
        "Clube Náutico Capibaribe",
        "Santa Cruz Futebol Clube",
        "Retrô Futebol Clube",
        "Maguary Futebol Clube",
        "Decisão Sertânia Esporte Clube",
        "Jaguar Esporte Clube",
        "Associação Acadêmica e Desportiva Vitória das Tabocas",
    ],
    "Copa do Nordeste": [
        "Sport Club do Recife",
        "Retrô Futebol Clube",
        "Clube de Regatas Brasil",  # CRB
        "Agremiação Sportiva Arapiraquense",  # ASA
        "Esporte Clube Vitória",  # Vitória-BA
        "Associação Atlética Juazeirense",  # Juazeirense
        "Jacuipense Esporte Clube",
        "Ceará Sporting Club",
        "Fortaleza Esporte Clube",
        "Ferroviário Atlético Clube",
        "Maranhão Atlético Clube",
        "Esporte Clube Imperatriz",
        "Esporte Clube Sousa",
        "Botafogo Futebol Clube (João Pessoa)",  # Botafogo-PB
        "Esporte Clube Piauí",
        "Fluminense Esporte Clube (Teresina)",  # Fluminense-PI
        "ABC Futebol Clube",
        "América Futebol Clube (Rio Grande do Norte)",  # América-RN
        "Associação Desportiva Itabaiana",
        "Associação Desportiva Confiança",
    ],
    "Brasileirão - Série B": [
        "Sport Club do Recife",
        "Clube Náutico Capibaribe",
        "Ceará Sporting Club",
        "Fortaleza Esporte Clube",
        "Clube de Regatas Brasil",  # CRB
        "Athletic Club",  # Athletic-MG
        "América Futebol Clube (Belo Horizonte)",  # América-MG
        "Botafogo Futebol Clube (Ribeirão Preto)",  # Botafogo-SP
        "Grêmio Novorizontino",
        "São Bernardo Futebol Clube",
        "Associação Atlética Ponte Preta",
        "Avaí Futebol Clube",
        "Criciúma Esporte Clube",
        "Esporte Clube Juventude",
        "Londrina Esporte Clube",
        "Operário Ferroviário Esporte Clube",
        "Vila Nova Futebol Clube",
        "Atlético Clube Goianiense",
        "Cuiabá Esporte Clube",
        "Goiás Esporte Clube",
    ],
}

# Flat deduplicated list of all unique teams






def get_neighbours(seed):
    num_links = 25
    page = wiki.page(seed)
    relevant_links = []
    for section in page.sections:
        print(section.title)
        # Verifica se o título da seção é um dos que queremos
        if section.title in target_sections:
            # Pega os links que aparecem no texto desta seção
            # (Usando a lógica de comparação de texto que vimos antes)
            section_links = [l for l in page.links if l in section.text]
            relevant_links.extend(section_links)
    all_links = relevant_links
    print(all_links)
    selected_links = random.sample(all_links, min(num_links, len(all_links)))
    selected_links = [a for a in selected_links if len(a.split()) < 4]
    result = []
    for link in selected_links:
        result.append(evaluate(link))
    result = list(zip(selected_links, result))
    pprint(result)
    top_two = sorted(result, key=lambda x: x[1], reverse=True)[:2]
    return top_two

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

def get_first_caption(page_title: str) -> str:
    url = "https://pt.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": page_title,
        "prop": "text",
        "format": "json",
        "redirects": 1  # Automatically follow redirects
    }
    headers = {
        "User-Agent": "trendmine/1.0 (your@email.com)"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            return ""

        data = response.json()
        if "error" in data:
            return ""

        html = data["parse"]["text"]["*"]
        soup = BeautifulSoup(html, "html.parser")

        # Look for caption in infoboxes or tables
        caption = soup.find("caption")
        if caption:
            return caption.get_text(strip=True)

        # Fallback: if no caption, return the page title cleaned up
        return page_title.replace("_", " ")
    except Exception:
        return page_title.replace("_", " ")

def get_pageviews(wikipedia_name: str, days: int = 30) -> int:
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)

    # Wikimedia API requires underscores instead of spaces
    slug = wikipedia_name.replace(" ", "_")

    url = (
        f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"
        f"/pt.wikipedia/all-access/all-agents"
        f"/{slug}"
        f"/daily"
        f"/{start.strftime('%Y%m%d')}00/{end.strftime('%Y%m%d')}00"
    )

    try:
        response = requests.get(url, headers={"User-Agent": "trendmine/1.0 (your@email.com)"})
        if response.status_code != 200:
            return 0

        data = response.json()
        return sum(item["views"] for item in data.get("items", []))
    except Exception:
        return 0

# Example target_sections structure for the function to work
# target_sections = {"football": {"teams": ["Sport_Club_do_Recife", "Clube_Náutico_Capibaribe"]}}

def get_query(seed: str, keys ) -> Item:
    """
    Selects a random item from target_sections[seed],
    fetches its display name and pageview score.
    """
    if seed not in trivia_categories:
        raise ValueError(f"Seed '{seed}' not found in target sections.")

    # Get a random category/key from the seed
    random_key = random.choice(keys)

    # Get a random wikipedia slug from that category
    wikipedia_slug = random.choice(trivia_categories[seed][random_key])

    # Fetch the name and score
    name = get_first_caption(wikipedia_slug)
    score = get_pageviews(wikipedia_slug)

    return Item(
        name=name,
        page=wikipedia_slug,
        score=score
    )

def save_to_json(section: str,
    teams: Dict[str, List[str]], output_path: Path = Path("data/teams.json")
):
    array:List[DataItem]= []
    for team in teams[section]:
        team = team.replace(' ', '_')
        name = get_first_caption(team)
        if name == "":
            print("error at ",team)
            continue
        score = get_pageviews(team)
        data = DataItem(name=name, page=team, score=score)  # ← fixed constructor
        array.append(data)  # ← was append() with no arg

    # ← new_dict.json_dump doesn't exist; convert dataclasses to dicts first
    serializable =  [ asdict(team) for team in array]

    write_to_file(section, serializable, output_path)

def write_to_file(name, data, output_path: Path = Path("data/teams copy.json")):
    existing = {}
    if output_path.exists():
        with open(output_path, "r", encoding="utf-8") as f:
            existing = json.load(f)
    existing[name] = data
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved to '{output_path}'")


def evaluate(query: str) -> float:
    messages = [
        {
            "role": "system",
            "content": "Your job is to classify if a given input is related to Soccer. Answer ONLY with a value between 0 to 1. Provide exactly one score per line. Do not add any extra text, letters, or explanation.",
        },
        {"role": "user", "content": query},
    ]
    response = ollama.chat(
        # model="hf.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF:Q3_K_M",
        model="qwen2.5:1.5b",
        messages=messages,
        options={
            "num_ctx": 128,  # SHRINK THE SCRATCHPAD: Only reserve RAM for 512 tokens
            "temperature": 0.1,  # Make it strictly logical, no creative rambling
        },
    )
    print(response)
    response_text = response["message"]["content"]
    print(response_text)
    try:
        return float(response_text)
    except ValueError:
        return 0.0

    scores = []
    response_lines = response_text.strip().split("\n")
    for line in response_lines:
        try:
            scores.append(float(line.strip()))
        except ValueError:
            scores.append(0.01)

    while len(scores) < len(queries):
        scores.append(0.02)
    return scores[: len(queries)]


    # neighbours = get_neighbours(TEAMS[0])
    # pprint(neighbours)


def complex_refinery(raw_title):
    """
    A complex refinery that uses Regex to transform raw Wikipedia
    titles into clean, searchable Google Trends terms.
    """
    # 1. Remove disambiguation parentheses: "Neymar (futebolista)" -> "Neymar"
    # It handles nested or multiple parentheses
    clean = re.sub(r"\s*\([^)]*\)", "", raw_title)

    # 2. Remove "Category:" or "Categoria:" prefixes
    clean = re.sub(r"^(Category|Categoria):", "", clean, flags=re.IGNORECASE)

    # 3. Strip leading/trailing whitespace and underscores
    clean = clean.replace("_", " ").strip()

    # 4. Complexity Check: If the title is too long (likely a description, not an entity),
    # we truncate it to the first 4 words to keep it "searchable."
    words = clean.split()
    if len(words) > 4:
        clean = " ".join(words[:4])

    return clean


def stochastic_data_miner():
    """
    Random Walk Algorithm:
    1. Jump to a random page.
    2. Extract its categories to find a 'Theme'.
    3. Pick a neighbor from that theme for a fair battle.
    """
    try:
        # Step 1: Stochastic Jump
        random_page_title = wikipedia.random(pages=1)
        page = wikipedia.page(random_page_title, auto_suggest=False)

        # Step 2: Extract Categories (Filtering out 'Hidden' or 'Maintenance' categories)
        # We look for categories that don't contain "Artigos" or "!Esboços"
        valid_themes = [
            c for c in page.categories if "Artigos" not in c and "!" not in c
        ]

        if not valid_themes:
            return stochastic_data_miner()  # Retry if no good theme found

        chosen_theme = random.choice(valid_themes)
        clean_theme = complex_refinery(chosen_theme)

        # Step 3: Get 'Neighbors' from the Category
        cat_page = wikipedia.page(chosen_theme, auto_suggest=False)
        neighbors = cat_page.links

        if len(neighbors) < 2:
            return stochastic_data_miner()

        # Step 4: Refine the Final Entities
        competitors = random.sample(neighbors, 2)
        entity_a = complex_refinery(competitors[0])
        entity_b = complex_refinery(competitors[1])

        return {
            "theme": clean_theme,
            "competitor_a": entity_a,
            "competitor_b": entity_b,
            "seed_origin": random_page_title,
        }

    except Exception:
        # Catching DisambiguationError or PageError and recursing
        return stochastic_data_miner()

def flatten(path: Path) -> Path:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    flattened = [item for section in data.values() for item in section]

    # dedup by "page", keeping first occurrence
    seen = set()
    deduped = []
    for item in flattened:
        if item["page"] not in seen:
            seen.add(item["page"])
            deduped.append(item)

    output_path = path.with_stem(path.stem + "_flattened")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(deduped, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved to '{output_path}' ({len(flattened) - len(deduped)} duplicates removed)")
    return output_path
if __name__ == "__main__":
    from users import TEAMS
    item= get_query()
    pprint(item)
    # write_to_file("bob", [asdict(DataItem(name="bob", page="booob", score=2))])
    # save_to_json("Brasileirão - Série B",teams)
    # flatten(Path("data/teams.json"))
