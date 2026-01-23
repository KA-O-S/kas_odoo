# -*- coding: utf-8 -*-

# === NEU: Notwendige Imports für die Hash-Funktion. Beeinflussen bestehenden Code nicht. ===
import hashlib
import re
from bs4 import BeautifulSoup
import datetime
from odoo.tools import html2plaintext
import logging

_logger = logging.getLogger(__name__)
# === ENDE NEUE IMPORTS ===

from odoo import models, fields, api


# === BESTEHEND: Deine SaleOrder-Klasse bleibt unverändert. ===
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # === BESTEHEND: Deine Felder bleiben exakt so, wie sie sind. ===
    contract_type = fields.Selection([
       ('ra', 'Rahmenvertrag'),
        ('tl', 'Teilleistungsvertrag'),
        ('evl', 'Erfolgsabhaengige Leistung'),
    ],
    string="Vertragsart",
    # ... (alle Feld-Attribute bleiben unverändert)
    )
    # ... (alle deine weiteren Felder bleiben unverändert) ...
    pre_block = fields.Html(string="Pre-Block")
    sub_block = fields.Html(string="Sub-Block")
    contract_components_ids = fields.Many2many(
        comodel_name="sale.order.contract",
        string="Text Blöcke",
        store=True
    )
    contract_components = fields.One2many(
        comodel_name="sale.order.contract",
        inverse_name="order_id",
        string="Text Blöcke",
    )
    date_initial_contract = fields.Date(string="Rahmenvertrag vom")
    date_contract_duration = fields.Date(string="Vertragsdauer")
    page_break_signature = fields.Boolean(string="Page Break Unterschrift")
    page_break_orderline = fields.Boolean(string="Page Break Order Lines")
    order_line_section = fields.One2many(
        'sale.order.line', 'order_id',
        string='Sections',
        domain=[('display_type', '=', 'line_section')]
    )


    # === HASH-METHODE, DIE DEINE PLAYWRIGHT-ARCHITEKTUR NACHBILDET ===
    def compute_contract_hash(self):
        """
        FINALE ARCHITEKTUR (V5 - PRÄZISE):
        Verwendet ausschließlich BeautifulSoup.get_text() zur Text-Extraktion.
        Dies verhindert die Erzeugung von Artefakten wie '*' und erhält
        legitime Zeichen im Text.
        """
        if self.env.context.get('in_contract_hash_computation'):
            return ""

        def get_precise_text(html_string):
            """Hilfsfunktion, die NUR BeautifulSoup zur Extraktion verwendet."""
            if not html_string:
                return ""
            soup = BeautifulSoup(html_string, 'html.parser')
            # 1. Entferne unsichtbare <script> und <style> Blöcke
            for tag in soup(["head","script", "style"]):
                tag.decompose()
            # 2. Extrahiere den reinen Text. .get_text() ist sauberer als html2plaintext.
            # ' ' als Separator sorgt für Leerzeichen zwischen Block-Elementen.
            return soup.get_text(separator=' ', strip=True)

        try:
            self_with_context = self.with_context(in_contract_hash_computation=True)
            self_with_context.ensure_one()
            
            # --- Rendering-Kontext vorbereiten ---
            report_action = self_with_context.env.ref('kas_contract.action_report_saleorder_contract_master')
            render_context = report_action._get_rendering_context(report_action, self_with_context.ids, data=None)
            docs = self_with_context.env[report_action.model].browse(self_with_context.ids)
            doc = docs[0] if docs else None
            render_context.update({'docs': docs, 'o': doc})

            # --- Header, Body und Footer separat rendern ---
            qweb_env = self_with_context.env['ir.qweb']
            header_html = qweb_env._render('kas_contract.kas_layout_header', render_context)
            if isinstance(header_html, bytes): header_html = header_html.decode('utf-8')
            
            body_html = qweb_env._render(report_action.report_name, render_context)
            if isinstance(body_html, bytes): body_html = body_html.decode('utf-8')

            footer_html = qweb_env._render('kas_contract.kas_layout_footer', render_context)
            if isinstance(footer_html, bytes): footer_html = footer_html.decode('utf-8')
            
            # --- Reinen, präzisen Text extrahieren ---
            footer_html_cleaned_for_hash = re.sub(r'<div id="document_hash_container".*?</div>', '', footer_html, flags=re.DOTALL)
            
            header_text = get_precise_text(header_html)
            body_text = get_precise_text(body_html)
            footer_text = get_precise_text(footer_html_cleaned_for_hash)

            full_plain_text = " ".join([header_text, body_text, footer_text])
            
            # --- Standardisieren und hashen ---
            # Wir entfernen jetzt nur noch Whitespace (Leerzeichen, Tabs, Zeilenumbrüche etc.)
            standardized_string = "".join(full_plain_text.lower().split())

            # --- Logging für die Verifizierung ---
            _logger.info(f"--- START HASH-QUELLE (PRÄZISE) ---\n{standardized_string}\n--- ENDE HASH-QUELLE ---")

            hasher = hashlib.sha256()
            hasher.update(standardized_string.encode('utf-8'))
            return hasher.hexdigest()

        except Exception as e:
            _logger.error(f"Fehler bei Hash-Berechnung (Arch V5) für SO '{self.name}': {e}", exc_info=True)
            return ""


    # === BESTEHEND: Deine Methoden bleiben exakt so, wie sie sind. ===
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['origin_contract'] = self.id
        return invoice_vals

    @api.model
    def default_get(self, fields_list):
        # ... (deine komplette default_get Logik bleibt unverändert) ...
        res = super(SaleOrder, self).default_get(fields_list)
        current_company = self.env.company.id
        components = self.env['contract.components'].search([('active', '=', True), ('company_id', '=', current_company)])

        contract_components = []
        for component in components:

            contract_component = self.env['sale.order.contract'].create({
                'title': component.title,
                'name': component.name,
                'text_block': component.text_block,
                'position': component.position,
                'model_id' : component.model_id.id,
                'order_inline_text' : component.order_inline_text,
                'section_signature' : component.section_signature,
            })
            contract_components.append(contract_component.id)
        res['contract_components'] = [(6, 0, contract_components)]
        return res

