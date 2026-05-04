import json
import requests

# Certifique-se de que o servidor FastAPI esteja rodando na porta 8000
BASE_URL = "http://127.0.0.1:8000"

def testar_palpite_dinamico(seed="football"):
    print(f"1. ⚔️ Solicitando uma nova batalha (Seed: {seed})...")
    # Adicionando o parâmetro seed para garantir o contexto correto
    response_get = requests.get(f"{BASE_URL}/battle?seed={seed}")

    if response_get.status_code != 200:
        print(f"❌ Erro ao buscar batalha: {response_get.text}")
        return

    battle_data = response_get.json()
    battle_id = battle_data["battle_id"]

    op_a = battle_data["a"]
    op_b = battle_data["b"]

    print(f"✅ Batalha recebida! ID: {battle_id[:8]}...")
    print(f"   Opção A: {op_a['name']} ({op_a['page']})")
    print(f"   Opção B: {op_b['name']} ({op_b['page']})")

    # Tenta encontrar o Sport ou apenas escolhe a Opção A por padrão
    palpite = "a"
    nome_palpite = op_a['name']

    if "Sport" in op_b['name']:
        palpite = "b"
        nome_palpite = op_b['name']
    elif "Sport" in op_a['name']:
        palpite = "a"
        nome_palpite = op_a['name']
    else:
        print(f"⚠️ 'Sport' não veio nesta rodada. Palpitando na Opção A: {nome_palpite}")

    print(f"\n2. 🎯 Enviando o palpite: '{palpite}' ({nome_palpite})...")

    # Payload ajustado para o novo Pydantic BaseModel (GuessPayload)
    payload = {
        "battle_id": battle_id,
        "guess": palpite
    }

    response_post = requests.post(f"{BASE_URL}/battle/guess", json=payload)

    if response_post.status_code != 200:
        print(f"❌ Erro ao enviar palpite: {response_post.status_code} - {response_post.text}")
        return

    resultado = response_post.json()

    print("\n3. 🏆 Resultado da Rodada:")
    print(json.dumps(resultado["result"], indent=4, ensure_ascii=False))

    print("\n4. ⏭️ Próxima Batalha (Gerada para a próxima rodada):")
    print(json.dumps(resultado["next_battle"], indent=4, ensure_ascii=False))

if __name__ == "__main__":
    # Testando com a categoria football
    testar_palpite_dinamico("football")
