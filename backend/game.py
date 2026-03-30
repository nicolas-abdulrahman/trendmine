import wikipedia
import random
import re

# Set language to Portuguese
wikipedia.set_lang("pt")

def complex_refinery(raw_title):
    """
    A complex refinery that uses Regex to transform raw Wikipedia 
    titles into clean, searchable Google Trends terms.
    """
    # 1. Remove disambiguation parentheses: "Neymar (futebolista)" -> "Neymar"
    # It handles nested or multiple parentheses
    clean = re.sub(r'\s*\([^)]*\)', '', raw_title)
    
    # 2. Remove "Category:" or "Categoria:" prefixes
    clean = re.sub(r'^(Category|Categoria):', '', clean, flags=re.IGNORECASE)
    
    # 3. Strip leading/trailing whitespace and underscores
    clean = clean.replace('_', ' ').strip()
    
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
        valid_themes = [c for c in page.categories if "Artigos" not in c and "!" not in c]
        
        if not valid_themes:
            return stochastic_data_miner() # Retry if no good theme found
            
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
            "seed_origin": random_page_title
        }

    except Exception:
        # Catching DisambiguationError or PageError and recursing
        return stochastic_data_miner()

# Execute
data = stochastic_data_miner()
print(f"📍 Discovery Origin: {data['seed_origin']}")
print(f"📂 Detected Theme: {data['theme']}")
print(f"⚔️  Battle: {data['competitor_a']} vs {data['competitor_b']}")