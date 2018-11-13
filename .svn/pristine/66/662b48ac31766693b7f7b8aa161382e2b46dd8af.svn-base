# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime

class price_compare(osv.osv_memory):
    _name = "price.compare"
    _description = " "

    _columns = {
        
        'supplier_ids':fields.many2many('res.partner',
                                    'supplier_prod_rel',
                                    'supp_id',
                                    'user_id','Supplier'),
	'product_ids':fields.many2many('product.product',
                                    'product_price_rel',
                                    'product_price_id',
                                    'product_id','Product'),
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
            'report_name'   : 'jasper_report_price_print',
            'datas': {
                    'model':'product.supplierinfo',
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
price_compare()
