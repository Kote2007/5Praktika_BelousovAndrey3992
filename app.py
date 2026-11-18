#6 Вариант, 3 практика, Белоусов Андрей
import json
import os
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse



#Параметры типа порта и сообщения + штуки для сохранки приколов
PORT = int(os.getenv("PORT", "8006"))
MESSAGE = os.getenv("MESSAGE", "Attendance online")
DATA_DIR = os.getenv("DATA_DIR", "./data")
STATE_FILE = os.path.join(DATA_DIR, "state.json")

#Система поиска... времени)
def utc_now(): return (datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"))

#Загрузка файлика
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f: data = json.load(f)

        return {
            "requests": int(data.get("requests") or 0),
            "present": int(data.get("present") or 0),
        }
    return {
        "requests": 0,
        "present": 0,
    }

#Сохранение или создание файлика
def save_state(state):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f: json.dump(state, f, ensure_ascii=False, indent=2)


STATE = load_state()
save_state(STATE)

#Главный класс для HTTP
class Handler(BaseHTTPRequestHandler):
    def send_json(self, status_code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path.rstrip("/") or "/"

        if path == "/attendance":
            STATE["requests"] += 1
            STATE["present"] += 1
            save_state(STATE)

            self.send_json(
                200,
                {
                    "message": MESSAGE,
                    "present": STATE["present"],
                    "generated_at": utc_now(),
                },
            )
        elif path == "/health":
            STATE["requests"] += 1
            save_state(STATE)

            self.send_json(200, {"status": "ok"})
        else:
            STATE["requests"] += 1
            save_state(STATE)

            self.send_json(404, {"error": "not_found"})

#Ну и main :3
if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)

    print(
        f"Starting service on 0.0.0.0:{PORT}; "
        f"state file: {os.path.abspath(STATE_FILE)}"
    )

    server = HTTPServer(("0.0.0.0", PORT), Handler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping service...")
    finally:
        server.server_close()
