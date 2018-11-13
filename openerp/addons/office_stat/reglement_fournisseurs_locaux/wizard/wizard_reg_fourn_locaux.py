# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime

class wizard_reg_fourns_locaux(osv.osv_memory):
    _name = "wizard.reg.fourns.locaux"
    _description = "Reglement fournisseurs locaux Wizard "

    _columns = { 
	
        'date_from': fields.date('Date Début', required=True, select=True),
	'date_to': fields.date('Date Fin', required=True, select=True), 

    }
    
    def create_report(self, cr, uid, ids, context={}):
        data = self.read(cr,uid,ids,)[-1]
        print data,' create_report('
	res={}
	res={
            'type'         : 'ir.actions.report.xml',
            'report_name'   : 'jasper_reg_fourns_locaux_print',
            'datas': {
                    'model':'account.invoice',
                    'id': context.get('active_ids') and context.get('active_ids')[0] or False,
                    'ids': context.get('active_ids') and context.get('active_ids') or [],
                    
                    'form':data
                    },
            'nodestroy': False
        }
        return res

  
wizard_reg_fourns_locaux()
