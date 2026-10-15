import os
from datetime import datetime, timezone
from functools import wraps
from flask import Flask, jsonify, redirect, render_template, request, session, url_for, abort
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-change-me")
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "true").lower() == "true", SESSION_COOKIE_SAMESITE="Lax")
ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH", "")
CLIENT_TOKEN = os.environ.get("CLIENT_TOKEN", "")
latest_status = {"last_seen": None, "hostname": None, "platform": None}

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

def current_status():
    seen = latest_status["last_seen"]
    online = False
    if seen:
        try:
            online = (datetime.now(timezone.utc) - datetime.fromisoformat(seen)).total_seconds() < 90
        except ValueError:
            pass
    return {**latest_status, "online": online}

@app.get("/")
def index():
    return redirect(url_for("dashboard" if session.get("logged_in") else "login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if not ADMIN_PASSWORD_HASH:
            error = "ADMIN_PASSWORD_HASH ist nicht konfiguriert."
        elif check_password_hash(ADMIN_PASSWORD_HASH, request.form.get("password", "")):
            session.clear()
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            error = "Anmeldung fehlgeschlagen."
    return render_template("login.html", error=error)

@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.get("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", status=current_status())

@app.post("/api/heartbeat")
def heartbeat():
    if not CLIENT_TOKEN or request.headers.get("Authorization", "") != f"Bearer {CLIENT_TOKEN}":
        abort(401)
    body = request.get_json(silent=True) or {}
    latest_status.update(last_seen=datetime.now(timezone.utc).isoformat(), hostname=str(body.get("hostname", "unknown"))[:100], platform=str(body.get("platform", "unknown"))[:100])
    return jsonify(ok=True)

@app.get("/api/status")
@login_required
def api_status():
    return jsonify(current_status())

@app.get("/health")
def health():
    return jsonify(ok=True)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
