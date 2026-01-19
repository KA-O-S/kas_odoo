# -*- coding: utf-8 -*-
{
    'name': "kas_contract",

    'summary': "Customisation for mapping contracts through a sales order. ",

    'description': """
    - timesheet - filter for partner
    """,

    'author': "Carsten Krumpholz IT-Consulting LTD",
    'website': "https://www.cakru-it.de",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'web'],

    # always loaded
    'data': [

        'security/ir.model.access.csv',
        'views/kas_sale_order_views.xml',
        'views/contract_components_views.xml',
        'views/contract_menu.xml',
        'views/kas_company_view.xml',
        'report/ir_actions_report.xml',
        'report/ir_actions_report_templates.xml',
        'report/kas_report_template.xml',
        'wizard/sale_advance_payment_inv_view.xml'
    ],
    'assets': {
        'web.report_assets_common': [
        'kas_contract/static/src/scss/kas_contract.scss',
        ],
        #'web.assets_backend': [
        #    'kas_contract/static/src/js/section_and_note_extension.js',
        #],
    },
}

