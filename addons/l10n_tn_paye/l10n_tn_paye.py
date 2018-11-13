from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp

class hr_contract(osv.osv):
    _inherit = 'hr.contract'

    _columns = {
        'nationalite': fields.char('Nationalite', size=64),
        'qualif': fields.char('Qualification', size=64),
        'niveau': fields.char('Niveau', size=64),
        'coef': fields.char('Coefficient', size=64),
    }
hr_contract()



class res_company(osv.osv):
    _inherit = 'res.company'

    _columns = {
        'plafond_secu': fields.float('Plafond de la Securite Sociale', digits_compute=dp.get_precision('Payroll')),
        'nombre_employes': fields.integer('Nombre d\'employes'),
        'cotisation_prevoyance': fields.float('Cotisation Patronale Prevoyance', digits_compute=dp.get_precision('Payroll')),
        'org_ss': fields.char('Organisme de securite sociale', size=64),
        'conv_coll': fields.char('Convention collective', size=64),
    }

res_company()



class hr_payslip(osv.osv):
    _inherit = 'hr.payslip'

    _columns = {
        'payment_mode': fields.char('Mode de paiement', size=64),
    }
hr_payslip()

class hr_employee(osv.osv):
    _inherit = 'hr.employee'
	
	
    _columns = {
		'matricule_cnss':fields.integer('Matricule CNSS', size=10),
		'num_chezemployeur':fields.integer('Numero chez l\'employeur'),
	}
hr_employee()

		
		
		
		
		
		
		
		
		
		
	