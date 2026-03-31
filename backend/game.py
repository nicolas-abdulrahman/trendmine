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



from pytrends.request import TrendReq
import time

# Initialize Pytrends (Brazil context)
# hl='pt-BR' ensures we use Portuguese, tz=180 is Brazil's offset
pytrends = TrendReq(hl='pt-BR', tz=180)

def play_trends_game():
    print("🎮 Bem-vindo ao TrendMine 2026!")
    score = 0
    
    while True:
        # 1. MINE: Get our random pair from the miner we built
        data = stochastic_data_miner() # Using your previous function
        competitors = [data['competitor_a'], data['competitor_b']]
        
        print(f"\n📂 TEMA: {data['theme']}")
        print(f"1. {competitors[0]}")
        print(f"2. {competitors[1]}")
        
        choice = input("Quem teve mais buscas nos últimos 7 dias? (1 ou 2, ou 'sair'): ")
        if choice.lower() == 'sair': break

        # 2. FETCH: Get data from Google Trends
        print("📊 Consultando o Google Trends...")
        try:
            pytrends.build_payload(competitors, timeframe='now 7-d', geo='BR')
            df = pytrends.interest_over_time()
            
            if df.empty:
                print("⚠️  Dados insuficientes para essa dupla. Pulando...")
                continue

            # 3. COMPARE: Calculate mean interest
            avg_a = df[competitors[0]].mean()
            avg_b = df[competitors[1]].mean()
            
            winner_idx = "1" if avg_a > avg_b else "2"
            winner_name = competitors[0] if avg_a > avg_b else competitors[1]

            # 4. RESULTS
            print(f"\n📈 RESULTADOS:")
            print(f"{competitors[0]}: {round(avg_a, 1)}")
            print(f"{competitors[1]}: {round(avg_b, 1)}")

            if choice == winner_idx:
                score += 1
                print(f"✅ ACERTOU! O vencedor é {winner_name}. Combo: {score}")
            else:
                print(f"❌ ERROU! {winner_name} dominou as buscas.")
                score = 0
                
            # Anti-rate limit sleep (Google is sensitive!)
            time.sleep(2) 

        except Exception as e:
            print(f"🤯 Erro na API: {e}. Vamos tentar outra dupla...")
            time.sleep(5)
    print(f"📍 Discovery Origin: {data['seed_origin']}")
    print(f"📂 Detected Theme: {data['theme']}")
    print(f"⚔️  Battle: {data['competitor_a']} vs {data['competitor_b']}")
play_trends_game()