# === BESTEHEND: Deine weiteren Klassen bleiben exakt so, wie sie sind. ===
class SaleOrderLine(models.Model):
    # ... (komplette Klasse bleibt unverändert) ...
    _inherit = 'sale.order.line'
    print_price =fields.Boolean(string="Mit Preis", default=True)
    section_pauschal = fields.Boolean(string="Pauschal", default=False)
    section_stundensatz = fields.Boolean(string="Stundensatz", default=False)

class SaleOrderContract(models.Model):
    # ... (komplette Klasse bleibt unverändert) ...
    _name = 'sale.order.contract'
    _description = "Sale Order Contract Componentes"
    _check_company_auto = True
    name = fields.Char(string="§. Überschrift")
    title = fields.Char(string="Beschreibung")
    text_block = fields.Html(string="Text")
    order_id = fields.Many2one(
        comodel_name="sale.order",
        string="Verkaufsauftrag"
    )
    sequence = fields.Integer(string="Sequence")
    position = fields.Selection([
        ('pre', 'Pre-Block'),
        ('sub', 'Sub-Block')
    ],
        string="Text-Position", default='pre',
        help="Position des Textblocks im Vertrag."
             " 1. vor oder nach den Auftragspositionen."
             " 2. Bei Teileistungsvertrag ’Inline' bestimmt die Auswahl vor oder nach den Leistungspositionen"
    )
    page_break = fields.Boolean(string="Page Break", default=False)
    model_id = fields.Many2one(
        comodel_name='ir.model'
    )
    order_inline_text = fields.Boolean(string="Inline")
    section_signature = fields.Boolean(string="Im Unterschriftblock", default=False)
