import json

def load_leaderboard():
    try:
        with open('leaderboard.json', 'r') as f:
            return json.load(f)
    except:
        return []

def save_score(name, items, dist):
    #items — это сумма монет и бонусов
    total_score = (items * 10) + int(dist // 10)
    
    data = load_leaderboard()
    data.append({
        "name": name, 
        "score": total_score, 
        "dist": int(dist)
    })
    
    # Сортируем и оставляем топ-10
    data = sorted(data, key=lambda x: x['score'], reverse=True)[:10]
    
    with open('leaderboard.json', 'w') as f:
        json.dump(data, f, indent=4)

# Функции для Пункта 3.5 (Settings)
def save_settings(settings):
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

def load_settings():
    # Настройки по умолчанию
    default = {"sound": True, "car_color": "red", "difficulty": "Medium"}
    try:
        with open('settings.json', 'r') as f:
            return json.load(f)
    except:
        return default
