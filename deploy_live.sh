#!/bin/bash

# ==============================================================================
# deploy_live.sh
#
# Automatisiert das Deployment von Aenderungen auf die Odoo Live-Umgebung.
# HOLT IMMER DEN 'main'-BRANCH.
# ==============================================================================

# --- Konfiguration ---
# Tragen Sie hier alle Ihre benutzerdefinierten Module ein.
MODULES_TO_UPDATE=(
    "kas_extension"
    "kas_contract"
    "odoo_chrome_pdf"
)

# Servicename in der docker-compose.yml
SERVICE_NAME="odoo-live"

# Datenbankname der Live-Umgebung
DATABASE_NAME="kas_odoo_live" # ACHTUNG: Sicherstellen, dass dies der korrekte Name ist!

# --- Skript-Logik (ab hier nichts aendern) ---

# Stoppt das Skript sofort, wenn ein Befehl fehlschlaegt.
set -e

# --- Schritt 1: Git-Repository aktualisieren ---
echo ">>> Schritt 1: Aktualisiere Git-Repository (Branch: main)..."
git fetch origin
git checkout main
git pull origin main
echo "Git-Repository ist auf dem neuesten Stand (main)."
echo

# --- Schritt 2: Docker-Container neu bauen und starten ---
echo ">>> Schritt 2: Fahre altes System herunter..."
docker-compose down

echo "Baue Images und starte System neu..."
docker-compose up -d --build
echo "Docker-System laeuft."
echo

# --- Schritt 3: Odoo-Module aktualisieren ---
echo ">>> Schritt 3: Aktualisiere Odoo-Module in der Datenbank '$DATABASE_NAME'..."

# Warte kurz, um sicherzustellen, dass der Odoo-Server vollstaendig gestartet ist
echo "Warte 15 Sekunden, bis Odoo bereit ist..."
sleep 15

for module in "${MODULES_TO_UPDATE[@]}"; do
    echo "Aktualisiere Modul: $module ..."
    docker-compose exec "$SERVICE_NAME" odoo -d "$DATABASE_NAME" -u "$module" --stop-after-init
done

echo "Alle Module erfolgreich aktualisiert."
echo

# --- Abschluss ---
echo "========================================"
echo "Deployment auf LIVE erfolgreich beendet."
echo "========================================"