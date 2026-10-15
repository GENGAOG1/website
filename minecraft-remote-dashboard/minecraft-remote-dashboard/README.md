# Minecraft Remote Dashboard – Starterprojekt

Flask-Dashboard mit Login und separatem Windows-Status-Client. Der Client sendet nur Hostname und Betriebssystem. Er führt **keine** Shell-Befehle aus, beendet keine Prozesse, löscht keine Dateien und streamt keinen Bildschirm.

## Lokal starten (Windows PowerShell)

Python 3.11+ installieren, im Projektordner:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FLASK_SECRET_KEY = "ein-langer-zufaelliger-secret-wert"
$env:ADMIN_PASSWORD_HASH = (python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('Ein-starkes-Passwort'))")
$env:CLIENT_TOKEN = "ein-langes-zufaelliges-token"
$env:COOKIE_SECURE = "false"
python app.py
```

Dashboard: http://127.0.0.1:5000

In einem zweiten Terminal:

```powershell
cd windows-client
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:SERVER_URL = "http://127.0.0.1:5000"
$env:CLIENT_TOKEN = "derselbe-token-wie-im-server"
python main.py
```

## Render deployen

1. Projekt in ein GitHub-Repository pushen.
2. Auf Render einen Web Service aus dem Repository erstellen und `render.yaml` verwenden.
3. `ADMIN_PASSWORD_HASH` in Render setzen. Hash lokal erzeugen:
   `python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('DEIN_STARKES_PASSWORT'))"`
4. `FLASK_SECRET_KEY` und `CLIENT_TOKEN` als geheime Umgebungsvariablen setzen. `COOKIE_SECURE=true` verwenden.
5. Den Windows-Client mit der HTTPS-URL des Render-Dienstes und demselben `CLIENT_TOKEN` konfigurieren.

## Grenzen & Sicherheit

- Statusdaten liegen nur im Arbeitsspeicher; Neustarts löschen sie. Für produktiven Einsatz Datenbank ergänzen.
- Kostenlose Hosting-Dienste können schlafen gehen; Heartbeats können verzögert sein.
- Bildschirmstreaming und Touch-Steuerung sind nicht enthalten. Verwende dafür eine etablierte Remote-Desktop-Lösung mit eigener Anmeldung und Gerätefreigabe.
- Verwende dieses Projekt nicht als einzige Notfallmaßnahme bei einem kompromittierten PC.
