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
            fourniseur_id = data['form']['fournisseur_id']
            print 'fourniseur_id!!!!!=',fourniseur_id
            cr.execute(" Select * from res_partner where id = %s ", (fourniseur_id,))
            fournisseur=cr.dictfetchone()
            rs_fournisseur= fournisseur['name']
            ref_fournisseur= fournisseur['ref']
            mat_fournisseur= fournisseur['mf']
            cr.execute('''SELECT stock_move.id as move_id, 
                          stock_move.origin, 
                          stock_move.address_id, 
                          stock_move.product_uom, 
                          stock_move.price_unit, 
                          stock_move.date_expected, 
                          stock_move.date,
                          stock_move.prodlot_id,
                          stock_move.move_dest_id,
                          stock_move.product_qty  as qte, 
                          stock_move.product_uos, 
                          stock_move.location_id,
                          stock_move.name,
                          stock_move.note, 
                          stock_move.product_id, 
                          stock_move.auto_validate, 
                          stock_move.price_currency_id, 
                          stock_move.partner_id, 
                          stock_move.company_id, 
                          stock_move.picking_id, 
                          stock_move.priority, 
                          stock_move.state, 
                          stock_move.location_dest_id, 
                          stock_move.tracking_id, 
                          stock_move.product_packaging, 
                          stock_move.purchase_line_id, 
                          stock_move.sale_line_id, 
                          stock_move.production_id, 
                          stock_move.cancel_cascade, 
                          stock_move.invoice_id, 
                          stock_move.price_subtotal as montant_article_br, 
                          stock_move.default_code as code_prod, 
                          stock_move.account_id, 
                          stock_move.discount, 
                          stock_move.prod_qty_stock,
                          stock_picking.date as date_br,
                          stock_picking.name as name_br,
                          product_template.name as name_prod,
                          product_uom.name as name_uom,
                          
                          stock_location.name as chantier 
                FROM stock_move left outer join stock_picking on stock_move.picking_id = stock_picking.id 
                left outer join product_uom on stock_move.product_uom = product_uom.id 
                left outer join product_template on stock_move.product_id = product_template.id
                left outer join  stock_location  on  stock_move.location_dest_id = stock_location.id 
                where stock_picking.state != %s  and invoice_state!= %s and stock_picking.partner_id= %s
                ORDER BY stock_picking.date,stock_picking.name ''',(br_brouilons,br_facturer,fourniseur_id))
            listedesBonreception_nonFacturer= cr.dictfetchall()
            if len(listedesBonreception_nonFacturer) > 0:
               #print 'listedesBonreception_nonFacturer!!!=',listedesBonreception_nonFacturer
               for BonReception_nonFacturer in listedesBonreception_nonFacturer:
                   Bonreception_id = BonReception_nonFacturer['move_id']
                   
                   Bonreception_date0 = BonReception_nonFacturer['date_br'].split("-")[0]
                   Bonreception_date1 = BonReception_nonFacturer['date_br'].split("-")[1]
                   Bonreception_date2 = BonReception_nonFacturer['date_br'].split("-")[2]
                   Bonreception_date3 = Bonreception_date2.split(" ")[0]
                   date_br=Bonreception_date3 +"/"+ Bonreception_date1 +"/"+ Bonreception_date0
                   num_br= BonReception_nonFacturer['name_br']
                   designation_article_br= BonReception_nonFacturer['name_prod']
                   qte_product= round(BonReception_nonFacturer['qte'],3)
                   udm= BonReception_nonFacturer['name_uom']
                   chantier= BonReception_nonFacturer['chantier']
                   MT_HT_Totale_Ligne= round(BonReception_nonFacturer['montant_article_br'],3)
                   #rim modif 27/03/2014 
                   obj_move = self.pool.get('stock.move').browse(cr, uid, BonReception_nonFacturer['move_id'])
                   taxe_amount = 0
                   for taxe_id in obj_move.move_tax_id:
                       print 'taxe_id.amount::::::::',taxe_id.amount
                       #obj_taxe = self.pool.get('account.tax').browse(cr, uid, obj_move.move_tax_id.id)
                       taxe_amount += taxe_id.amount
                   
                   
                   #print 'obj_move.move_tax_id!!!!!!!!!!',obj_move.move_tax_id
                   MT_Totale_Ligne = MT_HT_Totale_Ligne + (MT_HT_Totale_Ligne * taxe_amount)
                   #cr.execute(" Select * from stock_move where picking_id = %s ",(Bonreception_id,))  
                   #listestockmouve= cr.dictfetchall()
                   #if len(listestockmouve) > 0:
                      #print 'listestockmouve!!!=',listestockmouve
                      #for stock_mouve in listestockmouve:
                          #qte_product= round(stock_mouve['product_qty'],0)
                          #MT_Totale_Ligne= round(stock_mouve['price_subtotal'],3) 
                          #Product_id = stock_mouve['product_id']
                          #obj_UDM = self.pool.get('product.uom').browse(cr, uid, stock_mouve['product_uom'])
                          #obj_Location = self.pool.get('stock.location').browse(cr, uid, stock_mouve['location_dest_id'])
                          #udm=obj_UDM.name
                          #chantier=obj_Location.name
                   data={
                   'header1':header1,
                   'header2':header2,
                   'raison_sociale':rs_fournisseur,
                   'matricule_fiscale':mat_fournisseur,
                   'ref_fournisseur':ref_fournisseur,
                   'num_BonReception':num_br,
                   'date_br':date_br,
                   'designation_article':designation_article_br,
                   'qte_article':qte_product,
                   'product_udm':udm,
                   'chantier':chantier,
                   'montant_article':MT_Totale_Ligne,
                   'user':obj_user.name,
                          
                   
                   } 
                   result.append(data)
              
        return result

jasper_report.report_jasper('report.jasper_br_non_facturer_grouper_print', 'stock.move', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
