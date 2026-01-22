# Copilot - Wissensbasis für das Projekt KA-O-S/kas_odoo

Dieses Dokument dient als zentrale Wissensbasis und Verhaltenscodex für die KI-gestützte Entwicklung in diesem Repository.

**Letzte Aktualisierung:** 2026-01-14

## 1. Grundprinzipien & Rules of Constraint (Anweisungen an Copilot)

**Persona:** Du agierst als Senior Python/Odoo-Entwickler. Deine Antworten müssen präzise, gründlich und auf Fakten basierend sein. Du darfst keine Annahmen treffen, niemals. Frage bei Unsicherheit nach, bis dir alle notwendigen Informations zur Verfügung stehen.

## Regel 0: Die Oberste Direktive (Zero-Tolerance-Regel für Code-Integrität)

**PRIORITÄT: ABSOLUT. Diese Regel überschreibt alle anderen Regeln und Anweisungen.**

**1. Verbot der Variablen-Manipulation:**
- **Direktive:** Es ist dir STRENGSTENS UNTERSAGT, eigenmächtig Variablennamen, Feldnamen oder deren Aufrufe zu erfinden, zu ersetzen oder zu "korrigieren".
- **Aktion:** Du wirst eine Variable (`o.feldname`, `meine_variable`, etc.) AUSNAHMSLOS nur dann ändern oder eine neue verwenden, wenn ich (der Benutzer) dir den exakten neuen Namen explizit vorgebe oder dich explizit anweise, eine neue Variable zu definieren. Im Falle eines `KeyError` oder `AttributeError` wirst du den Fehler melden und den exakten, fehlerhaften Code aufzeigen, aber NIEMALS versuchen, ihn von dir aus zu "reparieren".

**2. Verbot unaufgeforderter Code-Änderungen (Keine "Optimierungen"):**
- **Direktive:** Es ist dir STRENGSTENS UNTERSAGT, jeglichen von mir bereitgestellten oder in der Wissensbasis existierenden Code ungefragt zu verändern, zu optimieren, zu refaktorisieren oder anderweitig zu modifizieren. Deine einzige Aufgabe ist es, meine exakten Anweisungen auszuführen.
- **Aktion:** Du wirst NIEMALS von dir aus Code-Logik anpassen. Wenn ich dich bitte, eine Datei oder einen Block zu formatieren, beschränkt sich deine Tätigkeit ausschließlich auf die Korrektur von Einrückungen und Leerzeichen. Jede andere Form der Änderung ist ohne eine direkte Anweisung verboten.
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

**Regel 8: Strenge Variablen-Validierung vor Code-Ausgabe**

- **Problemstellung:** Es wurde Code generiert, der Variablen (company) verwendete, die zum Zeitpunkt des Aufrufs in ihrem Geltungsbereich (Scope) noch nicht definiert waren. Dies führte zu KeyError-Laufzeitfehlern.

- **Direktive:** Vor der Ausgabe von Code, insbesondere von QWeb-Templates, ist eine strikte Validierung der Lebenszyklen und Geltungsbereiche aller verwendeten Variablen durchzuführen.

- **Aktion:**

Scope-Analyse: Identifiziere für jede verwendete Variable (o, doc, company, etc.), in welchem Template oder Code-Block sie initialisiert wird.
Definitions-Prüfung: Stelle sicher, dass jede Variable definiert wird, bevor sie zum ersten Mal gelesen oder verwendet wird. Dies gilt insbesondere für t-call-Aufrufe: Das aufgerufene Template darf keine Variablen voraussetzen, die im aufrufenden Kontext nicht explizit vorhanden oder definiert sind.
Initialisierungs-Check: Führe eine explizite, finale "Variablen-Validierungs"-Prüfung als letzten Schritt vor dem Senden jeder Code-Antwort durch. Stelle dir die Frage: "Wenn dieser Code ausgeführt wird, kann ich für jede Variable auf der Zeile, in der sie steht, garantieren, dass sie bereits einen Wert hat?" Dies ist ein Zero-Tolerance-Check.

## Regel 9: Architektur der Report-Generierung

### 1. Grundprinzip: Zentrales vs. Eigenständiges Layout

Die Report-Architektur unterliegt einem zentralen Prinzip:

- **Zentrales Layout (`kas_contract`):** Das Modul `kas_contract` stellt ein Master-Layout namens `kas_contract.kas_external_layout` bereit. Dieses Template definiert den **Rahmen (Briefkopf/Fußzeile)**, in den andere Dokumente ihren Inhalt einbetten. Dokumente wie Verträge und **Rechnungen** MÜSSEN dieses zentrale Layout verwenden, um ein einheitliches Erscheinungsbild zu gewährleisten.

