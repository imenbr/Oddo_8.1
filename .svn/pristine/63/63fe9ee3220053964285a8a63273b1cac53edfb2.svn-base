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
            order_ids = data['form']['order_ids'] 

            #info societe     
            #cr.execute("SELECT parametre1,parametre2 FROM res_company WHERE id = 1")
            #obj_company = cr.dictfetchone()
            header1 = 'header1'#obj_company['parametre1']
            header2 = 'header2'#obj_company['parametre2']
            obj_user = self.pool.get('res.users').browse(cr, uid, uid)

        for order_id in order_ids :
            cr.execute('SELECT name, partner_id FROM purchase_order WHERE id=%s', (order_id,))
            res = cr.dictfetchone()
            order_name = res['name']
            partner = res['partner_id']
            cr.execute('SELECT * FROM res_partner WHERE id=%s', (partner,))
            partner_name = cr.dictfetchone()['name']
            cr.execute('SELECT * FROM purchase_order_line WHERE order_id=%s', (order_id,))
            order_lines = cr.dictfetchall()
            for order_line in order_lines:
                quantity_order = order_line['product_qty']
                rest = order_line['rest_product_qty']
                ref = order_line['default_code']
                
                # get uom
                cr.execute('''SELECT product_uom.name as name FROM product_uom , product_template, product_product WHERE 
                            product_template.uom_id = product_uom.id AND  product_product.product_tmpl_id = product_template.id AND product_product.id=%s''', (order_line['product_id'],))
                uom = cr.dictfetchone()['name']
                #end get uom
                
                cr.execute('SELECT name_template FROM product_product WHERE id = %s', (order_line['product_id'],)) 
                product_name = cr.dictfetchone()['name_template']
                #Rim modif 24/03/2014 qte liv & %
                
                cr.execute('''SELECT COALESCE(sum(stock_move.product_qty),0) as qte_livree
                              FROM purchase_order, stock_picking, stock_move 
                              WHERE stock_picking.purchase_id = purchase_order.id 
                              AND stock_move.picking_id = stock_picking.id 
                              AND stock_move.State='done' and purchase_order.id = %s
                              AND stock_move.product_id= %s''', (order_id,order_line['product_id'],))
                qte_livree = cr.dictfetchone()['qte_livree']
                              
                if(rest == None):
                    rest = 0 
                
                #date = move['date']
                #date.split("-")[2]+"/"+date.split("-")[1]+"/"+date.split("-")[0]
                data={
                        'header1':header1,
                        'header2':header2,
                        'order_name': order_name,
                        'partner':partner_name,
                        'product_name': product_name, 
                        'ref':ref,
                        'uom':uom,
                        'quantity_order': quantity_order, 
                        'quantity_picking': qte_livree,
                        'qty_remaining':quantity_order - qte_livree,
                        #'date': date,
                        'pourcentage':(qte_livree/quantity_order)*100,
                        'user':obj_user.name,
                } 
                result.append(data)
        return result

jasper_report.report_jasper('report.jasper_product_order_statement_print', 'stock.move', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
