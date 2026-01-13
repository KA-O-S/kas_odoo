#!/bin/bash

# ==============================================================================
# deploy_stage.sh
#
# Automatisiert das Deployment von Aenderungen auf die Odoo Stage-Umgebung.
#
# Verwendung:
#   ./deploy_stage.sh [branch_name]
#
#   - Wenn kein Branch-Name angegeben wird, wird der aktuell ausgecheckte
#     Branch verwendet.
# ==============================================================================

# --- Konfiguration ---
# Tragen Sie hier alle Ihre benutzerdefinierten Module ein.
MODULES_TO_UPDATE=(
    "kas_extension"
    "kas_contract"
    "odoo_chrome_pdf"
)

# Servicename in der docker-compose.yml
SERVICE_NAME="odoo-stage"

# Datenbankname der Stage-Umgebung
DATABASE_NAME="STAGE_20240405121108"

# --- Skript-Logik (ab hier nichts aendern) ---

# Stoppt das Skript sofort, wenn ein Befehl fehlschlaegt.
set -e

# Branch-Name aus dem ersten Argument des Skripts uebernehmen, falls vorhanden
BRANCH=${1}

# --- Schritt 1: Git-Repository aktualisieren ---
echo ">>> Schritt 1: Aktualisiere Git-Repository..."
git fetch origin

if [ -n "$BRANCH" ]; then
    echo "Wechsle zu Branch '$BRANCH' und hole neuesten Stand..."
    git checkout "$BRANCH"
    git pull origin "$BRANCH"
else
    echo "Hole neuesten Stand des aktuellen Branches..."
    git pull
fi
echo "Git-Repository ist auf dem neuesten Stand."
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
echo "Deployment auf STAGE erfolgreich beendet."
echo "========================================"