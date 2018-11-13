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
#import time, datetime
#import base64
#import os
#import netsvc

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
            header2 = 'header1'#obj_company['parametre2']
            obj_user = self.pool.get('res.users').browse(cr, uid, uid)
            inventory_id = data['form']['inventory_id']          
            inventory = self.pool.get('stock.inventory').browse(cr, uid, inventory_id[0])
            
            inv_date = inventory.date.split(" ")[0]
            inv_date = inv_date.split("-")[2]+"/"+inv_date.split("-")[1]+"/"+inv_date.split("-")[0]
            for line in inventory.line_ids:
                data={
                            'header1':header1,
                            'header2':header2,
                            'location':inventory.location_id.name,
                            'produit':line.product_id.name,
                            'ref':line.product_id.default_code,
                            'unite':line.product_id.uom_id.name,     
                } 
                result.append(data)
        return result

jasper_report.report_jasper('report.jasper_report_stock_inventory_print', 'stock.inventory', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
