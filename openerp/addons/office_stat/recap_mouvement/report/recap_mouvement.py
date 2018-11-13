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
            
            nb_annee = int(datefin)- int(datedebut)
            
            count = 0
            current_year = int(datedebut)
            
            if nb_annee > 0:
              
                while count <= nb_annee:
                    count_month = 1
                    while count_month <= 12:   
                        somme_total = 0
                        cr.execute(" Select COALESCE(sum(amount_total),0) as somme_amount_total, COALESCE(sum(amount_untaxed),0) as somme_amount_untaxed, COALESCE(sum(amount_tax),0) as somme_amount_tax,COALESCE(sum(timbre),0) as somme_timbre from account_invoice where type = 'out_invoice' and state != 'cancel' and (extract(MONTH from date_invoice)=%s) AND (extract(YEAR from date_invoice)=%s) ",(count_month, current_year))
                        invoices_list = cr.dictfetchone()
                        #calculer somme montant avoir 
                        cr.execute(" Select COALESCE(sum(amount_total),0) as somme_refund from account_invoice where type = 'out_refund' and state != 'cancel' and (extract(MONTH from date_invoice)=%s) AND (extract(YEAR from date_invoice)=%s) ",(count_month, current_year))
                        refund_list = cr.dictfetchone()
                        #calculer montant exoner ::seulement somme des factures des partenaires exoner
                        #cr.execute(" Select COALESCE(sum(amount_total),0) as total from account_invoice,res_partner where account_invoice.partner_id = res_partner.id and res_partner.exoner=True and account_invoice.type = 'out_invoice' and account_invoice.state != 'cancel' and (extract(MONTH from date_invoice)=%s) AND (extract(YEAR from date_invoice)=%s) ",(count_month, current_year))
                        cr.execute(" Select COALESCE(sum(amount_total),0) as total from account_invoice,res_partner WHERE amount_tax <= 0 and account_invoice.type = 'out_invoice' and account_invoice.state != 'cancel' and (extract(MONTH from date_invoice)=%s) AND (extract(YEAR from date_invoice)=%s) ",(count_month, current_year))
                        exonere_list = cr.dictfetchone()
                        #calculer montant ttc et tva:: seulement somme des factures ayant des tva
                        cr.execute(" Select COALESCE(sum(amount_total),0) as somme_amount_total , COALESCE(sum(amount_tax),0) as somme_amount_tax from account_invoice WHERE amount_tax > 0 and type = 'out_invoice' and state != 'cancel' and (extract(MONTH from date_invoice)=%s) AND (extract(YEAR from date_invoice)=%s) ",(count_month, current_year))
                        somme_ttc_tva = cr.dictfetchone()
                        # colonne total general = somme total ttc (pour les factures avec tva) + somme des factures des clients exoner - somme des avoirs
                        somme_total = round(somme_ttc_tva['somme_amount_total'],3) + round(exonere_list['total'],3) - round(refund_list['somme_refund'],3)
                        data={
                            'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                            'month':count_month,
                            'year':current_year,
                            'somme_exonere':round(exonere_list['total'],3),
                            'somme_ttc':round(somme_ttc_tva['somme_amount_total'],3),
                            'somme_montant_ht':round(invoices_list['somme_amount_untaxed'],3),
                            'somme_amount_tax':round(somme_ttc_tva['somme_amount_tax'],3),
                            'somme_timbre':round(invoices_list['somme_timbre'],3),
                            'somme_avoir':round(refund_list['somme_refund'],3),
                            'total_general':round(somme_total,3),
                            'from':datedebut,
                            'to':datefin,
                            'user':obj_user.name,
                        } 
                        result.append(data) 
                        count_month += 1
                    current_year += 1
                    count += 1
                  
            elif nb_annee == 0:
         
                count_month = 1
                while count_month <= 12:   
                        somme_total = 0
                        cr.execute(" Select COALESCE(sum(amount_total),0) as somme_amount_total, COALESCE(sum(amount_untaxed),0) as somme_amount_untaxed, COALESCE(sum(amount_tax),0) as somme_amount_tax,COALESCE(sum(timbre),0) as somme_timbre from account_invoice where type = 'out_invoice' and state != 'cancel' and (extract(MONTH from date_invoice)=%s) AND (extract(YEAR from date_invoice)=%s) ",(count_month, current_year))
                        invoices_list = cr.dictfetchone()
                        #calculer somme montant avoir 
                        cr.execute(" Select COALESCE(sum(amount_total),0) as somme_refund from account_invoice where type = 'out_refund' and state != 'cancel' and (extract(MONTH from date_invoice)=%s) AND (extract(YEAR from date_invoice)=%s) ",(count_month, current_year))
                        refund_list = cr.dictfetchone()
                        #calculer montant exoner ::seulement somme des factures des partenaires exoner
                        #cr.execute(" Select COALESCE(sum(amount_total),0) as total from account_invoice,res_partner where account_invoice.partner_id = res_partner.id and res_partner.exoner=True and account_invoice.type = 'out_invoice' and account_invoice.state != 'cancel' and (extract(MONTH from date_invoice)=%s) AND (extract(YEAR from date_invoice)=%s) ",(count_month, current_year))
                        cr.execute(" Select COALESCE(sum(amount_total),0) as total from account_invoice,res_partner WHERE amount_tax <= 0 and account_invoice.type = 'out_invoice' and account_invoice.state != 'cancel' and (extract(MONTH from date_invoice)=%s) AND (extract(YEAR from date_invoice)=%s) ",(count_month, current_year))
                        exonere_list = cr.dictfetchone()
                        #calculer montant ttc et tva:: seulement somme des factures ayant des tva
                        cr.execute(" Select COALESCE(sum(amount_total),0) as somme_amount_total , COALESCE(sum(amount_tax),0) as somme_amount_tax from account_invoice WHERE amount_tax > 0 and type = 'out_invoice' and state != 'cancel' and (extract(MONTH from date_invoice)=%s) AND (extract(YEAR from date_invoice)=%s) ",(count_month, current_year))
                        somme_ttc_tva = cr.dictfetchone()
                        # colonne total general = somme total ttc (pour les factures avec tva) + somme des factures des clients exoner - somme des avoirs
                        somme_total = round(somme_ttc_tva['somme_amount_total'],3) + round(exonere_list['total'],3) - round(refund_list['somme_refund'],3)
                        data={
                            'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                            'month':count_month,
                            'year':current_year,
                            'somme_exonere':round(exonere_list['total'],3),
                            'somme_ttc':round(somme_ttc_tva['somme_amount_total'],3),
                            'somme_montant_ht':round(invoices_list['somme_amount_untaxed'],3),
                            'somme_amount_tax':round(somme_ttc_tva['somme_amount_tax'],3),
                            'somme_timbre':round(invoices_list['somme_timbre'],3),
                            'somme_avoir':round(refund_list['somme_refund'],3),
                            'total_general':round(somme_total,3),
                            'from':datedebut,
                            'to':datefin,
                            'user':obj_user.name,
                        } 
                        result.append(data)  
                        
                        #invoices_list = cr.dictfetchall()
                        count_month += 1
                    
            else:
                raise osv.except_osv(_('Avertissement !'),_("Verifier année début et année fin "))
              
        return result

jasper_report.report_jasper('report.jasper_recap_mouvement_print', 'account.invoice', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
