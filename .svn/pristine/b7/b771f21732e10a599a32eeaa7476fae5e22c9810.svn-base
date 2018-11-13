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
import time
import os

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
        result=[]
        
        if 'form' in data:
            quant_obj = self.pool.get("stock.quant")
            #info societe     
            #cr.execute("SELECT parametre1,parametre2 FROM res_company WHERE id = 1")
            #obj_company = cr.dictfetchone()
            header1 = 'header1'#obj_company['parametre1']
            header2 = 'header2'#obj_company['parametre2']
            obj_user = self.pool.get('res.users').browse(cr, uid, uid)
            stock_ids = data['form']['stock_ids']
            date = time.strftime('%d-%m-%Y %H:%M')
            
            for stock_id in stock_ids:
                cr.execute('SELECT name FROM stock_location WHERE id =%s', (stock_id,))
                location = cr.dictfetchone()['name']
                cr.execute('SELECT * FROM product_product order by default_code') 
                products = cr.dictfetchall()
                for product in products:
                    dom = [('company_id', '=', 1), ('location_id', 'child_of', stock_id), ('product_id','=', product['id'])]
                    quants = quant_obj.search(cr, uid, dom, context=context)
                    tot_qty = 0
                    for quant in quant_obj.browse(cr, uid, quants, context=context):
                        tot_qty += quant.qty
                    if (tot_qty > 0 ):
                        # get uom
                        cr.execute('''SELECT product_uom.name as name FROM product_uom , product_template, product_product WHERE 
                            product_template.uom_id = product_uom.id AND  product_product.product_tmpl_id = product_template.id AND product_product.id=%s''', (product['id'],))
                        uom = cr.dictfetchone()['name']
                        
                        #end get uom
                        #get purchase_price
                        prod_ids = self.pool.get('product.template').search(cr, uid, [('product_variant_ids','=',product['id'])])
                        prod_objs=self.pool.get('product.template').browse(cr,uid,prod_ids,context=context)
                        #end get purchase_price
                        data={
                            'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                            'header1':header1,
                            'header2':header2,
                            'date':date,
                            'product_name':product['name_template'],
                            'ref':product['default_code'],
                            'uom':uom,
                            'quantity':tot_qty,
                            'location':location,
                            'user':obj_user.name,
                            'price_unit':prod_objs.list_price,
                            'purchase_price':prod_objs.purchase_price,
                        } 
                        result.append(data)
        return result

jasper_report.report_jasper('report.jasper_report_stock_location_print', 'stock.picking', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
