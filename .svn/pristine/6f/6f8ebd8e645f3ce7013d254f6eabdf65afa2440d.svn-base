# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime

class wizard_facture_clients_nonreglees(osv.osv_memory):
    _name = "wizard.facture.clients.nonreglees"
    _description = " "

    _columns = { 
        'fournisseur_id':fields.many2one('res.partner', 'Client',required=True),   
        'report_type':fields.selection([("pdf","PDF"),
                                        ("xls","Excel"),
                                        ("html","HTML")
                                        ],'Type'),
        
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
            'report_name'   : 'jasper_facture_clients_nonreglees_print',
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
wizard_facture_clients_nonreglees()
