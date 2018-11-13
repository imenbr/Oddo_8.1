# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime

class wizard_caisse_locaux(osv.osv_memory):
    _name = "wizard.caisse.locaux"
    _description = "Caisse Locaux Wizard "

    _columns = { 
	'caisse_id':fields.many2one('account.bank.statement', 'Caisse',required=True),
        'date_debut': fields.date('Date Debut', required=True, select=True), 
        'date_fin': fields.date('Date Fin', required=True, select=True), 

    }

    def create_report(self, cr, uid, ids, context={}):
        data = self.read(cr,uid,ids,)[-1]
        print data,' create_report('
	res={}
	res={
            'type'         : 'ir.actions.report.xml',
            'report_name'   : 'jasper_caisse_locaux_print',
            'datas': {
                    'model':'account.bank.statement',
                    'id': context.get('active_ids') and context.get('active_ids')[0] or False,
                    'ids': context.get('active_ids') and context.get('active_ids') or [],
                    
                    'form':data
                    },
            'nodestroy': False
        }
        return res

  
wizard_caisse_locaux()
