# Architektur

Browser -> Flask-Dashboard auf Render -> authentifizierte Heartbeats vom Windows-Client.
Der Client meldet ausschließlich Statusmetadaten. Bildschirm-/Eingabesteuerung bleibt in einer separat abgesicherten Remote-Desktop-Komponente.
