# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import JasperDataParser  
from openerp.jasper_reports import jasper_report
from openerp import pooler
import time
from datetime import datetime
import base64
import os
#import netsvc
from openerp.osv import fields, osv
from openerp.tools.translate import _

class jasper_client(JasperDataParser.JasperDataParser):
    def __init__(self, cr, uid, ids, data, context):
        super(jasper_client, self).__init__(cr, uid, ids, data, context)

    def generate_data_source(self, cr, uid, ids, data, context):
        return 'records'

    def generate_parameters(self, cr, uid, ids, data, context):
        return {}

    def generate_properties(self, cr, uid, ids, data, context):
        return {}

    def generate_records(self, cr, uid, ids, data, context):
        pool= pooler.get_pool(cr.dbname)
        result=[]
        if 'form' in data:
            from_date = data['form']['date_from']
            to_date = data['form']['date_to']
          
           
            reg_ids = pool.get('account.invoice').search(cr, uid, [('date_invoice','>=',from_date),('date_invoice','<=',to_date),('state','=','paid'),('type','=','out_invoice')])
            #
            reg_objs = pool.get('account.invoice').browse(cr, uid, reg_ids)
            if reg_objs:
                for reg in reg_objs:

                        invoice_line_ids = self.pool.get('account.invoice.line').search(cr, uid, [('invoice_id','=',reg.id)])
                        invoice_line_objs=self.pool.get('account.invoice.line').browse(cr,uid,invoice_line_ids,context=context)
                        
                        for line in invoice_line_objs:
                            
                            prod_ids = self.pool.get('product.template').search(cr, uid, [('product_variant_ids','=',line.product_id.id)])
                            prod_objs=self.pool.get('product.template').browse(cr,uid,prod_ids,context=context)
                            
                            
                            profit= line.price_unit - prod_objs.purchase_price
                            data={
                                
                                'prod':line.product_id["name_template"],
                                'profit':profit,
                                'price_unit':line.price_unit,
                                'purchase_price':prod_objs.purchase_price,
                                
                                
                            } 
                            result.append(data)
            else :
                data={
                      
                      'prod':'',
                      'profit':'',
                      'price_unit':'',
                      'purchase_price':'',
                                
                                
                } 
                result.append(data)
                        
        return result

jasper_report.report_jasper('report.jasper_profit_print', 'account.invoice', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
