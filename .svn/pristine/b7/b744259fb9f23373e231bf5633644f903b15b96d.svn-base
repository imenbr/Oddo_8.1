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
            from_date = data['form']['date_debut']
            to_date = data['form']['date_fin']
            caisse_id = data['form']['caisse_id']
            print "caissssssssssssssssse ===",caisse_id[1]
            cash_ids = pool.get('account.bank.statement').search(cr, uid, [('name','in',caisse_id)])
            cash_objs = pool.get('account.bank.statement').browse(cr, uid, cash_ids)
            cash_line_ids = self.pool.get('account.bank.statement.line').search(cr, uid, [('statement_id','=',caisse_id[0]),('date','>=',from_date),('date','<=',to_date)])
            #('date','>=',from_date),('date','<=',to_date)
            cash_line_objs = pool.get('account.bank.statement.line').browse(cr, uid, cash_line_ids)
            if cash_line_objs:
                for cash in cash_line_objs:
                    data={
                        'date_op':cash.date,
                        'nom_so':cash.partner_id.id,
                        'Designation':cash.name,
                        'reference':cash.ref,
                        'montant':cash.amount,
                        'solde_ouverture':cash_objs.balance_start,
                        'solde_final':cash_objs.balance_end_real,
                        'caisse':caisse_id[1],
                    } 
                    result.append(data)
            else :
                data={
                        'date_op':'',
                        'nom_so':'',
                        'Designation':'',
                        'reference':'',
                        'montant':'',
                        'solde_ouverture':'',
                        'solde_final':'',
                        'caisse':caisse_id[1],
                } 
                result.append(data)
                        
        return result

jasper_report.report_jasper('report.jasper_caisse_locaux_print', 'account.bank.statement', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
