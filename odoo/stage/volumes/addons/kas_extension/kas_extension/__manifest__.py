# -*- coding: utf-8 -*-
{
    'name': "kas_extension",

    'summary': "Customer Extensions ",

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
    'depends': ['base', 'account', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/invoice_seq.xml',
        'views/res_company_views.xml',
        'views/hr_timesheet_views.xml',
        'views/invoice_view.xml',
        'report/ir_actions_report.xml',
        'report/timesheet_template.xml',
        'report/invoice_template.xml'
    ],

}

