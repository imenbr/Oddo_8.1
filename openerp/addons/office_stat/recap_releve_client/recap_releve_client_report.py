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
from openerp import pooler
import time
from datetime import datetime
import base64
import os
#import netsvc
from openerp.osv import fields, osv
from openerp.tools.translate import _

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
        ReportCredit=0.0
        ReportDebit=0.0
        
        solde = 0.0
  
        if 'form' in data:                                                                                              
            obj_user = self.pool.get('res.users').browse(cr, uid, uid)
            type_affichage = data['form']['type_affichage']
            print 'type_affichage',type_affichage
            
            cr.execute(" Select * from res_partner where customer = 'True' order by name")
            fournisseurs=cr.dictfetchall()
            for fournisseur in fournisseurs:
                ReportCredit=0.0
                ReportDebit=0.0
                affich = 0
                fournisseur_id = fournisseur['id']
                RaisonSocial = fournisseur['name']
            
                #**************************************** Montant en espece *********************************
                cr.execute("SELECT * FROM reglement_paiement where partner_id = %s and state = 'close' and type='out' ",  (fournisseur_id,))
                reglements = cr.dictfetchall()
                for reglement in reglements:                
                    if reglement['montant_espece'] > 0:
                        #ReportDebit += reglement['montant_espece']
                        ReportCredit += reglement['montant_espece']
                        affich = 1
                #rim modif :: sttc : penalite de reatrd
                #**************************************** Montant penalite *********************************
                #cr.execute("SELECT * FROM reglement_paiement where partner_id = %s and state = 'close' and type='out' ",  (fournisseur_id,))
                #reglements = cr.dictfetchall()
                #for reglement in reglements:                
                #    if reglement['montant_espece'] > 0:
                #        #ReportDebit += reglement['montant_penalite']
                #        ReportCredit += reglement['montant_penalite']
                #        affich = 1
                #**************************************** Retenue a la source *********************************
                cr.execute("SELECT * FROM reglement_retenu_source where partner_id = %s and state = 'close' and type='out'",  (fournisseur_id,))
                retenues = cr.dictfetchall()
                for retenue in retenues: 
                    #ReportDebit += retenue['total_retenu']
                    ReportCredit += retenue['total_retenu']
                    affich = 1
                #**************************************** Facture Fournisseur *********************************
                cr.execute("select * FROM account_invoice where type='out_invoice' and partner_id = %s",  (fournisseur_id,))
                invoices = cr.dictfetchall()
                for invoice in invoices:   
                    #ReportCredit += invoice['amount_total']
                    ReportDebit += invoice['amount_total']
                    affich = 1
                #**************************************** Facture Avoir Fournisseur *********************************
                cr.execute("select * FROM account_invoice where type='out_refund' and partner_id = %s",  (fournisseur_id,))
                invoices = cr.dictfetchall()
                for invoice in invoices:  
                    #ReportDebit += invoice['amount_total'] 
                    ReportCredit += invoice['amount_total'] 
                    affich = 1
                #**************************************** PIECE PAIEMENT :: CHQ TRT ************************************
                cr.execute("select * FROM reglement_piece,reglement_mode where reglement_piece.mode_reglement = reglement_mode.id and reglement_piece.partner_id = %s and reglement_piece.type='out' and reglement_piece.state='cashed' and (reglement_mode.code ='CHQ' or  reglement_mode.code ='TRT') ",  (fournisseur_id,))
            
                pieces = cr.dictfetchall()
                for piece in pieces:  
                    #ReportDebit += piece['montant_piece']
                    ReportCredit += piece['montant_piece']
                    affich = 1

                #**************************************** PIECE PAIEMENT :: ESP VIR ************************************
                cr.execute("select * FROM reglement_piece,reglement_mode where reglement_piece.mode_reglement = reglement_mode.id and reglement_piece.partner_id = %s and reglement_piece.type='out' and (reglement_mode.code ='ESP' or  reglement_mode.code ='VIR')",  (fournisseur_id,))
                pieces = cr.dictfetchall()
                for piece in pieces:  
                    #ReportDebit += piece['montant_piece']
                    ReportCredit += piece['montant_piece']
                    affich = 1
           
                #**************************************** Total precedant ************************************            
                solde = round (ReportDebit-ReportCredit,3)
                if affich==1:   
                    if type_affichage == 'all':
                        data={
                        'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                        'raison_social':RaisonSocial,
                        'debit':round(ReportDebit,3),
                        'credit':round(ReportCredit,3),
                        'solde':solde,
                        'user':obj_user.name,
                        } 
                        result.append(data)  
                    else:
                        if solde != 0:
                            data={
                        'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                        'raison_social':RaisonSocial,
                        'debit':round(ReportDebit,3),
                        'credit':round(ReportCredit,3),
                        'solde':solde,
                        'user':obj_user.name,
                        } 
                        result.append(data)  
        return result
jasper_report.report_jasper('report.jasper_rapport_recap_releve_client_print', 'reglement.piece', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
