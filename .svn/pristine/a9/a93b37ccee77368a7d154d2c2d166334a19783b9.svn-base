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
from jasper_reports import jasper_report
import pooler
import time, datetime
import base64
import os
import netsvc

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
            #info societe     
            #cr.execute("SELECT parametre1,parametre2 FROM res_company WHERE id = 1")
            #obj_company = cr.dictfetchone()
            header1 = 'header1'#obj_company['parametre1']
            header2 = 'header2'#obj_company['parametre2']
            obj_user = self.pool.get('res.users').browse(cr, uid, uid)
            from_date = data['form']['from_date']
            to_date = data['form']['to_date']
            stock_ids = data['form']['stock_ids']
            product_ids = data['form']['product_ids']
            from_date = from_date.split("-")[2]+"/"+from_date.split("-")[1]+"/"+from_date.split("-")[0]
            to_date = to_date.split("-")[2]+"/"+to_date.split("-")[1]+"/"+to_date.split("-")[0]
            picking_type = 'in'
            for stock_id in stock_ids:
                cr.execute('SELECT id FROM stock_picking WHERE location_dst_id =%s AND type=%s', (stock_id,picking_type) )
                picking_ids = cr.dictfetchall() 
                cr.execute('SELECT name FROM stock_location WHERE stock_location.id =%s', (stock_id,))
                location = cr.dictfetchone()['name'] 
                if len(picking_ids) != 0:
                    pick='('
                    for picking in picking_ids:
                        pick=pick+str(picking['id'])+','
                    pick = pick[:-1]
                    pick=pick+')'
                    if product_ids:
                        prod='('
                        for produit in product_ids:
                            prod=prod+str(produit)+','
                        prod = prod[:-1]
                        prod=prod+')'
                        request ='SELECT SUM(product_qty * ( price_unit *(1-discount*0.01))) as tot, SUM(product_qty) as tot_qty, product_id, default_code FROM stock_move WHERE state = \'done\' AND date <= \''+str(to_date)+'\' AND date >= \''+str(from_date)+'\' AND picking_id in '+pick+' AND location_dest_id ='+str(stock_id)+' AND product_id in '+prod+' group by product_id, default_code'
                        cr.execute(request,(product_ids,))
                
                    else:
                        request ='SELECT SUM(product_qty * ( price_unit *(1-discount*0.01))) as tot, SUM(product_qty) as tot_qty, product_id, default_code FROM stock_move WHERE state = \'done\' AND date <= \''+str(to_date)+'\' AND date >= \''+str(from_date)+'\' AND picking_id in '+pick+' AND location_dest_id ='+str(stock_id)+' group by product_id, default_code'
                    
                #cr.execute('SELECT SUM(product_qty * price_unit) as tot, SUM(product_qty) as tot_qty, product_id, name FROM stock_move WHERE picking_id in %s AND location_dest_id = %s group by product_id, name', (picking_ids, stock_id,) )
                        cr.execute(request)
                   
                    products = cr.dictfetchall()
                    sub_total = 0.0
                    tot_qty = 0.0
                    for product in products:
                        product_id = product['product_id']
                        ref = product['default_code']
                        sub_total = product['tot']
                        tot_qty = product['tot_qty']
                        cr.execute('SELECT name_template FROM product_product WHERE id = %s', (product['product_id'],)) 
                        product_name = cr.dictfetchone()['name_template']
                        # get uom
                        cr.execute('''SELECT product_uom.name as name FROM product_uom , product_template, product_product WHERE 
                            product_template.uom_id = product_uom.id AND  product_product.product_tmpl_id = product_template.id AND product_product.id=%s''', (product['product_id'],))
                        uom = cr.dictfetchone()['name']
                        #end get uom

                        #get amount taxed
                        cr.execute('SELECT * FROM product_supplier_taxes_rel WHERE prod_id=%s', (product['product_id'],))
                        taxes = cr.dictfetchall()
                        tva = 0.0
                        for tax in taxes:
                            cr.execute('SELECT * FROM account_tax WHERE id=%s', (tax['tax_id'],))   
                            amount = cr.dictfetchone()['amount'] 
                            tva += sub_total * amount
                        #end get amount taxed 
                        data={
                                'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                                'header1':header1,
                                'header2':header2,
                                'location':location,
                                'name_product': product_name,
                                'ref':ref,
                                'uom':uom,
                                'product_qty': tot_qty,
                                'subtotal' : round(sub_total + tva,3),
                                'user':obj_user.name,
                        } 
                        result.append(data)
        return result

jasper_report.report_jasper('report.jasper_report_stock_product_purchase', 'stock.picking', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
