"""Minimal status client: sends metadata only, no shell commands or desktop control."""
import os, platform, socket, time
import requests
from dotenv import load_dotenv
load_dotenv()
SERVER_URL = os.environ.get("SERVER_URL", "").rstrip("/")
CLIENT_TOKEN = os.environ.get("CLIENT_TOKEN", "")
INTERVAL = max(15, int(os.environ.get("HEARTBEAT_INTERVAL", "30")))

def main():
    if not SERVER_URL.startswith("https://") and not SERVER_URL.startswith("http://127.0.0.1"):
        raise SystemExit("SERVER_URL muss HTTPS nutzen (lokal ist 127.0.0.1 erlaubt).")
    if not CLIENT_TOKEN:
        raise SystemExit("CLIENT_TOKEN fehlt.")
    headers = {"Authorization": f"Bearer {CLIENT_TOKEN}"}
    payload = {"hostname": socket.gethostname(), "platform": platform.platform()}
    print(f"Status-Client läuft: {SERVER_URL}")
    while True:
        try:
            r = requests.post(f"{SERVER_URL}/api/heartbeat", json=payload, headers=headers, timeout=10)
            r.raise_for_status()
            print("Heartbeat erfolgreich.")
        except requests.RequestException as e:
            print(f"Heartbeat fehlgeschlagen: {e}")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
