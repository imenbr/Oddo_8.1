# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class wizard_product_order_statement(osv.osv_memory):
    _name = "wizard.product.order.statement"
    _description = " "

    _columns = {
        'order_ids':fields.many2many('purchase.order',
                                    'wizard_order_ids_rel',
                                    'order_id',
                                    'wizard_id','Order'),
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
            'report_name'   : 'jasper_product_order_statement_print',
            'datas': {
                    'model':'stock.move',
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
wizard_product_order_statement()
