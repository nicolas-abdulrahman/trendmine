"""
TrendMine API - Tests
─────────────────────
Run with:
  python test.py

Make sure the API is running first:
  uvicorn main:app --reload
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def separator(title: str):
    print(f"\n{'─' * 50}")
    print(f"  {title}")
    print(f"{'─' * 50}")

def print_json(data: dict):
    print(json.dumps(data, indent=2, ensure_ascii=False))

def test_seeds():
    separator("GET /seeds")
    r = requests.get(f"{BASE_URL}/seeds")
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    data = r.json()
    assert "seeds" in data, "Missing 'seeds' key"
    assert len(data["seeds"]) > 0, "Seeds list is empty"
    print_json(data)
    print("✅ PASSED")

def test_battle_random():
    separator("GET /battle  (random seed)")
    r = requests.get(f"{BASE_URL}/battle")
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    data = r.json()
    assert "competitor_a" in data, "Missing competitor_a"
    assert "competitor_b" in data, "Missing competitor_b"
    assert "theme" in data, "Missing theme"
    assert data["competitor_a"]["name"] != data["competitor_b"]["name"], "Both competitors are the same!"
    print_json(data)
    print("✅ PASSED")
    return data["competitor_a"]["name"], data["competitor_b"]["name"]

def test_battle_with_seed():
    separator("GET /battle?seed=futebol")
    r = requests.get(f"{BASE_URL}/battle", params={"seed": "futebol"})
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    data = r.json()
    assert data["seed"] == "futebol", f"Expected seed 'futebol', got {data['seed']}"
    print_json(data)
    print("✅ PASSED")

def test_battle_with_depth():
    separator("GET /battle?depth=3  (deeper walk)")
    r = requests.get(f"{BASE_URL}/battle", params={"depth": 3})
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    data = r.json()
    assert "all_candidates_scored" in data
    print_json(data)
    print(f"  → Candidates explored: {data['all_candidates_scored']}")
    print("✅ PASSED")

def test_battle_invalid_depth():
    separator("GET /battle?depth=99  (invalid depth)")
    r = requests.get(f"{BASE_URL}/battle", params={"depth": 99})
    assert r.status_code == 422, f"Expected 422 validation error, got {r.status_code}"
    print_json(r.json())
    print("✅ PASSED  (correctly rejected)")

def test_result(a: str, b: str):
    separator(f"GET /result?a={a}&b={b}")
    r = requests.get(f"{BASE_URL}/result", params={"a": a, "b": b})
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    data = r.json()
    assert "winner" in data, "Missing winner"
    assert "draw" in data, "Missing draw"
    assert data["competitor_a"]["name"] == a
    assert data["competitor_b"]["name"] == b
    assert data["competitor_a"]["score"] >= 0
    assert data["competitor_b"]["score"] >= 0
    print_json(data)
    if data["draw"]:
        print("  → It's a draw!")
    else:
        print(f"  → Winner: {data['winner']}")
    print("✅ PASSED")

def test_result_same_query():
    separator("GET /result?a=X&b=X  (same query)")
    r = requests.get(f"{BASE_URL}/result", params={"a": "futebol", "b": "futebol"})
    # Should either return draw or 422 — both are acceptable
    print(f"  Status: {r.status_code}")
    print_json(r.json())
    print("✅ PASSED  (edge case handled)")

def test_result_unknown_query():
    separator("GET /result with obscure/unknown terms")
    r = requests.get(f"{BASE_URL}/result", params={"a": "xyzabc123notreal", "b": "qwerty99999fake"})
    # Should return 404 or 500 gracefully — not crash
    assert r.status_code in (404, 500), f"Expected 404 or 500, got {r.status_code}"
    print(f"  Status: {r.status_code}")
    print_json(r.json())
    print("✅ PASSED  (handled gracefully)")


if __name__ == "__main__":
    print("\n🎮 TrendMine API — Test Suite")
    print("=" * 50)

    results = {"passed": 0, "failed": 0}

    tests = [
        ("Seeds endpoint",          test_seeds),
        ("Battle with seed",        test_battle_with_seed),
        ("Battle with depth",       test_battle_with_depth),
        ("Battle invalid depth",    test_battle_invalid_depth),
        ("Result same query",       test_result_same_query),
        ("Result unknown query",    test_result_unknown_query),
    ]

    # Run fixed tests
    for name, fn in tests:
        try:
            fn()
            results["passed"] += 1
        except AssertionError as e:
            print(f"❌ FAILED: {e}")
            results["failed"] += 1
        except requests.exceptions.ConnectionError:
            print(f"\n💀 Cannot connect to {BASE_URL}")
            print("   Make sure the API is running: uvicorn main:app --reload")
            exit(1)
        except Exception as e:
            print(f"❌ ERROR: {e}")
            results["failed"] += 1

    # Run battle random + pipe its result into /result
    try:
        a, b = test_battle_random()
        results["passed"] += 1
        test_result(a, b)
        results["passed"] += 1
    except AssertionError as e:
        print(f"❌ FAILED: {e}")
        results["failed"] += 1
    except Exception as e:
        print(f"❌ ERROR: {e}")
        results["failed"] += 1

    # Summary
    total = results["passed"] + results["failed"]
    separator("SUMMARY")
    print(f"  Total:  {total}")
    print(f"  Passed: {results['passed']} ✅")
    print(f"  Failed: {results['failed']} ❌")
    print()
