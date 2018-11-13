# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class wizard_stock_order(osv.osv_memory):
    _name = "wizard.stock.order"
    _description = " "

    _columns = { 
        'from_date':fields.date('From'),
        'to_date':fields.date('To'),
        'location_id':fields.many2one('stock.location', 'Location', ondelete='set null'),
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
            'report_name'   : 'jasper_report_stock_order_print',
            'datas': {
                    'model':'stock.picking',
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
wizard_stock_order()