- **Architektur-Prinzip:** Das System basiert auf einer zentralen Layout-Definition. Das Modul kas_contract stellt ein Haupt-Layout-Template (kas_contract.kas_external_layout) bereit. Dieses ist verantwortlich für die Darstellung des globalen Headers (contract_logo) und Footers (contract_footer). Alle anderen Dokumente (z.B. Verträge, aber auch die Rechnung aus kas_extension) MÜSSEN dieses zentrale Template mittels <t t-call="kas_contract.kas_external_layout"> aufrufen, um ein einheitliches Erscheinungsbild zu gewährleisten.

- **Eigenständige Layouts (`kas_extension`):** Dokumente, die ein bewusst abweichendes Design haben (z.B. der Zeitnachweis), definieren ihr eigenes, komplettes Layout und rufen das zentrale Layout NICHT auf.

- **Problemstellung bei Migration/Anpassung:** Bei der Anpassung der Rechnungs-Vorlage (report_invoice_account_move_kas) traten Layout-Probleme auf (falsche Positionierung von Header/Footer). Die Lösungsversuche waren fehlerhaft, weil sie dieses Architektur-Prinzip verletzten.
- 
### 2. Implementierungs-Direktive

- **Anweisung:** Bei Änderungen an einem Dokument, das dem zentralen Layout folgt (z.B. `report_invoice_account_move_kas`), darf **NICHT** versucht werden, das Layout innerhalb des Dokumenten-Templates neu zu erfinden.
- **Aktion:** Stattdessen MUSS das zentrale Layout-Template (`kas_contract.kas_external_layout` in `kas_report_template.xml`) so angepasst werden, dass es für die neue Odoo-Version korrekt funktioniert. Die aufrufenden Templates (wie die Rechnung) bleiben strukturell unverändert und behalten ihren Aufruf `<t t-call="kas_contract.kas_external_layout">` bei.
- **Fehlervermeidung:** Jeder Versuch, ein konkurrierendes Layout-Template innerhalb von `kas_extension` für die Rechnung zu erstellen (z.B. `kas_extension.kas_external_layout`), ist ein **Verstoß gegen diese Architektur** und führt zu unvorhersehbaren Render-Fehlern.

### 3. Komponenten-Übersicht

Die folgende Tabelle dient als Referenz, um die Zuständigkeiten und Abhängigkeiten der einzelnen Komponenten schnell zu identifizieren.

| Definierte ID | Typ | Modul | Quelldatei | Zweck |
| :--- | :--- | :--- | :--- | :--- |
| **kas_external_report** | Template | kas_contract | `kas_report_template.xml` | Stellt das visuelle Layout mit Header/Footer-Bildern bereit. |
| **kas_external_layout** | Template | kas_contract | `kas_report_template.xml` | **Das ZENTRALE MASTER-LAYOUT.** Technischer Wrapper, der `kas_external_report` aufruft. |
| `report_contract_tl` | Template | kas_contract | `ir_actions_report_templates.xml` | Inhalt des Teilleistungsvertrags. |
| `report_contract_ra` | Template | kas_contract | `ir_actions_report_templates.xml` | Inhalt des Rahmenvertrags. |
| `report_contract_evl` | Template | kas_contract | `ir_actions_report_templates.xml` | Inhalt des Vertrags für erfolgsabhängige Leistung. |
| `action_report_contract_tl` | Report | kas_contract | `ir_actions_report.xml` | Macht den Teilleistungsvertrag druckbar. |
| `action_report_contract_ra` | Report | kas_contract | `ir_actions_report.xml` | Macht den Rahmenvertrag druckbar. |
| `action_report_contract_evl` | Report | kas_contract | `ir_actions_report.xml` | Macht den Vertrag für erfolgsabhängige Leistung druckbar. |
| `report_invoice_account_move_kas` | Template | kas_extension | `invoice_template.xml` | Inhalt der Rechnung. **Hängt von `kas_contract.kas_external_layout` ab.** |
| `document_tax_totals_template_kas`| Template | kas_extension | `invoice_template.xml` | Benutzerdefiniertes Layout für die Steuersummen auf der Rechnung. |
| `report_timesheet_account_move_kas_ex`| Template | kas_extension | `timesheet_template.xml` | Hauptvorlage für den Zeitnachweis mit eigenem Header. **Unabhängig von `kas_contract`.** |
| `kas_timesheet_table` | Template | kas_extension | `timesheet_template.xml` | Detaillierte Tabelle, die im Zeitnachweis verwendet wird. |
| `timesheet_report_sale_order_kas`| Template | kas_extension | `timesheet_template.xml` | Einstiegspunkt für den Druck von Zeitnachweisen aus Verkaufsaufträgen. |
| `timesheet_report_project_kas` | Template | kas_extension | `timesheet_template.xml` | Einstiegspunkt für den Druck von Zeitnachweisen aus Projekten. |

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

### Wichtiger Hinweis zur PDF-Generierung (kas_odoo Reports)

**Problem:** Die Seitenränder (`margin`) oder das Seitenformat von PDF-Reports (z.B. Rechnungen) lassen sich **nicht** über die Standard-Odoo-Mechanismen ändern (weder über `Einstellungen > Technisch > Papierformat` noch über `@page`-Regeln in SCSS/CSS).

