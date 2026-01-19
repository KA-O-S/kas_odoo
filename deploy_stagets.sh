#!/bin/bash
# ==============================================================================
# deploy_stage.sh
#
# Deployment für Odoo STAGE.
#
# Verwendung:
#   ./deploy_stage.sh                # nimmt main
#   ./deploy_stage.sh <branch_name>  # nimmt angegebenen Branch
# ==============================================================================

set -euo pipefail

BRANCH="${1:-main}"

MODULES_TO_UPDATE=(
  "kas_extension"
  "kas_contract"
  "odoo_chrome_pdf"
)

SERVICE_NAME="odoo-stage"
DATABASE_NAME="STAGE_20240405121108"
ODOO_CONF="/etc/odoo/odoo.conf"

if [[ -n "$(git status --porcelain)" ]]; then
  echo "ERROR: Working Tree hat lokale Änderungen/untracked Files."
  echo "Bitte committen/stashen oder bereinigen, bevor deploy_stage.sh läuft."
  echo
  git status --porcelain
  exit 1
fi

echo ">>> Schritt 1: Git auf Branch '${BRANCH}' aktualisieren (hart auf origin/${BRANCH})..."
git fetch origin
git checkout -B "${BRANCH}" "origin/${BRANCH}"
git reset --hard "origin/${BRANCH}"
git clean -fd
echo "Git OK."
echo

echo ">>> Schritt 2: Docker neu bauen und starten (STAGE)..."
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
echo "Deployment STAGE erfolgreich beendet."
echo "Branch: ${BRANCH}"
echo "========================================"
