import random
import re
from pprint import pprint

import ollama
import wikipediaapi

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
]


def get_neighbours(seed):
    num_links = 25
    page = wiki.page(seed)
    relevant_links = []
    for section in page.sections:
        pprint(section)
        # Verifica se o título da seção é um dos que queremos
        if section.title in target_sections:
            # Pega os links que aparecem no texto desta seção
            # (Usando a lógica de comparação de texto que vimos antes)
            section_links = [l for l in page.links if l in section.text]
            relevant_links.extend(section_links)
            break
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


if __name__ == "__main__":
    from users import TEAMS

    neighbours = get_neighbours(TEAMS[0])
    pprint(neighbours)


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
