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
from osv import fields, osv, orm
from tools.translate import _

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
            br_facturer='invoiced'
            br_brouilons='draft'
            cr.execute("SELECT parametre1,parametre2 FROM res_company WHERE id = 1")
            obj_company = cr.dictfetchone()
            header1 = obj_company['parametre1']
            header2 = obj_company['parametre2'] 
            obj_user = self.pool.get('res.users').browse(cr, uid, uid)
            #emp_ids = self.pool.get('hr.employee').search(cr, uid, [('active','=',True)], context=context)
            fourniseur_id = data['form']['fournisseur_id2']
            print 'fourniseur_id!!!!!=',fourniseur_id
            cr.execute(" Select * from res_partner where id = %s ", (fourniseur_id,))
            fournisseur=cr.dictfetchone()
            rs_fournisseur= fournisseur['name']
            ref_fournisseur= fournisseur['ref']
            mat_fournisseur= fournisseur['mf']
            cr.execute(" Select * from stock_picking where partner_id = %s and  invoice_state != %s and  state != %s",(fourniseur_id,br_facturer,br_brouilons))
            listedesBonreception_nonFacturer= cr.dictfetchall()
            if len(listedesBonreception_nonFacturer) > 0:
               print 'listedesBonreception_nonFacturer!!!=',listedesBonreception_nonFacturer
               for BonReception_nonFacturer in listedesBonreception_nonFacturer:
                   Bonreception_id = BonReception_nonFacturer['id']
                   Bonreception_numero = BonReception_nonFacturer['name']
                   Bonreception_date0 = BonReception_nonFacturer['date'].split("-")[0]
                   Bonreception_date1 = BonReception_nonFacturer['date'].split("-")[1]
                   Bonreception_date2 = BonReception_nonFacturer['date'].split("-")[2]
                   Bonreception_date3 = Bonreception_date2.split(" ")[0]
                   Bonreception_date=Bonreception_date3 +"/"+ Bonreception_date1 +"/"+ Bonreception_date0
                   cr.execute(" Select * from stock_move where picking_id = %s ",(Bonreception_id,))  
                   listestockmouve= cr.dictfetchall()
                   if len(listestockmouve) > 0:
                      print 'listestockmouve!!!=',listestockmouve
                      for stock_mouve in listestockmouve:
                          qte_product= round(stock_mouve['product_qty'],0)
                          MT_Totale_Ligne= round(stock_mouve['price_subtotal'],3) 
                          Product_id = stock_mouve['product_id']
                          obj_UDM = self.pool.get('product.uom').browse(cr, uid, stock_mouve['product_uom'])
                          obj_Location = self.pool.get('stock.location').browse(cr, uid, stock_mouve['location_dest_id'])
                          udm=obj_UDM.name
                          chantier=obj_Location.name
                          data={
                          'header1':header1,
                          'header2':header2,
                          'raison_sociale':rs_fournisseur,
                          'matricule_fiscale':mat_fournisseur,
                          'ref_fournisseur':ref_fournisseur,
                          'num_BonReception':Bonreception_numero,
                          'date_br':Bonreception_date,
                          'designation_article':stock_mouve['name'],
                          'qte_article':qte_product,
                          'num_article':stock_mouve['default_code'],
                          'product_udm':udm,
                          'chantier':chantier,
                          'montant_article':MT_Totale_Ligne,
                          'user':obj_user.name,
                          
                   
                          } 
                          result.append(data)
           
                   
            
            
                        
        return result

jasper_report.report_jasper('report.jasper_br_non_facturer_print', 'stock.move', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
