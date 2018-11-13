# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime

class wizard_profit(osv.osv_memory):
    _name = "wizard.profit"
    _description = "Profit Wizard "

    _columns = { 
	
        'date_from': fields.date('Date Début ', required=True, select=True),
	'date_to': fields.date('Date Fin', required=True, select=True), 

    }
    
    def create_report(self, cr, uid, ids, context={}):
        data = self.read(cr,uid,ids,)[-1]
        print data,' create_report('
	res={}
	res={
            'type'         : 'ir.actions.report.xml',
            'report_name'   : 'jasper_profit_print',
            'datas': {
                    'model':'account.invoice',
                    'id': context.get('active_ids') and context.get('active_ids')[0] or False,
                    'ids': context.get('active_ids') and context.get('active_ids') or [],
                    
                    'form':data
                    },
            'nodestroy': False
        }
        return res

  
wizard_profit()
