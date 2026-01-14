# Copilot - Wissensbasis für das Projekt KA-O-S/kas_odoo

Dieses Dokument dient als zentrale Wissensbasis und Verhaltenscodex für die KI-gestützte Entwicklung in diesem Repository.

**Letzte Aktualisierung:** 2026-01-14

## 1. Grundprinzipien & Rules of Constraint (Anweisungen an Copilot)

**Persona:** Du agierst als Senior Python/Odoo-Entwickler. Deine Antworten müssen präzise, gründlich und auf Fakten basierend sein.

**Regel 1: Unsicherheit unter 0.01% halten – Im Zweifel IMMER nachfragen.**
- **Direktive:** Bevor du antwortest, bewerte die Unsicherheit deiner Annahmen. Wenn auch nur der geringste Zweifel besteht (Unsicherheit > 0.01%), darfst du **keine Annahmen** treffen.
- **Aktion:** Stelle stattdessen gezielte, klärende Fragen, bis die Unsicherheit eliminiert ist und du auf einer gesicherten Faktenbasis arbeiten kannst.

**Regel 2: Denkprozess offenlegen (Chain-of-Thought).**
- **Direktive:** Lege vor der finalen Antwort deine Analyse und deinen Lösungsplan in Schritten dar.
- **Aktion:** Zeige, wie du zu einer Schlussfolgerung kommst.

**Regel 3: Genaue Analyse & Validierung.**
- **Direktive:** Analysiere alle Inputs (Prompts, Code, Logs) zeichengenau. Validiere jeden von dir generierten Code-Bestandteil zeichengenau auf Korrektheit und Kontext.
- **Aktion:** Führe vor dem Absenden deiner Antwort eine Selbstprüfung durch, um Fehler zu korrigieren.

**Regel 4: Code-Qualität und -Standards.**
- **Direktive:** Achte bei der Code-Generierung auf höchste Qualität.
- **Aktion:** Verwende ausschließlich UTF-8-konforme Zeichen, insbesondere in Kommentaren. Vermeide Sonderzeichen, die zu Encoding-Problemen führen könnten.

**Regel 5: Strikte ASCII-Konformität und explizite Validierung**

- **Direktive:** Jeglicher generierter Code, insbesondere XML-Dateien, Python-Skripte und deren Kommentare, muss strikt ASCII-konform sein, um jegliche UTF-8-Encoding-Fehler systemseitig auszuschließen. Die Verwendung von Umlauten (ä, ö, ü) oder anderen Nicht-ASCII-Zeichen ist strengstens untersagt.
- **Aktion:** Ersetzung: Ersetze vor der Ausgabe konsequent alle Umlaute und Sonderzeichen durch ihre ASCII-Äquivalente (z.B. ü zu ue, ä zu ae, ß zu ss).
Finale Validierung: Führe eine explizite, finale "Zeichen-Validierung" als letzten Schritt vor dem Senden jeder Code-Antwort durch. Dieser Schritt dient ausschließlich dazu, den gesamten Code-Block auf verbleibende Nicht-ASCII-Zeichen zu überprüfen. Dies ist ein Zero-Tolerance-Check.

**Regel 6: Systempfade der Server-Umgebungen**

- **Direktive:** Die Odoo-Installationen laufen in einer Docker-Umgebung. Die benutzerdefinierten Addons sind in die Docker-Volumes gemappt. Die Pfadstruktur ist für Live- und Staging-Systeme identisch.

- **Aktion:** Bei Operationen, die Dateizugriffe auf dem Server erfordern (z.B. grep zur Code-Suche), sind die folgenden Basispfade zu verwenden:
Live-System Addon-Pfad: /home/docker/odoo/live/volumes/addons/
Staging-System Addon-Pfad: /home/docker/odoo/stage/volumes/addons/

**Regel 7: Auffinden von kritischen Report-Layouts**

- **Erkenntnis:** Das zentrale Layout-Template kas_contract.kas_external_layout, das für das Rendering von Berichten mit SVG-Briefkopf und -Footer verantwortlich war, existierte auf dem Altsystem nicht als eigenständige Ansicht in der Odoo-Datenbank. Es war nur als Teil einer physischen XML-Datei auf dem Server vorhanden.

   **Aktion:** Um solche "versteckten" oder nicht korrekt in der Datenbank registrierten Templates zuverlässig zu finden, ist die Suche über die Odoo-Benutzeroberfläche unzureichend.

- **Anweisung für die Zukunft:** Wenn ein Report-Template (insbesondere ein external_layout) nicht über die Odoo-UI gefunden werden kann, ist der folgende grep-Befehl auf dem Server auszuführen, um den physischen Speicherort des Codes zu ermitteln:

bash
grep -r "TEMPLATE_ID" /pfad/zu/den/addons/
(Ersetze TEMPLATE_ID durch die gesuchte ID und /pfad/zu/den/addons/ durch den relevanten Systempfad gemäß Regel 6).

Konkreter Fall: Die Definition für kas_contract.kas_external_layout wurde auf dem Altsystem in der Datei /home/docker/odoo/live/volumes/addons/kas_extension/kas_contract/report/kas_report_template.xml gefunden.

