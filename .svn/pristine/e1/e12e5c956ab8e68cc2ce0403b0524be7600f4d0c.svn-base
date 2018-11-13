# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp

class cotisation_trims(osv.osv):
    _name = 'cotisation.trims'


    def annuler_declaration(self, cr, uid, ids, context):
        '''
           Methode du workflow: changer l'état du declaration CNSS à l'état annulé
        ''' 

        self.write(cr, uid, ids, {'state': 'cancel'})
        return True

    def confirmer_declaration(self, cr, uid, ids, context):  
        '''
           Methode du workflow: permet la confirmation du declaration CNSS
        '''   

        self.write(cr, uid, ids, {'state': 'done'})
                   
        return True


    _columns = {
        
        'name': fields.char('Référence', size=64),
	'state': fields.selection([
            ('draft', 'Brouillon'),
            ('verify', 'Waiting'),
            ('done', 'Terminé'),
            ('cancel', 'Annulé'),
        ], 'Status', select=True, readonly=True, copy=False,
            help='* When the payslip is created the status is \'Draft\'.\
            \n* If the payslip is under verification, the status is \'Waiting\'. \
            \n* If the payslip is confirmed then status is set to \'Done\'.\
            \n* When user cancel payslip the status is \'Rejected\'.'),
	
	'date_from': fields.date('Date From', readonly=True, states={'draft': [('readonly', False)]}, required=True),
        'date_to': fields.date('Date To', readonly=True, states={'draft': [('readonly', False)]}, required=True),
	'cotisa_lines': fields.one2many('cotisation.trims.ligne', 'cotisa_id', 'Ligne de declaration trimestielle'),
	
    }
    _defaults = {
        'state': 'draft',

    }

cotisation_trims()

class cotisation_trims_ligne(osv.osv):
    _name = 'cotisation.trims.ligne'


    _columns = {
	'cotisa_id' : fields.many2one('cotisation.trims' , 'Declaration Trimestrielle' , ondelete='cascade'),
	'employee_id': fields.many2one('hr.employee', 'Employee', required=True),
	'mois1_id': fields.many2one('hr.payslip', 'Fiche de Paie 1er Mois'),
	'mois2_id': fields.many2one('hr.payslip', 'Fiche de Paie 2éme Mois'),
	'mois3_id': fields.many2one('hr.payslip', 'Fiche de Paie 3éme Mois'),
        'sal3': fields.float('Salaire 3éme mois', digits_compute=dp.get_precision('Payroll'),readonly=True),
        'sal2': fields.float('Salaire 2éme mois', digits_compute=dp.get_precision('Payroll'),readonly=True),
        'sal1': fields.float('Salaire 1er mois', digits_compute=dp.get_precision('Payroll'),readonly=True),





    }
    _defaults = {
        'sal1': lambda *a: 0.00,
        #'product_uom': _get_uom_id,
        'sal2': lambda *a: 0.00,
        'sal3': lambda *a:  0.00,
    }


    def mois1_id_change(self, cr, uid, ids,fiche_paie, context=None):

	res_final = {}
        if fiche_paie:
            #les informations sur le fiche de paie

            hr_payslip_obj = self.pool.get('hr.payslip').browse(cr,uid,fiche_paie,context=context)
            hr_payslip_line_ids = self.pool.get('hr.payslip.line').search(cr, uid, [('slip_id', '=', fiche_paie)])

            hr_payslip_line_obj = self.pool.get('hr.payslip.line').browse(cr,uid,hr_payslip_line_ids)


            for hr_payslip_line in hr_payslip_line_obj :
		if hr_payslip_line.code=='NET' :
            		salaire=hr_payslip_line.total

            res_final = {'value':{'sal1':salaire}}
        return res_final

    def mois2_id_change(self, cr, uid, ids, fiche_paie, context=None):

	res_final = {}
        if fiche_paie:
            #les informations sur le fiche de paie

            hr_payslip_obj = self.pool.get('hr.payslip').browse(cr,uid,fiche_paie,context=context)
            hr_payslip_line_ids = self.pool.get('hr.payslip.line').search(cr, uid, [('slip_id', '=', fiche_paie)])

            hr_payslip_line_obj = self.pool.get('hr.payslip.line').browse(cr,uid,hr_payslip_line_ids)


            for hr_payslip_line in hr_payslip_line_obj :
		if hr_payslip_line.code=='NET' :
            		salaire=hr_payslip_line.total

            res_final = {'value':{'sal2':salaire}}
        return res_final

    def mois3_id_change(self, cr, uid, ids,  fiche_paie, context=None):

	res_final = {}
        if fiche_paie:
            #les informations sur le fiche de paie

            hr_payslip_obj = self.pool.get('hr.payslip').browse(cr,uid,fiche_paie,context=context)
            hr_payslip_line_ids = self.pool.get('hr.payslip.line').search(cr, uid, [('slip_id', '=', fiche_paie)])

            hr_payslip_line_obj = self.pool.get('hr.payslip.line').browse(cr,uid,hr_payslip_line_ids)


            for hr_payslip_line in hr_payslip_line_obj :
		if hr_payslip_line.code=='NET' :
            		salaire=hr_payslip_line.total

            res_final = {'value':{'sal3':salaire}}
        return res_final


cotisation_trims_ligne()
