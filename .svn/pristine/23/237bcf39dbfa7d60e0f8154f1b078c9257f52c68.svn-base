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
from openerp.JasperReports import *
from openerp.jasper_reports import jasper_report
import time, datetime

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
        
        price=0.0
        partner=False
        name_product=False
        supplier_product_name=False
        product_code=False

        if 'form' in data:
            supplier_ids = data['form']['supplier_ids'] 
            #info societe     
            #cr.execute("SELECT parametre1,parametre2 FROM res_company WHERE id = 1")
            #obj_company = cr.dictfetchone()
            header1 = 'my header 1'#obj_company['parametre1']
            header2 = 'my header2'#obj_company['parametre2']
            obj_user = self.pool.get('res.users').browse(cr, uid, uid)
            
            for supplier_id in supplier_ids:
                cr.execute('SELECT * FROM product_product, product_supplierinfo WHERE product_product.product_tmpl_id = product_supplierinfo.product_tmpl_id AND  product_supplierinfo.name=%s order by product_code', (supplier_id,))
                products = cr.dictfetchall()
                if len(products) > 0:
                  for product in products:
                    
                    supplier = product['name']
                    cr.execute('SELECT name FROM res_partner WHERE id=%s', (product['name'],))
                    partner = cr.dictfetchone()['name']
                    
                    discount = product['supplier_discount'] 
                    if (discount):
                        price = product['prix'] * (1 - discount * 0.01)    
                    else:
                        price = product['prix'] 
                 
                    supplier_product_name= product['product_name']
                    product_code= product['product_code']
                    cr.execute('SELECT name_template FROM product_product WHERE id=%s', (product['product_tmpl_id'],))
                    
                    name_product= cr.dictfetchone()['name_template']
                    cr.execute('SELECT product_uom.name as uom_name FROM product_uom,product_template WHERE product_template.uom_id=product_uom.id AND product_template.id=%s', (product['product_tmpl_id'],))
                    uom = cr.dictfetchone()['uom_name']
                    #get amount taxed
                    cr.execute('SELECT * FROM product_supplier_taxes_rel WHERE prod_id=%s', (product['product_tmpl_id'],))
                    
                    taxes = cr.dictfetchall()
                    tva = 0.0
                    for tax in taxes:
                        cr.execute('SELECT * FROM account_tax WHERE id=%s', (tax['tax_id'],))   
                        amount = cr.dictfetchone()['amount'] 
                        tva += price * amount
                    #end get amount taxed 
                    #price
                    price = price + tva
                    price = round(price,3)
                    data={
                        'header1':header1,
                        'header2':header2,
                        'name_product':name_product,
                        'price':price,
                        'supplier_product_name':supplier_product_name,
                        'product_code':product_code,
                        'partner':partner,
                        'uom':uom,
                        'user':obj_user.name,
                    } 
                    result.append(data)
                else:
                    data={
                        'header1':header1,
                        'header2':header2,
                        'name_product':'',
                        'price':'',
                        'supplier_product_name':'',
                        'product_code':'',
                        'partner':partner,
                        'uom':'',
                        'user':obj_user.name,
                    } 
                    result.append(data)  
        return result

jasper_report.report_jasper('report.jasper_report_supplier_product_print', 'product.supplierinfo', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