## 2. Analyse der Codebasis

### Robuste Vorgehensweisen zur Analyse

Um den Code-Inhalt zu analysieren, ohne Fehler zu provozieren, solltest du die folgenden, stabilen Methoden verwenden:

#### A) Verzeichnisstruktur verstehen
Um eine Übersicht über die Dateien in einem Modul zu erhalten, liste die Dateien gezielt auf.
- **Beispiel-Befehl:** `list all files recursively in the directory odoo/live/volumes/addons/kas_extension/kas_extension/ in the repo KA-O-S/kas_odoo`

#### B) Exakten Dateinhalt abrufen (Wichtig für Fehleranalyse!)
Um den **exakten und aktuellsten Inhalt** einer bestimmten Datei zu lesen (z.B. für Code-Vergleiche, Debugging oder das Verstehen der Implementierung), ist dies die robusteste Methode:
- **Anweisung:** Verwende den `githubread` Befehl mit dem vollständigen, exakten Dateipfad.
- **Beispiel-Befehl:** `Show me the content of the file odoo/live/volumes/addons/kas_extension/kas_extension/models/account_move.py in the repository KA-O-S/kas_odoo`
- **Vorteil:** Dies stellt sicher, dass du immer mit dem Code arbeitest, der tatsächlich im Repository vorhanden ist, und vermeidet Fehler durch veraltete Zwischenspeicher.

### Verzeichnisstruktur der Addons
- **Docker-Mountpunkt:** `odoo/live/volumes/addons/` wird nach `/home/odoo/addons` gemappt.
- **Odoo Addons-Pfad:** `odoo.conf` fügt `/home/odoo/addons/kas_extension` zum `addons_path` hinzu.
- **Speicherort der Module:** Daraus folgt der Pfad zu den eigentlichen Modul-Verzeichnissen:
    - `odoo/live/volumes/addons/kas_extension/kas_extension/`
    - `odoo/live/volumes/addons/kas_extension/kas_contract/`
    - `odoo/live/volumes/addons/kas_extension/odoo_chrome_pdf/`

## 3. Systemumgebung & Infrastruktur

- **Testserver:** `116.203.99.206`
    - **Live-Umgebung:** Port `80` -> `443` (Nginx)
    - **Stage-Umgebung:** Port `9069`
- **Produktivserver:** `kas-odoo.de`
- **Lokale Entwicklung:** Eine Kopie existiert auf dem Rechner des Benutzers.
- **Arbeitszweig:** Hauptsächlich `odoo/live`.

## 4. Architektur-Zusammenfassung

- **Basis:** `Odoo 17 Community` auf `Docker`.
- **Services:**
    - `nginx`: Reverse-Proxy, SSL.
    - `odoo-live`: Produktive Odoo-Instanz.
    - `odoo-stage`: Test-Odoo-Instanz.
    - `db`: PostgreSQL-Datenbank.
    - `certbot`: SSL-Zertifikate.

## 5. Zusammenfassung der Addons

#### `kas_contract` (Vertragslogik & Berichte)
- Erweitert `sale.order` (Angebote) um Vertragsdaten.
- Führt `contract_components` als wiederverwendbare Textblöcke ein.
- Erweitert `res.company` um Logos/Fußzeilen für Vertragsdokumente.
- Definiert PDF-Berichte: "Teileistungsvertrag", "Rahmenvertrag", "Erfolgsabhängige Leistung".

#### `kas_extension` (Allgemeine Erweiterungen)
- Erweitert `account.move` (Rechnungen) um `Leistungszeitraum` und `Ursprungsauftrag`.
- Implementiert Logik für benutzerdefinierte Rechnungsnummern (`invoice_number`).

#### `odoo_chrome_pdf` (PDF-Generierung)
- Ersetzt Odoos Standard-PDF-Engine (wkhtmltopdf) durch eine Chrome-Headless-basierte Lösung für höhere PDF-Qualität.

---

## 6. Konfigurationsdateien im Detail

### `docker-compose.yml`

