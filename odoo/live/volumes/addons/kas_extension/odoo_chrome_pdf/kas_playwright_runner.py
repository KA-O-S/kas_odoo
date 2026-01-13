#!/usr/bin/env python3
import sys
import asyncio
import logging
import resource
from playwright.async_api import async_playwright # <--- HINZUGEFUEGT

logging.basicConfig(level=logging.INFO, format='%(asctime)s - KAS_RUNNER - %(levelname)s - %(message)s')

def set_and_check_limits():
    """Setzt das RLIMIT_AS auf unendlich und ueberprueft es."""
    # Versuche, das soft limit auf das hard limit zu setzen (-1 = unendlich)
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        logging.info(f"LIMIT VOR AENDERUNG: RLIMIT_AS soft={soft}, hard={hard}")
        
        resource.setrlimit(resource.RLIMIT_AS, (hard, hard))
        
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        logging.info(f"LIMIT NACH AENDERUNG: RLIMIT_AS soft={soft}, hard={hard}")
        if soft != -1:
            logging.error("KRITISCHER FEHLER: Konnte das Limit nicht auf unendlich setzen!")
            
    except Exception as e:
        logging.error(f"Fehler beim Setzen des Limits: {e}")

async def main():
    html_string = sys.stdin.read()
    
    # Setze das Limit direkt vor dem Browser-Start
    set_and_check_limits()
    
    logging.info(f"Runner gestartet. Starte Chromium-Browser...")
    
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(args=['--no-sandbox'])
            page = await browser.new_page()
            await page.set_content(html_string, wait_until='networkidle')
            pdf_bytes = await page.pdf(format='A4', print_background=True)
            await browser.close()
            sys.stdout.buffer.write(pdf_bytes)
            logging.info(f"PDF generiert. Groesse: {len(pdf_bytes)} bytes.")
        except Exception as e:
            logging.error(f"Playwright-Fehler: {e}", exc_info=True)
            sys.exit(1)

if __name__ == '__main__':
    sys.stdin.reconfigure(encoding='utf-8')
    asyncio.run(main())