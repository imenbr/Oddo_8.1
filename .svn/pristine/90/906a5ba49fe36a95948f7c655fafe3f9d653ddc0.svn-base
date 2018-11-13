# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime
from openerp import SUPERUSER_ID, api
class dec_cnss_wizard(osv.osv_memory):
    _name = "declaration.cnss.wizard"
    _description = "declaration cnss wizard"






    _columns = { 

        'trimestre': fields.selection([('1', 'T01'),('2','T02'),('3','T03'),('4','T04')], 'Trimestre', required=True, ),        

    }
    _defaults = {
	#'date_aujourd': fields.datetime.now,
    }





    def create_report(self, cr, uid, ids, context={}):
	month= datetime.now().month
	wizard=self.browse(cr, uid, ids)
	j=int(wizard.trimestre)
	mois=(2*j)+(j+(-2))#1er mois de chaque trimestre
	if month < mois:
		raise osv.except_osv(('Trimestre erroné'), ('Vous devez choisir un trimestre déjà dépassé ou en cours '))
        data = self.read(cr,uid,ids,)[-1]
        print data,' create_report('
	res={}
	res={
            'type'         : 'ir.actions.report.xml',
            'report_name'   : 'jasper_declaration_cnss_print',
            'datas': {
                    'model':'hr.payslip',
                    'id': context.get('active_ids') and context.get('active_ids')[0] or False,
                    'ids': context.get('active_ids') and context.get('active_ids') or [],
                    
                    'form':data
                    },
            'nodestroy': False
        }
        return res

  
dec_cnss_wizard()