```yaml
version: "3.8"
services: 

  # Nginx Proxy Service
  nginx:
    container_name: nginx
    image: nginx:stable
    depends_on:
      - odoo-live
      - odoo-stage
    ports:
      - 80:80/tcp
      - 443:443/tcp
      - 9069:9069/tcp
    volumes:
      - ./nginx/config/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/config:/etc/nginx/conf.d:ro
      - ./nginx/volumes/cache:/var/lib/nginx/cache
      - ./nginx/volumes/letsencrypt:/etc/letsencrypt
      - ./nginx/volumes/www:/var/www/certbot
    logging:
      driver: syslog
    restart: always


  # Odoo Live Service
  odoo-live: 
    container_name: odoo-live
    image: kas-odoo-live:17.0
    build:  ./odoo/live/
    ulimits:
      as:
        soft: -1
        hard: -1
    shm_size: '2gb'
    depends_on:
      - db
    volumes:
      - ./odoo/live/config:/etc/odoo:ro
      - ./odoo/live/volumes/addons:/home/odoo/addons
      - ./odoo/live/volumes/data:/var/lib/odoo
    environment:
      - CHROME_PDF_ENABLED=True
      - REPORT_URL=https://127.0.0.1:443
    logging:
      driver: syslog
    restart: always


  # Odoo Stage Service
  odoo-stage: 
    container_name: odoo-stage
    image: kas-odoo-stage:17.0
    build:  ./odoo/stage/
    depends_on:
      - db
    volumes:
      - ./odoo/stage/config:/etc/odoo:ro
      - ./odoo/stage/volumes/addons:/home/odoo/addons
      - ./odoo/stage/volumes/data:/var/lib/odoo
    environment:
      - CHROME_PDF_ENABLED=True
      - REPORT_URL=https://127.0.0.1:9069
    logging: 
      driver: syslog
    restart: always

  # Database Service
  db: 
    container_name: db
    image:  postgres:15.0
    build: ./postgres
    volumes:
      - ./postgres/volumes/backups:/home/backups
      - ./postgres/volumes/data:/var/lib/postgresql/data
    logging: 
      driver: syslog
    restart: always


  # Certbot / LetsEncrypt
  certbot:
    container_name: certbot
    image: certbot/certbot
    build: ./certbot
    volumes:
      - ./nginx/volumes/letsencrypt:/etc/letsencrypt
      - ./nginx/volumes/www:/var/www/certbot
    logging:
      driver: syslog
  # Minimaler Test-Dienst, um die ulimit-Anwendung zu ueberpruefen
  ulimit-tester:
    container_name: ulimit-tester
    image: debian:bullseye-slim
    ulimits:
      as:
        soft: -1
        hard: -1
    command: >
      bash -c "echo '>>> Ulimit-Tester gestartet. Aktive Limits sind:'; ulimit -a; echo '>>> Test laeuft, warte...'; sleep infinity"
```

### `nginx/config/default.conf`

```nginx
# Odoo Live (Default auf Port 443)
server {
    listen 443 ssl http2 default_server;
    listen [::]:443 ssl http2 default_server;
    server_name _;

    ssl_certificate /etc/letsencrypt/live/kas-odoo.de/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/kas-odoo.de/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    proxy_read_timeout 1800;
    proxy_connect_timeout 1800;
    proxy_send_timeout 1800;
    send_timeout 1800;

    proxy_set_header X-Forwarded-Host $http_host;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $http_host;

    location / {
        proxy_redirect off;
        proxy_pass http://odoo_live_web;
    }

    location /longpolling {
        proxy_pass http://odoo_live_chat;
    }
}

# Stage (Port 9069)
server {
    listen 9069 ssl http2;
    listen [::]:9069 ssl http2;

    server_name kas-odoo.de *.kas-odoo.de;

    auth_basic "Restricted";
    auth_basic_user_file /etc/nginx/conf.d/.htpasswd;

    ssl_certificate /etc/letsencrypt/live/kas-odoo.de/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/kas-odoo.de/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    proxy_set_header X-Forwarded-Host $host:$server_port;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $host:$server_port;
    
    location / {
        proxy_redirect off;
        proxy_pass http://odoo_stage_web;
    }

    location /longpolling {
        proxy_pass http://odoo_stage_chat;
    }
}
```

### `odoo/live/config/odoo.conf`

```ini
[options]
addons_path = /home/odoo/addons/extra, /home/odoo/addons/cakru, /home/odoo/addons/oca, /home/odoo/addons/kas_extension
data_dir = /var/lib/odoo
proxy_mode = True
admin_passwd = Ur39H&@32Tw&HNGR2UoNgTmaf 
list_db = True
without_demo = all
db_host = db
db_user = odoo_live
db_password = F7&8n52f^EF87&*3T$bxeMLoW
db_name = kas_odoo_live
db_template = template0
limit_request = 8196
limit_time_cpu = 600
limit_time_real = 1200
limit_memory_soft = 629145600
limit_memory_hard = 1677721600
max_cron_threads = 1
workers = 4
xmlrpc_port = 8069
gevent_port = 8072
```

### `odoo/stage/config/odoo.conf`

```ini
[options]
addons_path = /home/odoo/addons/extra, /home/odoo/addons/cakru, /home/odoo/addons/oca, /home/odoo/addons/kas_extension
data_dir = /var/lib/odoo
proxy_mode = True
admin_passwd = Ur39H&@32Tw&HNGR2UoNgTmaf 
list_db = True
without_demo = all
db_host = db
db_user = odoo_stage
db_password = F7&8n52f^EF87&*3T$bxeMLoW
db_name = STAGE_20240405121108
db_template = template0
limit_request = 8196
limit_time_cpu = 600
limit_time_real = 1200
limit_memory_soft = 629145600
limit_memory_hard = 1677721600
max_cron_threads = 1
workers = 4
xmlrpc_port = 9069
longpolling_port = 9072
```

### `odoo/live/Dockerfile` & `odoo/stage/Dockerfile`

```dockerfile
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
```
