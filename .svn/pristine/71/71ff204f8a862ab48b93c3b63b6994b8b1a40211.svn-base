# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime

class wizard_cheque_circulation(osv.osv_memory):
    _name = "wizard.cheque.circulation"
    _description = "Cheques Circulation Wizard "

    _columns = { 
	
        'date_from': fields.date('Date ', required=True, select=True), 

    }
    
    def create_report(self, cr, uid, ids, context={}):
        data = self.read(cr,uid,ids,)[-1]
        print data,' create_report('
	res={}
	res={
            'type'         : 'ir.actions.report.xml',
            'report_name'   : 'jasper_cheques_circulation_print',
            'datas': {
                    'model':'reglement.piece',
                    'id': context.get('active_ids') and context.get('active_ids')[0] or False,
                    'ids': context.get('active_ids') and context.get('active_ids') or [],
                    
                    'form':data
                    },
            'nodestroy': False
        }
        return res

  
wizard_cheque_circulation()
