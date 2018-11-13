# -*- coding: utf-8 -*-
from osv import osv,fields
from tools.translate import _

class wizard_facture_fournisseur_nonregler(osv.osv_memory):
    _name = "wizard.facture.fournisseur.nonregler"
    _description = " "

    _columns = { 
        'fournisseur_id':fields.many2one('res.partner', 'Fournisseur',required=True),   
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
            'report_name'   : 'jasper_facture_fournisseur_nonregler_print',
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
wizard_facture_fournisseur_nonregler()
