# -*- coding: utf-8 -*-
from osv import osv,fields
from tools.translate import _
import time
from datetime import datetime

class wizard_stock_product_purchase(osv.osv_memory):
    _name = "wizard.stock.product.purchase"
    _description = " "

    _columns = { 
        'from_date':fields.date('From'),
        'to_date':fields.date('To'),
        'stock_ids':fields.many2many('stock.location',
                                    'stock_location_rel',
                                    'stock_location_id',
                                    'stock_location_id','Stock'),
        'product_ids':fields.many2many('product.product',
                                    'product_rel',
                                    'product_id',
                                    'product_id','Produit'),
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
            'report_name'   : 'jasper_report_stock_product_purchase',
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
wizard_stock_product_purchase()
