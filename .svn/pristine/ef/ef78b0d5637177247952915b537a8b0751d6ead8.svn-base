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
            type_respart='in_invoice'
            facture_regler='paid'
            facture_brouilons='draft'
            obj_user = self.pool.get('res.users').browse(cr, uid, uid)
            #emp_ids = self.pool.get('hr.employee').search(cr, uid, [('active','=',True)], context=context)
            fourniseur_id = data['form']['fournisseur_id']
            cr.execute("SELECT parametre1,parametre2 FROM res_company WHERE id = 1")
            obj_company = cr.dictfetchone()
            header1 = obj_company['parametre1']
            header2 = obj_company['parametre2'] 
            cr.execute(" Select * from res_partner where id = %s ", (fourniseur_id,))
            fournisseur=cr.dictfetchone()
            rs_fournisseur= fournisseur['name']
            mf_fournisseur= fournisseur['mf']
            #rim modif 07/04/2014 comment this line
            #ref_fournisseur= fournisseur['ref']
            cr.execute(" Select * from account_invoice where partner_id = %s and type = %s and state != %s and  state != %s",(fourniseur_id,type_respart,facture_regler,facture_brouilons))
            listedesfacture_nonregler= cr.dictfetchall()
            if len(listedesfacture_nonregler) > 0:
               for facture_nonregler in listedesfacture_nonregler:
                   numero_facture = facture_nonregler['number']
                   #rim modif 07/04/2014
                   ref_fournisseur = facture_nonregler['reference']
                   datefacturation = facture_nonregler['date_invoice']
                   #rim modif 07/05/2014 :: format date
                   datefacturation = datefacturation.split('-')[2]+'/'+datefacturation.split('-')[1]+'/'+datefacturation.split('-')[0]
                   montant_facture= round(facture_nonregler['amount_total'],3)
                   #montant_payer= round(facture_nonregler['montant_paye'],3)                   
                   reste_a_payer=  round(facture_nonregler['residual'],3) 
                   
                             
                   retenue = facture_nonregler['montant_retenue'] or 0
                   montant_payer = round(facture_nonregler['montant_paye'],3)  - round(retenue,3)
                   data={
                       'header1':header1,
                       'header2':header2,
                       'raison_socaile':rs_fournisseur,
                       'matricule_fiscale':mf_fournisseur,
                       'numerofacture':numero_facture,
                       'datefacturation':datefacturation,
                       'reference_fournisseur':ref_fournisseur,
                       'montant_facture':montant_facture,
                       'montant_payer2':round(montant_payer,3),
                       'reste_a_payer2':reste_a_payer,
                       'retenue':round(retenue,3),
                       'user':obj_user.name,
                   } 
                   result.append(data)
                        
        return result

jasper_report.report_jasper('report.jasper_facture_fournisseur_nonregler_print', 'account.invoice', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
