#!/bin/bash
# ==============================================================================
# deploy_live.sh
#
# Deployment für Odoo LIVE (Testserver-Live-Instanz).
#
# Verwendung:
#   ./deploy_live.sh                # nimmt main
#   ./deploy_live.sh <branch_name>  # nimmt angegebenen Branch
#
# Verhalten:
#   - bricht ab, wenn Working Tree dirty ist (Schutz vor unbeabsichtigtem Verlust)
#   - setzt den lokalen Branch hart auf origin/<branch>
#   - baut Container neu und führt Modul-Upgrades via Odoo-CLI im Container aus
# ==============================================================================

set -euo pipefail

# --- Konfiguration ---
BRANCH="${1:-main}"

MODULES_TO_UPDATE=(
  "kas_extension"
  "kas_contract"
  "odoo_chrome_pdf"
)

SERVICE_NAME="odoo-live"
DATABASE_NAME="kas_odoo_live"
ODOO_CONF="/etc/odoo/odoo.conf"

# --- Schutz: keine lokalen uncommitted Änderungen überschreiben ---
if [[ -n "$(git status --porcelain)" ]]; then
  echo "ERROR: Working Tree hat lokale Änderungen/untracked Files."
  echo "Bitte committen/stashen oder bereinigen, bevor deploy_live.sh läuft."
  echo
  git status --porcelain
  exit 1
fi

echo ">>> Schritt 1: Git auf Branch '${BRANCH}' aktualisieren (hart auf origin/${BRANCH})..."
git fetch origin

# Branch lokal auf Remote-Stand setzen (funktioniert auch, wenn Branch lokal noch nicht existiert)
git checkout -B "${BRANCH}" "origin/${BRANCH}"
git reset --hard "origin/${BRANCH}"
git clean -fd
echo "Git OK."
echo

echo ">>> Schritt 2: Docker neu bauen und starten (LIVE)..."
docker-compose down
docker-compose up -d --build
echo "Docker läuft."
echo

echo ">>> Schritt 3: Odoo-Module upgraden (DB: ${DATABASE_NAME})..."
echo "Warte 15 Sekunden, bis Odoo bereit ist..."
sleep 15

for module in "${MODULES_TO_UPDATE[@]}"; do
  echo "Upgrade: ${module}"
  docker-compose exec "${SERVICE_NAME}" odoo \
    -c "${ODOO_CONF}" \
    -d "${DATABASE_NAME}" \
    -u "${module}" \
    --stop-after-init \
    --workers=0 \
    --max-cron-threads=0
done

echo
echo "========================================"
echo "Deployment LIVE erfolgreich beendet."
echo "Branch: ${BRANCH}"
echo "========================================"
