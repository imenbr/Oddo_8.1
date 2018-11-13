# -*- coding: utf-8 -*-
{
    'name': "Test wizard",
    'summary': """Manage trainings""",

    'description': """
        Open Academy module for managing trainings:
            - training courses
            - training sessions
            - attendees registration
    """,

    'author': "Your Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly ==> liste des dependances conditionnant l'ordre de démarrage. toujours on commence par base.
    'depends': ['base','aaa_openacademy'],

    # always loaded ==> se sont les fichiers de données à charger lors de l'installation du module.
    'data': [
	
      'wizard/wizard_reception.xml'  
    ],
    # only loaded in demonstration mode ==> données de demo (pour les tests unitaires)
    'demo': [
        
    ],
}


