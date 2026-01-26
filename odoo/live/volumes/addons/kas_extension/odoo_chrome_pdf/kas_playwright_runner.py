#!/usr/bin/env python3
# /home/docker/odoo/live/volumes/addons/odoo_chrome_pdf/kas_playwright_runner.py
import sys
import asyncio
import logging
import resource
import json # <--- WICHTIG: json hinzugefügt
from playwright.async_api import async_playwright


logging.basicConfig(level=logging.INFO, format='%(asctime)s - KAS_RUNNER - %(levelname)s - %(message)s')

def set_and_check_limits():
    # ... (diese Funktion bleibt unverändert)
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        logging.info(f"LIMIT VOR AENDERUNG: RLIMIT_AS soft={soft}, hard={hard}")
        resource.setrlimit(resource.RLIMIT_AS, (hard, hard))
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        logging.info(f"LIMIT NACH AENDERUNG: RLIMIT_AS soft={soft}, hard={hard}")
        if soft != -1: logging.error("KRITISCHER FEHLER: Konnte das Limit nicht auf unendlich setzen!")
    except Exception as e:
        logging.error(f"Fehler beim Setzen des Limits: {e}")

async def main():
    # ===== START MINIMALINVASIVE AENDERUNG =====
    # JSON lesen statt reinem HTML
    try:
        payload_string = sys.stdin.read()
        payload = json.loads(payload_string)
        body_html = payload.get('body', '')
        header_html = payload.get('header', '') # Header extrahieren
        footer_html = payload.get('footer', '')
        paper_format_from_payload = payload.get('paper_format', 'A4')
        is_landscape_from_payload = payload.get('is_landscape', False)
        
    except (json.JSONDecodeError, KeyError) as e:
        logging.error(f"Fehler beim Parsen der JSON-Payload: {e}")
        sys.exit(1)
    # ===== ENDE MINIMALINVASIVE AENDERUNG =====

    set_and_check_limits()
    
    logging.info(f"Runner gestartet. Starte Chromium-Browser...")
    
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(args=['--no-sandbox'])
            page = await browser.new_page()
            await page.set_content(body_html, wait_until='networkidle')

            # ===== START MINIMALINVASIVE AENDERUNG =====
            pdf_options = {
                'format': 'A4',
                'print_background': True,
                'landscape': False,
                'prefer_css_page_size': True,
                'margin': {"top": "35mm", "right": "12mm", "bottom": "45mm", "left": "12mm"}, # Top-Margin erhöht
                'header_template': header_html,
                'footer_template': footer_html,
                'format': paper_format_from_payload,
                'landscape': is_landscape_from_payload,
                'display_header_footer': bool(header_html or footer_html)

            }
            pdf_bytes = await page.pdf(**pdf_options)
            # ===== ENDE MINIMALINVASIVE AENDERUNG =====
            
            await browser.close()
            sys.stdout.buffer.write(pdf_bytes)
            logging.info(f"PDF generiert. Groesse: {len(pdf_bytes)} bytes.")
        except Exception as e:
            logging.error(f"Playwright-Fehler: {e}", exc_info=True)
            sys.exit(1)

if __name__ == '__main__':
    sys.stdin.reconfigure(encoding='utf-8')
    asyncio.run(main())