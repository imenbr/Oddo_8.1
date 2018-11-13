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
import time, datetime
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
            obj_user = self.pool.get('res.users').browse(cr, uid, uid)
            
            cr.execute(" Select * from stock_picking where picking_type_id=1 and invoice_state !=  'invoiced' and state != 'cancel' ORDER by date")
            br_ids= cr.dictfetchall()
            if len(br_ids) > 0:
             
               for br in br_ids:
                   br_id = br['id']
                   br_numero = br['name']
                
                   partner = self.pool.get('res.partner').browse(cr, uid, br['partner_id'], context=context)
                   br_date =''
                   if br['date']:
                       br_date10 = br['date'].split(" ")[0] 
                       br_date0 = br_date10.split("-")[0]
                       br_date1 = br_date10.split("-")[1]
                       br_date2 = br_date10.split("-")[2]
                       #br_date0 = br['date'].split("-")[0]
                       #br_date1 = br['date'].split("-")[1]
                       #br_date2 = br['date'].split("-")[2]
                   
                       br_date = br_date2 +"/"+ br_date1 +"/"+ br_date0
                   
                   data={
                       'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                       'raison_sociale':partner.name,
                       'num_BonReception':br_numero,
                       'date_br':br_date,
                       'montant_ttc':br['amount_total'],
                       'montant_ht':br['amount_untaxed'],
                       'user':obj_user.name,
                   } 
                   result.append(data)
                  
            else: 
                data={
                    'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                    'raison_sociale':'',
                    'num_BonReception':'',
                    'date_br':'',
                    'montant_ttc':0,
                    'montant_ht':0,
                    'user':obj_user.name,
                    } 
                result.append(data)    
        print 'data::::::',data
        return result

jasper_report.report_jasper('report.jasper_br_non_facturer_print', 'stock.move', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
