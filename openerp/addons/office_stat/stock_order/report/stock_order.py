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
        res = {}
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
                     'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                     'header1':header1,
                     'header2':header2,
                     'date':'',
                     'amount_total':0,
                     'location':location,
                     'order_name':'',
                     'received':'0%',
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
                    order_id = order['id']
                    #calculate received : inspired from _shipped_rate method of the purchase.order model 
                    cr.execute('''SELECT
                p.order_id, sum(m.product_qty), m.state
            FROM
                stock_move m
            LEFT JOIN
                purchase_order_line p on (p.id=m.purchase_line_id)
            WHERE
                p.order_id = %s GROUP BY m.state, p.order_id''',(order_id,))
                    res[order_id]= [0.00,0.00]
                    
                    for oid,nbr,state in cr.fetchall():
                        
                        if state=='cancel':
                            continue
                        if state=='done':
                            
                            res[oid][0] += nbr or 0.0
                            res[oid][1] += nbr or 0.0
                        else:
                            res[oid][1] += nbr or 0.0
                   
                    if not res[order_id][1]:
                        res[order_id] = 0.0
                    else:
                        res[order_id] = 100.0 * res[order_id][0] / res[order_id][1]

                    if res[order_id] > 0:
                        received = str(res[order_id] ) + '%'
                    else:
                        received = str(res[order_id] ) + '0%'
                    data={
                        'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                        'header1':header1,
                        'header2':header2,
                        'date':date,
                        'amount_total':amount_total,
                        'location':location,
                        'order_name':name,
                        'received':received,
                        'user':obj_user.name,
                    } 
                    result.append(data)
        return result

jasper_report.report_jasper('report.jasper_report_stock_order_print', 'stock.picking', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
