# Verwenden Sie das offizielle Odoo-Image als Basis
FROM odoo:17.0

# Wechseln Sie zum root-Benutzer fuer die Installation von Paketen
USER root

# Schritt 1: Python-Abhaengigkeiten installieren
RUN pip3 install playwright aiohttp requests
RUN pip3 uninstall -y greenlet gevent && pip3 install --no-cache-dir greenlet gevent

# Schritt 2: System-Abhaengigkeiten und Diagnose-Werkzeuge als ROOT installieren
RUN apt-get update && apt-get install -y --no-install-recommends libnss3 libxss1 libasound2 libatk-bridge2.0-0 libgtk-3-0 libgbm-dev \
    strace \
    && rm -rf /var/lib/apt/lists/*

# Schritt 3: Definieren Sie eine Umgebungsvariable fuer den systemweiten Browser-Pfad
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/playwright

# Schritt 4: Installieren des Playwright-Browsers an diesen systemweiten Ort
RUN playwright install chromium

# Berechtigungen fuer Odoo-Datenverzeichnis setzen
RUN mkdir -p /var/lib/odoo && chown -R odoo:odoo /var/lib/odoo

# Zurueck zum odoo-Benutzer fuer den normalen Betrieb
USER odoo