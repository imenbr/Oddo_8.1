# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime

class Decompte_salaire_wizard(osv.osv_memory):
    _name = "decompte.salaire.wizard"
    _description = "Decompte salaire wizard"

    _columns = { 
	#'caisse_id':fields.many2one('account.bank.statement', 'Caisse',required=True),
        'date_debut': fields.date('Date Debut', required=True, select=True), 
        'date_fin': fields.date('Date Fin', required=True, select=True), 

    }
    _defaults = {
	#'date_aujourd': fields.datetime.now,
    }

    def create_report(self, cr, uid, ids, context={}):
        data = self.read(cr,uid,ids,)[-1]
        print data,' create_report('
	res={}
	res={
            'type'         : 'ir.actions.report.xml',
            'report_name'   : 'jasper_decompte_salaire_print',
            'datas': {
                    'model':'hr.payslip',
                    'id': context.get('active_ids') and context.get('active_ids')[0] or False,
                    'ids': context.get('active_ids') and context.get('active_ids') or [],
                    
                    'form':data
                    },
            'nodestroy': False
        }
        return res

  
Decompte_salaire_wizard()
