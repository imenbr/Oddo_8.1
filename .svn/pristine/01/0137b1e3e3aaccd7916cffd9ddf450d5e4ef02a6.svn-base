# -*- coding: utf-8 -*-
##############################################################################
#
#    Cash Management Module, Specific module for Cash Management Solution
#    Copyright (C) 2013-20xx Rim BEN DHAOU.
#
#    This module is not free !!!!!: you can't redistribute it !!!!!
#
#    This program is developeded in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
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
            from_date = data['form']['from_date']
            to_date = data['form']['to_date']
            user_ids = data['form']['user_ids']            
            from_date_f=from_date.split("-")[2]+"/"+from_date.split("-")[1]+"/"+from_date.split("-")[0]
            to_date_f =to_date.split("-")[2]+"/"+to_date.split("-")[1]+"/"+to_date.split("-")[0]
            result=[]
            for user_id in user_ids :
                typ="out_refund" #avoir_client
                cr.execute('SELECT sum(amount_untaxed) as tot_credit_ht,sum(amount_total) as tot_credit_ttc FROM account_invoice WHERE date_invoice >=%s and date_invoice<=%s and partner_id=%s and type=%s group by partner_id ', (from_date,to_date,user_id,typ,))
                res=cr.dictfetchone()
                tot_credit_ht=0.0
                tot_credit_ttc=0.0
                if res:
                   tot_credit_ht= res['tot_credit_ht']
                   tot_credit_ttc= res['tot_credit_ttc']
                typ="out_invoice" #facture_client
                cr.execute('SELECT sum(amount_untaxed) as tot_debit_ht,sum(amount_total) as tot_debit_ttc  FROM account_invoice WHERE date_invoice >=%s and date_invoice<=%s and partner_id=%s and type=%s group by partner_id ', (from_date,to_date,user_id,typ,))
                res=cr.dictfetchone()
                tot_debit_ht=0.0
                tot_debit_ttc=0.0
                if res :
                   tot_debit_ht= res['tot_debit_ht']
                   tot_debit_ttc= res['tot_debit_ttc']
                cr.execute('SELECT name FROM res_partner WHERE id=%s ', (user_id,))
                partner= cr.dictfetchone()['name'] 
                ca_ht=tot_debit_ht-tot_credit_ht
                ca_ttc=tot_debit_ttc-tot_credit_ttc
                
                data={
                    'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                    'path':"",#os.getcwd(),  
                    'debit':tot_debit_ht, 
                    'credit':tot_credit_ht,            
                    'ca':ca_ht,   
                    'ca_ttc':ca_ttc,                 
                    'from_date': from_date_f,
                    'to_date': to_date_f,
                    'partner':partner,
                    }
                result.append(data)
        return result

jasper_report.report_jasper('report.jasper_report_turnover_client_print', 'res.users', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
