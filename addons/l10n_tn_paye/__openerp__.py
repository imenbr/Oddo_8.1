{
    'name': 'Tunisia-payroll',
    'category': 'Localization/Payroll',
    'author': 'SIAT:Mohamed Habib CHALLOUF',
    'website': 'http://www.siat.com.tn',
    "category" : "Localization",
    'version': '1.0',
    'depends': ['hr_payroll'],
    
	
    'description': """Tunisian Payroll Rules.
======================

   Gestion de la Paie Tunisienne:    
    - Gestion des employés.
    - Gestion des contrats.
    - Configuration et paramètrage
            * Les rubriques de paie :primes,indemnités,avantages,déductions,...
            * Les rubriques cotisable ,imposable , soumise à la prime d'ancienneté  ...
            * Les cotisations : cotisations salariales et patronales CNSS,Mutuelle...
            * Barème de la prime d'ancienneté,cotisations CNSS ...       
    - Calcul de paie selon les normes tunisien : calcul automatique de la prime d'ancienneté,heures supplémentaire,cotisations salariales et patronales,...
    - Gestion des congés  :Calcul automatique des congés non payés à partir du module hr_holidays
    - Comptabilisation de la paie :  configuration des comptes de credit et de débit
    - Reporting : les  bulletins de paie,journale de paie ,Ordres de virement ...
    """,
    'active': False,
    'update_xml':['l10n_tn_paye_view.xml'],
	 'data': [
        'l10n_tn_paye_view.xml',
        'l10n_tn_paye_data.xml',
		
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
	'images': ['images/l10n_tn_paye_categories.jpeg', 'images/l10n_tn_paye_structure.jpeg', 'images/l10n_tn_paye_bulletin.jpeg'],

}
