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
            #info societe     
            #cr.execute("SELECT parametre1,parametre2 FROM res_company WHERE id = 1")
            #obj_company = cr.dictfetchone()
            header1 = 'header1'#obj_company['parametre1']
            header2 = 'header2'#obj_company['parametre2']
            #rim modif 27/03/2014
            obj_user = self.pool.get('res.users').browse(cr, uid, uid)

            from_date = data['form']['from_date']
            to_date = data['form']['to_date']
            location_id = data['form']['location_id']
            
            #from_date = from_date.split("-")[2]+"/"+from_date.split("-")[1]+"/"+from_date.split("-")[0]
            #to_date = to_date.split("-")[2]+"/"+to_date.split("-")[1]+"/"+to_date.split("-")[0]
            cr.execute('SELECT * FROM purchase_order WHERE location_id = %s AND state != \'cancel\' AND date_order >= %s  AND date_order <= %s', (location_id[0],from_date,to_date))
            #cr.execute('SELECT * FROM purchase_order WHERE location_id = %s ', (location_id,))
            orders = cr.dictfetchall()
            
            cr.execute('SELECT name FROM stock_location WHERE id =%s', (location_id[0],))
            location = cr.dictfetchone()['name']
            if(len(orders) == 0):
                data={
                     'header1':header1,
                     'header2':header2,
                     'date':'',
                     'amount_total':0,
                     'location':location,
                     'order_name':'',
                     'received':'0.0%',
                     'user':obj_user.name,
                } 
                result.append(data)
            else:
                for order in orders:
                    date = order['date_order'].split(" ")[0]
                    time = order['date_order'].split(" ")[1]
                    date = date.split("-")[2]+"/"+date.split("-")[1]+"/"+date.split("-")[0]+" "+time                    
                    name = order['name']
                    amount_total = order['amount_total'] 
     
                    #calculate received : inspired from _shipped_rate method of the purchase.order model 
                    cr.execute('''SELECT
                sum(pol.product_qty), sum(pol.rest_product_qty)
            FROM
                purchase_order p, purchase_order_line pol
            WHERE
                pol.order_id = p.id AND p.id = %s GROUP BY p.id''',(order['id'],))
                    res= [0.00,0.00]
                    for qty,rest_qty in cr.fetchall():
                       res[0] += qty or 0.00
                       res[1] += rest_qty or 0.00
                    
                    if not res[1]:
                        res = 100.00
                        res = round(res,2)
                    else:
                        res = 100.00 * ((res[0]- res[1])/ res[0])
                        res = round(res,2)
                    #end calculate received
                 
                    data={
                        'header1':header1,
                        'header2':header2,
                        'date':date,
                        'amount_total':amount_total,
                        'location':location,
                        'order_name':name,
                        'received':str(res) + '%',
                        'user':obj_user.name,
                    } 
                    result.append(data)
        return result

jasper_report.report_jasper('report.jasper_report_stock_order_print', 'stock.picking', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
