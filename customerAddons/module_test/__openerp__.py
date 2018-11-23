# -*- coding: utf-8 -*-
{
    'name': "moduleTest",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Your Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'module_test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'templates.xml',
        'views/moduleTest.xml',
        'views/partner.xml',
        # 'views/details.xml',
        # 'views/button.xml',
        # 'views/price.xml',
        # 'views/courrier.xml',
        # 'views/customer.xml',
        # 'views/customer184Meth.xml',
        # 'views/customer184.xml',
        # 'views/action191.xml',
        # 'views/list197.xml',
        # 'views/view199.xml',
        # 'views/herite.xml',
        'views/session_workflow.xml',
        # 'views/workflowAutomatic.xml',

    ],
    #
    # 'js': [
    #     'static/src/js/test.js'
    # ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
