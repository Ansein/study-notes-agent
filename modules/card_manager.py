# modules/card_manager.py
import os, json, random

def _card_path(subject):
    base = os.path.join("data", "cards")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, f"{subject}_cards.json")

def generate_card(subject, question, answer):
    path = _card_path(subject)
    card = {"question": question, "answer": answer}
    if os.path.exists(path):
        cards = json.load(open(path, "r", encoding="utf-8"))
    else:
        cards = []
    cards.append(card)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)

def get_random_card():
    base = "data/cards"
    if not os.path.exists(base):
        return "暂无复习卡片", ""
    files = [f for f in os.listdir(base) if f.endswith(".json")]
    if not files:
        return "暂无复习卡片", ""
    file = random.choice(files)
    cards = json.load(open(os.path.join(base, file), "r", encoding="utf-8"))
    card = random.choice(cards)
    return card["question"], card["answer"]
