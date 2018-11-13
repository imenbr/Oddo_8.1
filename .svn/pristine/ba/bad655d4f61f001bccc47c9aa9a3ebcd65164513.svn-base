# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime

class wizard_dec_impot_emp(osv.osv_memory):
    _name = "wizard.dec.impot.emp"
    _description = " "





    _columns = { 
         


        'annee': fields.char('Année', required=True, select=True), 
    }
    _defaults = {
	#'anne': fields.datetime.now,
	'annee' : lambda *a: str(time.strftime('%Y')),
    }

    def create_report(self, cr, uid, ids, context={}):
        data = self.read(cr,uid,ids,)[-1]
        print data,' create_report('
	res={}
	res={
            'type'         : 'ir.actions.report.xml',
            'report_name'   : 'jasper_impot_print',
            'datas': {
                    'model':'hr.payslip',
                    'id': context.get('active_ids') and context.get('active_ids')[0] or False,
                    'ids': context.get('active_ids') and context.get('active_ids') or [],

                    'form':data
                    },
            'nodestroy': False
        }
        return res


wizard_dec_impot_emp()
