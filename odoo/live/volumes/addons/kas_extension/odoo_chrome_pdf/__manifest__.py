{
    'name': 'KAS Chrome PDF Reports',
    'version': '17.0.1.0.0',
    'category': 'Reporting',
    'summary': 'Chrome Headless PDF generation replacing wkhtmltopdf',
    'description': """
        Chrome Headless PDF Reports fuer KAS-Odoo
        
        Ersetzt wkhtmltopdf durch Chrome Headless fuer:  
        - Moderne CSS-Unterstuetzung
        - JavaScript-Rendering
        - Bessere PDF-Qualitaet
        - Schnellere Generierung
        
        Getestet mit Chrome 143.0.7499.169 + pyppeteer
    """,
    'author': 'KAS',
    'depends': ['base', 'web'],
    'data': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}