import pprint
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def run_test():
    # 1. Start Battle
    print("--- Testing GET /battle ---")
    res = requests.get(f"{BASE_URL}/battle?seed=football")
    if res.status_code != 200:
        print(f"Failed: {res.text}")
        return

    data = res.json()
    battle_id = data["battle_id"]
    score_a = data["a"]["score"]
    score_b = data["b"]["score"]

    print(f"Received Battle: {data['a']['name']} ({score_a}) vs {data['b']['name']} ({score_b})")

    # 2. Simulate User Choice (Picking higher score)
    # The frontend knows the scores, so it decides 'guess' locally
    user_choice_is_correct = True # Simulating a correct click

    print(f"\n--- Testing POST /battle/guess (Correct choice) ---")
    payload = {
        "battle_id": battle_id,
        "guess": user_choice_is_correct
    }

    res_guess = requests.post(f"{BASE_URL}/battle/guess", json=payload)

    if res_guess.status_code == 200:
        next_battle = res_guess.json()
        print("Success! Next Battle Received:")
        print(f"A: {next_battle['a']['name']} (Score: {next_battle['a']['score']})")
        print(f"B: {next_battle['b']['name']} (Score: {next_battle['b']['score']})")

        # Verify if winner was kept (since guess was True)
        winner_name = data['a']['name'] if score_a >= score_b else data['b']['name']
        if next_battle['a']['name'] == winner_name or next_battle['b']['name'] == winner_name:
            print("\n✅ Logic Verified: Winner was kept.")

            pprint.pprint(next_battle)
        else:
            print("\n❌ Logic Error: Winner was not kept despite correct guess.")
    else:
        print(f"Failed: {res_guess.status_code} - {res_guess.text}")

if __name__ == "__main__":
    run_test()
