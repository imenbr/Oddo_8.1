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
            print 'hello from journal de vente' 
            obj_user = self.pool.get('res.users').browse(cr, uid, uid)
  
            datedebut = data['form']['date_debut']
            datefin = data['form']['date_fin']

            Annee = datedebut.split("-")[0]
            Mois = datedebut.split("-")[1]
            Jour = datedebut.split("-")[2]
            datedebut = Jour +"/"+ Mois +"/"+ Annee

            AnneeFin = datefin.split("-")[0]
            MoisFin = datefin.split("-")[1]
            JourFin = datefin.split("-")[2]
            datefin = JourFin +"/"+ MoisFin +"/"+ AnneeFin
            
            cr.execute(" Select * from account_invoice where (type = 'out_invoice' or type='out_refund') and state != 'cancel' and date_invoice >= %s and date_invoice <= %s  ORDER by date_invoice ",(data['form']['date_debut'], data['form']['date_fin']))
            invoices_list = cr.dictfetchall()
            recap_ttc_6 = 0
            recap_ttc_12 = 0
            recap_ttc_18 = 0
            somme_recap_ttc = 0
            somme_exoner = 0
            if len(invoices_list) > 0:
                for invoice in invoices_list:
                    
                    numero_facture = invoice['internal_number']
                    ref_fournisseur = invoice['reference']
                    datefacturation = invoice['date_invoice']   
                   
                    if datefacturation:                
                        datefacturation = datefacturation.split('-')[2]+'/'+datefacturation.split('-')[1]+'/'+datefacturation.split('-')[0]
                    montant_facture= round(invoice['amount_total'],3)             
                    
                    amount_untaxed = round(invoice['amount_untaxed'],3)    
                    amount_tax = round(invoice['amount_tax'],3)    
                    timbre = round(invoice['timbre'],3)  
                    #discount_total = round(invoice['discount_total'],3) 
                    #undiscount_total = round(invoice['undiscount_total'],3) 
                    facture= self.pool.get('account.invoice').browse(cr, uid, invoice['id'])
                    tva6 = 0
                    tva12 = 0
                    tva18 = 0
                    
                    base_tva6 = 0
                    base_tva12 = 0
                    base_tva18 = 0
                    exoner = 0
                    signe = 1
                    type_fact = 'Facture'
                    if facture.type == 'out_refund':
                        signe = -1 
                        type_fact = 'Avoir'
                    
                    partner = self.pool.get('res.partner').browse(cr, uid, invoice['partner_id'])
                    rs_fournisseur= partner.name
                    #tva info
                    if invoice['amount_tax'] > 0:
                        for line in facture.tax_line:
                            print 'line tax name:::::::::::::::::::::::::::::',line.name
                            if (line.name == 'TVA encaissement 6.0 % - TVA collectee  sur les encaissements 6%') :
                                tva6 = line.amount
                                base_tva6 = line.base
                                recap_ttc_6 += signe * ( base_tva6 + tva6)
                            if (line.name == ' TVA encaissement 18.0 % - TVA collectee  sur les encaissements ' ):
                                tva18 = line.amount
                                base_tva18 = line.base
                                recap_ttc_18 += signe * ( base_tva18 + tva18)
                            if (line.name == 'TVA encaissement 12.0 % - TVA collectee  sur les encaissements 1'):
                                tva12 = line.amount
                                base_tva12 = line.base
                                recap_ttc_12 += signe * ( base_tva12 + tva12)
                 
                    #partner info
                    
                    if invoice['amount_tax'] > 0:
                        exoner = 0
                        amount_total = montant_facture
                        
                    else:
                        exoner = montant_facture
                        somme_exoner += signe * exoner
                        amount_total = 0
                        amount_untaxed = 0
                    somme_recap_ttc = recap_ttc_18 +  recap_ttc_12 + recap_ttc_6 + somme_exoner
                    somme_total = montant_facture
                    
                    data={
                           'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                           'type':type_fact,
                           'raison_socaile':rs_fournisseur,
                           'numerofacture':numero_facture,
                           'datefacturation':datefacturation,
                           'montant_facture':signe * amount_total,
                           'montant_ht':signe * amount_untaxed,
                           'timbre':round(signe * timbre,3),
                           'tva6':round(signe * tva6,3),
                           'tva12':round(signe * tva12,3),
                           'tva18':round(signe * tva18,3) ,
                           'base_tva6':round(signe * base_tva6,3),
                           'base_tva18':round(signe * base_tva18,3),
                           'base_tva12':round(signe * base_tva12,3),
                           'exoner':signe * exoner,
                           'recap_ttc_6':round(recap_ttc_6,3),
                           'recap_ttc_18':round(recap_ttc_18,3),
                           'recap_ttc_12':round(recap_ttc_12,3),
                           'somme_recap_ttc':round(somme_recap_ttc,3),
                           'amount_tax':round(signe * amount_tax,3),
                           'total_general':signe * round(somme_total,3),
                           'from':datedebut,
                           'to':datefin,
                           'user':obj_user.name,
                    } 
                    result.append(data)    
        return result

jasper_report.report_jasper('report.jasper_journal_vente_print', 'account.invoice', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