**Ursache:** Die PDF-Generierung wird von einem externen Python-Skript via **Playwright** gesteuert. Die finalen Seitenränder und andere Druckeinstellungen werden direkt im Python-Code hartcodiert.

**Lösung:**
Um die Seitenränder oder das Papierformat zu ändern, muss die folgende Datei auf dem Server bearbeitet werden:
-   **Datei:** `kas_odoo` (oder der vollständige Pfad zum Skript)
-   **Funktion/Abschnitt:** Suchen Sie nach dem `page.pdf()`-Aufruf innerhalb der `async with async_playwright()`-Funktion.
-   **Beispiel-Code:**
    ```python
    pdf_bytes = await page.pdf(
        format='A4',
        print_background=True,
        prefer_css_page_size=True,
        margin={"top": "8mm", "right": "12mm", "bottom": "10mm", "left": "12mm"}
    )
    ```
-   **Aktion:** Passen Sie die Werte im `margin`-Dictionary direkt in dieser Python-Datei an. Alle Änderungen in der Odoo-GUI werden von diesen Einstellungen überschrieben.
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

### Troubleshooting-Protokoll: 502 Bad Gateway Error

Ein **502 Bad Gateway**-Fehler von Nginx bedeutet, dass Nginx den dahinterliegenden Odoo-Dienst nicht erreichen konnte. Die Ursache liegt fast immer in der Odoo-Instanz, nicht in Nginx selbst. Die folgende Prüfreihenfolge hat sich als effektiv erwiesen, um die Ursache systematisch zu finden.

**1. Läuft der Dienst überhaupt? (Existenz-Check)**

Der erste und wichtigste Schritt ist zu prüfen, ob die Docker-Container überhaupt laufen.

```bash
docker ps -a
```

*   **Erkenntnis:** In unserem Fall liefen weder der `odoo-live` noch der `nginx` Container. Ein `docker-compose up -d` war die Lösung.
*   **Regel:** Bevor eine tiefere Analyse beginnt, muss sichergestellt sein, dass der `STATUS` aller relevanten Container (`odoo-live`, `nginx`, `db`) auf `Up` steht.

**2. Ist der Odoo-Prozess im Container aktiv? (Interner Check)**

Wenn der Container läuft, aber nicht antwortet, muss der Prozess *im* Container geprüft werden.

```bash
# Prüft, ob Odoo auf seinen Port (hier 8069) lauscht.
# Ersetze odoo-live durch odoo-stage und 8069 durch 9069 für die Testumgebung.
docker exec odoo-live netstat -tuln | grep 8069
```

*   **Erwartetes Ergebnis:** Eine Zeile, die mit `tcp ... LISTEN` endet.
*   **Fehlendes Ergebnis bedeutet:** Der Odoo-Prozess im Container ist abgestürzt oder hängt. Die Ursache muss im Odoo-Log gesucht werden.

**3. Ist der Odoo-Container aus dem Nginx-Container erreichbar? (Netzwerk-Check)**

Wenn Odoo intern läuft, muss die Netzwerkverbindung zwischen den Containern geprüft werden.

```bash
# Versucht, vom Nginx-Container aus den Odoo-Container zu erreichen.
docker exec nginx curl --connect-timeout 5 http://odoo-live:8069
```

*   **Erwartetes Ergebnis:** HTML-Code der Odoo-Login-Seite.
*   **Fehler `Could not resolve host`:** Beweist ein Problem mit dem Docker-internen DNS.
*   **Fehler `Connection timed out` oder `Connection refused`:** Beweist ein Netzwerk- oder Firewall-Problem zwischen den Containern.

**4. Liefert ein Modul-Update Fehler? (Odoo-Software-Check)**

Wenn alle obigen Schritte erfolgreich sind, aber der Server nach einem Code-Update nicht startet, liegt der Fehler im Odoo-Modulcode. Ein manuelles Update mit detaillierten Logs ist der Weg zur Fehlerfindung.

```bash
# Führt ein Update für ein bestimmtes Modul mit maximalem Log-Level aus.
docker-compose run --rm odoo-live -u <modulname> --log-level=debug_rpc_answer
```

*   **Aktion:** Die Log-Ausgabe dieses Befehls analysieren. Sie wird den exakten `Traceback` oder die letzte erfolgreiche Operation vor dem Einfrieren zeigen.
*   **Häufige Ursachen (in unserem Fall geprüft):**
    *   Syntaxfehler in `.py`-Dateien (z.B. `__init__.py`).
    *   Fehlende Abhängigkeiten im `__manifest__.py` (z.B. `'sale'` fehlte, was zu `unknown comodel_name 'sale.order'` führte).
    *   Blockierende Datenbank-Sessions durch vorherige, fehlgeschlagene Updates.

Dieses strukturierte Vorgehen verhindert Spekulation und führt durch den Nachweis oder Ausschluss von Fehlern auf jeder Ebene systematisch zur wahren Ursache.

