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
        if 'form' in data:
            obj_user = self.pool.get('res.users').browse(cr, uid, uid)
  
            datedebut = data['form']['date_debut']
            datefin = data['form']['date_fin']

            #Annee = datedebut.split("-")[0]
            #Mois = datedebut.split("-")[1]
            #Jour = datedebut.split("-")[2]

            #datedebut = Jour +"/"+ Mois +"/"+ Annee
            #AnneeFin = datefin.split("-")[0]
            #MoisFin = datefin.split("-")[1]
            #JourFin = datefin.split("-")[2]
            #datefin = JourFin +"/"+ MoisFin +"/"+ AnneeFin
            
            cr.execute(" Select * from account_invoice where ( type = 'in_invoice' or type='in_refund') and state != 'cancel' and date_invoice >= %s and date_invoice <= %s  ORDER by date_invoice ",(datedebut, datefin,))
            invoices_list = cr.dictfetchall()
            #print "invoices_list",invoices_list
            somme_ttc6 = 0
            somme_ttc12 = 0
            somme_ttc18 = 0
            somme_base6 = 0
            somme_base12 = 0
            somme_base18 = 0
            somme_tva6 = 0
            somme_tva12 = 0
            somme_tva18 = 0

            if len(invoices_list) > 0:
                for invoice in invoices_list:
                    #initialisation
                    signe = 1
                    exoner = 0
                    ttc = 0
                    tva18 = 0
                    tva12 = 0
                    tva6 = 0
                    base0 = 0
                    base18 = 0
                    base12 = 0
                    base6 = 0
                    total = 0
                    timbre = 0
                    tva18_found = 0
                    tva12_found = 0
                    tva6_found = 0

                    cr.execute(" Select * from res_partner where id = %s ", (invoice['partner_id']  ,))
                    fournisseur=cr.dictfetchone()
                    rs_fournisseur= fournisseur['name']
                
                    if (invoice['type'] == 'in_refund'):
                        signe = -1
                    
                    numero_facture = invoice['internal_number']
                    ref_fournisseur = invoice['reference']
                    datefacturation = invoice['date_invoice']   
                   
                    if datefacturation:                
                        datefacturation = datefacturation.split('-')[2]+'/'+datefacturation.split('-')[1]+'/'+datefacturation.split('-')[0]
                    # si fournisseur exonere et pas de taxe
                    if fournisseur['exoner'] and invoice['amount_tax'] <= 0:
                        exoner = round(invoice['amount_total'],3)
                        total = exoner
                    else:    
                        ttc = round(invoice['amount_total'],3)             
                        total = ttc
                          
                    amount_untaxed = round(invoice['amount_untaxed'],3)    
                    facture= self.pool.get('account.invoice').browse(cr, uid, invoice['id'])
                    print 'facture.tax_line',facture.tax_line
                    for line in facture.tax_line:
                        print 'line',line
                        print 'line.name:::',line.name,"::::::"
                        if (line.name == u"ACHAT-18.0 %  - TVA sur autres biens et services  (achat) 18.0%") or (line.name == '18%'):
                            tva18 = line.amount
                            base18 = line.base
                            print "tva18 :::::::::::::::::",tva18
                            print "base18 :::::::::::::::::",base18
                            somme_base18 += signe * base18
                            somme_tva18 += signe * tva18 
                            if tva18 > 0:
                                tva18_found = 1
                        if (line.name == u"ACHAT-12.0 %  - TVA sur autres biens et services  (achat) 12.0%") or (line.name =='ACHAT-12.0 ') or (line.name == 'ACHAT-12.0%'):
                            tva12 = line.amount
                            base12 = line.base
                            print "tva12 :::::::::::::::::",tva12
                            print "base12 :::::::::::::::::",base12
                            somme_base12 += signe * base12
                            somme_tva12 += signe * tva12
                            if tva12 > 0:
                                tva12_found = 1
                        if (line.name == u"ACHAT-6.0 - TVA sur autres biens et services  (achat) 6.0%") or (line.name ==' 6%'):
                            tva6 = line.amount
                            base6 = line.base
                            print "tva6 :::::::::::::::::",tva6
                            print "base6 :::::::::::::::::",base6
                            somme_base6 += signe * base6
                            somme_tva6 += signe * tva6 
                            if tva6 > 0:
                                tva6_found = 1
                        if line.name == '0%' or line.name == '  0%' :
                            base0 = line.base

                    # calculer (ou cumuler) les ttc des factures avec tva 6 pour le recap
                    if tva6_found == 1:
                        somme_ttc6 += signe * round(invoice['amount_total'],3)
                    # calculer (ou cumuler) les ttc des factures avec tva 12 pour le recap
                    if tva12_found == 1:
                        somme_ttc12 += signe * round(invoice['amount_total'],3)
                    # calculer (en cumuler) les ttc des factures avec tva 18 pour le recap
                    if tva18_found == 1:
                        somme_ttc18 += signe * round(invoice['amount_total'],3)
                    data={
                           'raison_socaile':rs_fournisseur,
                           'numerofacture':numero_facture,
                           'datefacturation':datefacturation,
                           'montant_facture':signe * round(ttc,3),
                           'montant_ht':signe * round(amount_untaxed,3),
                           'tva12':signe * round(tva12,3),
                           'tva6':signe * round(tva6,3),
                           'tva18':signe * round(tva18,3) ,
                           'base0':signe * round(base0,3),
                           'base12':signe * round(base12,3),
                           'base6':signe * round(base6,3),
                           'base18':signe * round(base18,3),
                           'timbre':signe * round(timbre,3),
                           'exoner':signe * round(exoner,3),
                           'tot_general':signe * round(total,3),
                           'recap_ttc12':round(somme_ttc12,3),
                           'recap_ttc6':round(somme_ttc6,3),
                           'recap_ttc18':round(somme_ttc18,3),
                           'recap_somme_tva':round(somme_tva6 + somme_tva12 + somme_tva18,3),
                           'recap_somme_base':round(somme_base6 + somme_base12 + somme_base18,3),
                           'recap_somme_ttc':round(somme_ttc12 + somme_ttc12 + somme_ttc18,3),
                           'user':obj_user.name,
                    } 
                    result.append(data)    
                    print 'data:::::::::::::::',data
        return result

jasper_report.report_jasper('report.jasper_tva_achat_print', 'account.invoice', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
