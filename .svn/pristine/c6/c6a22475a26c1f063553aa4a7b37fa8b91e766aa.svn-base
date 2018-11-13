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
            date_aujourd = data['form']['date_aujourd']
            date_fin  = data['form']['date_fin']
            date_debut = data['form']['date_debut']
            compte_biat = data['form']['compte_biat']
            compte_zitouna= data['form']['compte_zitouna']
            total=0
            #cheque_antidates = data['form']['cheque_antidates']
            
            #factures_clients = data['form']['factures_clients']
            #solde_caisse = data['form']['solde_caisse']
            #cheque_circ = data['form']['cheque_circ']
            #fact_etrangr = data['form']['fact_etrangr']
            #fact_locaux  = data['form']['fact_locaux']
            #stock = data['form']['stock']
            #print "compte_biat******************",   compte_biat   
            ####debut
            #montant facture clients non payées 
            factures_clients=0
            fact_ids = self.pool.get('account.invoice').search(cr, uid, [('date_invoice','>=',date_debut),('date_invoice','<=',date_fin),('state','not in',['paid']),('type','=','out_invoice')])
            fact_objs = self.pool.get('account.invoice').browse(cr, uid, fact_ids)
	
	        #res['factures_clients'] =factures_clients
            if fact_objs:
                for fact in fact_objs:	
                    factures_clients=factures_clients+fact.reste_a_payer
		        #res['factures_clients'] =factures_clients	
	

	        #montant cheque antidates
            cheque_antidates=0
	        #res['cheque_antidates'] =cheque_antidates
            pieces_ids = self.pool.get('reglement.piece').search(cr, uid, [('date_echance','>',date_aujourd),('mode_reglement','=','Chèque'),('type','=','out'),('state','=','integrated')])   
            pieces_objs = self.pool.get('reglement.piece').browse(cr, uid, pieces_ids)
            if pieces_objs:
                for piece in pieces_objs:
                    cheque_antidates=cheque_antidates+piece.montant_piece
		        #res['cheque_antidates'] =cheque_antidates

	
	        #solde caisse ouverte
            solde_caisse=0
	        #res['solde_caisse'] =solde_caisse
            cash_ids = self.pool.get('account.bank.statement').search(cr, uid, [('state','=','open')])
            cash_objs = self.pool.get('account.bank.statement').browse(cr, uid, cash_ids)
            if cash_objs:
                for cash in cash_objs:
                    solde_caisse=solde_caisse+cash.balance_end_real
		        #res['solde_caisse'] =solde_caisse
		
	        #montant cheque en circulation
            cheque_circ=0
	        #res['cheque_circ'] =cheque_circ
            cheq_ids = self.pool.get('reglement.piece').search(cr, uid, [('date_encaissement','>',date_debut),('mode_reglement','=','Chèque'),('type','=','in'),('state','=','integrated')])
                    
            cheq_objs = self.pool.get('reglement.piece').browse(cr, uid, cheq_ids)
            if cheq_objs:
                for cheq in cheq_objs:
                    cheque_circ=cheque_circ+cheq.montant_piece
		        #res['cheque_circ'] =cheque_circ


	        #factures fourns entrangere
            fact_etrangr=0
	        #res['fact_etrangr'] =fact_etrangr
            facture_ids = self.pool.get('account.invoice').search(cr, uid, [('date_invoice','>=',date_debut),('date_invoice','<=',date_fin),('state','not in',['paid','draft']),('type','=','in_invoice'),('currency_id','!=','TND')])
                    
            facture_objs = self.pool.get('account.invoice').browse(cr, uid, facture_ids)
            if facture_objs:		
                for facture in facture_objs:
                    currency=facture.currency_id.id,
                    currency_obj = self.pool.get('res.currency').browse(cr,uid,currency,context=context)
                    rate = currency_obj.rate_silent
                    montant_local=facture.reste_a_payer / rate
                    fact_etrangr=fact_etrangr+montant_local
		        #res['fact_etrangr'] =fact_etrangr		


	        #facture fourns locaux
            local_ids = self.pool.get('account.invoice').search(cr, uid, [('date_invoice','>=',date_debut),('date_invoice','<=',date_fin),('state','not in',['draft','paid']),('type','=','in_invoice'),('currency_id','=','TND')])
                    
            local_objs = self.pool.get('account.invoice').browse(cr, uid, local_ids)
            fact_locaux=0
	        #res['fact_locaux'] =fact_locaux
            if local_objs:
                for facture in local_objs:
                    fact_locaux=fact_locaux+facture.reste_a_payer
		        #res['fact_locaux'] =fact_locaux


	        #res_final = {'value':res}
		
	        # Stock
            stock=0
	        #res['stock'] =stock
            cr.execute('SELECT * FROM product_product')
            products = cr.dictfetchall()
            if len(products)>0 :
                for product in products:
                    prod_ids = self.pool.get('product.template').search(cr, uid, [('product_variant_ids','=',product['id'])])
                    prod_objs=self.pool.get('product.template').browse(cr,uid,prod_ids,context=context)
                    prodd_ids = self.pool.get('product.product').search(cr, uid, [('id','=',product['id'])])
                    prodd_objs=self.pool.get('product.product').browse(cr,uid,prodd_ids,context=context)
                    purchase_price=prod_objs.purchase_price
                    print "purchase_price",purchase_price
			        #Qte=product['qty_available']
                    Qte=prodd_objs.qty_available
                    print "Qteeeeeeeeeeeee==",Qte
                    stock=stock+(purchase_price*Qte)
		        #res['stock'] =stock
            #cautions et grantie
            total=compte_biat+compte_zitouna+cheque_antidates+factures_clients+stock+solde_caisse-(cheque_circ+fact_etrangr+fact_locaux)
            ####fin  
            data={
                'compte_biat':compte_biat,
                'compte_zitouna':compte_zitouna,
                'cheque_antidates':cheque_antidates,
                'factures_clients':factures_clients,
                'solde_caisse':solde_caisse,
                'cheque_circ':cheque_circ,
                'fact_etrangr':fact_etrangr,
                'fact_locaux':fact_locaux,
                'stock':stock,
                'total':total,
                #'cautions':
                            
                         
            } 
            result.append(data)
                  
        return result

jasper_report.report_jasper('report.jasper_etat_profit_print', 'account.invoice', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
