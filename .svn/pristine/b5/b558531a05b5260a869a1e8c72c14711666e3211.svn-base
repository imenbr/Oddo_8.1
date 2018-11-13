# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime

class wizard_turnover_stat_client(osv.osv_memory):
    _name = "wizard.turnover.stat.client"
    _description = " Sttc Turnover Stats Client"

    _columns = {
        'type': fields.selection([
            ('out_invoice','Vente'),
            ('in_invoice','Achat'),
            ],'Type'),
        
        'user_ids':fields.many2many('res.partner',
                                    'user_analysis_rel',
                                    'user_analysis_id',
                                    'user_id','Client'),
        'report_type':fields.selection([("pdf","PDF"),
                                        ("xls","Excel"),
                                        ("html","HTML")
                                        ],'Type'),
        'from_date':fields.date('From'),
        'to_date':fields.date('To'),
        'state': fields.selection([('choose','choose'),
                                    ('get','get'),
                                   ]),

    }

    def create_report(self, cr, uid, ids, context={}):
        data = self.read(cr,uid,ids,)[-1]
        print data,' create_report('
	res={}
	res={
            'type'         : 'ir.actions.report.xml',
            'report_name'   : 'jasper_report_turnover_client_print',
            'datas': {
                    'model':'account.invoice',
                    'id': context.get('active_ids') and context.get('active_ids')[0] or False,
                    'ids': context.get('active_ids') and context.get('active_ids') or [],
                    'report_type': data['report_type'],
                    'form':data
                },
            'nodestroy': False
            }
        return res
    _defaults = {
        'report_type': lambda *a: 'pdf',
        'state': lambda *a: 'choose',
        }
wizard_turnover_stat_client()
