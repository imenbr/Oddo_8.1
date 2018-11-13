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
        res={}
        result2=[]
        ReportCredit=0.0
        ReportCreditNull=0.000
        ReportDebit=0.0
        ReportDebitNull=0.000
        ReportDatePiece=''
        ReportLibellePiece='REPORT DE LA PERIODE PRECEDANTE'
        ReportNumeroPiece=''
        debit = 0.0
        credit =0.0
        solde = 0.0
        solde_precendant = 0.0
        if 'form' in data: 
                                                                                                            
            obj_user = self.pool.get('res.users').browse(cr, uid, uid)

            datedebut = data['form']['date_debut']
            datefin = data['form']['date_fin']


            print "datedebut ====> ",datedebut
            #print "datedebut ====> ",time.strptime(datedebut, '%d/%m/%Y %H:%M:%S')
            print "datefin ====> ",datefin
            #print "datefin ====> ",time.strptime(datefin, '%d/%m/%Y %H:%M:%S')

            ReportDatePiece = datedebut            
            fournisseur_id = data['form']['fournisseur_id']
            cr.execute(" Select * from res_partner where id = %s ", (fournisseur_id[0],))
            Fournisseur=cr.dictfetchone()
            RaisonSocial = Fournisseur['name']
            
            #first line
            #**************************************** Montant en espece precedant *********************************
            cr.execute("SELECT * FROM reglement_paiement where partner_id = %s and date_reglement <= %s and state = 'close' and type='out' ",  (fournisseur_id[0],datedebut,))
            reglements = cr.dictfetchall()
            for reglement in reglements:                
                if reglement['montant_espece'] > 0:
                    #ReportDebit += reglement['montant_espece']
                    ReportCredit += reglement['montant_espece']
                    
            #rim modif :: sttc :: penalite de reatrd
            #**************************************** PENALITE DE RETARD *********************************
            #cr.execute("SELECT * FROM reglement_paiement where partner_id = %s and date_reglement <= %s and state = 'close' and type='out' ",  (fournisseur_id[0],datedebut,))
            #reglements = cr.dictfetchall()
            #for reglement in reglements:                
            #    if reglement['montant_penalite'] > 0:
            #        ReportCredit += reglement['montant_penalite']

            #**************************************** Retenue a la source precedant *********************************
            cr.execute("SELECT * FROM reglement_retenu_source where partner_id = %s and date_retenu <= %s and state = 'close' and type='out' ",  (fournisseur_id[0],datedebut,))
            retenues = cr.dictfetchall()
            for retenue in retenues: 
                #ReportDebit += retenue['total_retenu']
                ReportCredit += retenue['total_retenu']
            #**************************************** Facture Fournisseur precedant *********************************
            cr.execute("select * FROM account_invoice where type='out_invoice' and partner_id = %s and date_invoice <= %s  ",  (fournisseur_id[0],datedebut,))
            invoices = cr.dictfetchall()
            for invoice in invoices:   
                #ReportCredit += invoice['amount_total']
                ReportDebit += invoice['amount_total']
            #**************************************** Facture Avoir Fournisseur precedant *********************************
            cr.execute("select * FROM account_invoice where type='out_refund' and partner_id = %s and date_invoice <= %s  ",  (fournisseur_id[0],datedebut,))
            invoices = cr.dictfetchall()
            for invoice in invoices:  
                #ReportDebit += invoice['amount_total'] 
                ReportCredit += invoice['amount_total'] 
            #**************************************** PIECE PAIEMENT precedant :: CHQ TRT ************************************
            cr.execute("select * FROM reglement_piece,reglement_mode where reglement_piece.mode_reglement = reglement_mode.id and reglement_piece.partner_id = %s and reglement_piece.type='out' and reglement_piece.date_encaissement <= %s  and reglement_piece.state='cashed' and (reglement_mode.code ='CHQ' or  reglement_mode.code ='TRT') ",  (fournisseur_id[0],datedebut,))
            
            pieces = cr.dictfetchall()
            for piece in pieces:  
                #ReportDebit += piece['montant_piece']
                ReportCredit += piece['montant_piece']
            #**************************************** PIECE PAIEMENT precedant :: ESP VIR ************************************
            cr.execute("select * FROM reglement_piece,reglement_mode where reglement_piece.mode_reglement = reglement_mode.id and reglement_piece.partner_id = %s and reglement_piece.type='out' and reglement_piece.date_encaissement <= %s and (reglement_mode.code ='ESP' or  reglement_mode.code ='VIR')",  (fournisseur_id[0],datedebut))
            pieces = cr.dictfetchall()
            for piece in pieces:  
                #ReportDebit += piece['montant_piece']
                ReportCredit += piece['montant_piece']
            #**************************************** Total precedant ************************************            
            solde_precedant = round (ReportDebit-ReportCredit,3)
            ReportDebit = round(ReportDebit,3)
            ReportCredit = round(ReportCredit,3)

            #**************************************** Facture Fournisseur  *********************************
            cr.execute("select * FROM account_invoice where type='out_invoice' and partner_id = %s and date_invoice >= %s and date_invoice <= %s  ",  (fournisseur_id[0],datedebut,datefin,))
            invoices = cr.dictfetchall()
            for invoice in invoices:   
                #credit += invoice['amount_total']
                debit += invoice['amount_total']
                date_invoice = invoice['date_invoice'].split("-")[2]+"/"+invoice['date_invoice'].split("-")[1]+"/"+invoice['date_invoice'].split("-")[0]
                data={
                    'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                    'raison_social':RaisonSocial,
            
                    'date_debut':datedebut,
                    'date_fin':datefin,
                    'date_piece':datetime.strptime(date_invoice, '%d/%m/%Y'),#date_invoice,
                    'libelle':'Facture',
                    'num_piece':invoice['internal_number'],
                    #'debit':0,
                    #'credit':invoice['amount_total'],
                    'debit':invoice['amount_total'],
                    'credit':0,
                    'solde':round (solde_precedant + debit - credit,3),
                    'user':obj_user.name,
                    'date_report_precedent':ReportDatePiece,
                    'libelle_report_precedent':ReportLibellePiece,
                    'num_piece_report_precedent':ReportNumeroPiece,
                    'debit_report_precedent':ReportDebit,
                    'credit_report_precedent':ReportCredit,
                    'solde_precedant':solde_precedant,
                    'invoices':'',
                    } 
                result.append(data)

            #**************************************** montant en espece *********************************
            cr.execute("SELECT * FROM reglement_paiement where partner_id = %s and date_reglement <= %s and date_reglement >= %s and type='out' and state = 'close'",  (fournisseur_id[0],datefin,datedebut,))
            reglements = cr.dictfetchall()
            for reglement in reglements:
                paiement = self.pool.get('reglement.paiement').browse(cr, uid, reglement['id'], context=context)
                invoices =''
                #**************************************** montant en espece *********************************
                if reglement['montant_espece'] > 0:
                    #rim modif :: sttc 18/07/2014
                    for invoice in paiement.reglement_detail:
                        
                        invoices += '[' + invoice.invoice_id.internal_number +']'
                    #end rim modif :: 
                    
                    #debit += reglement['montant_espece']
                    credit += reglement['montant_espece']
                    date_reglement = reglement['date_reglement'].split("-")[2]+"/"+reglement['date_reglement'].split("-")[1]+"/"+reglement['date_reglement'].split("-")[0]
                    data={
                        'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                        'raison_social':RaisonSocial,
                        'date_debut':datedebut,
                        'date_fin':datefin,
                        'date_piece':datetime.strptime(date_reglement, '%d/%m/%Y'),#date_reglement,
                        'libelle':'ESPECE',
                        'num_piece':'',
                        #'debit':round(reglement['montant_espece'],3),
                        #'credit':0,
                        'debit':0,
                        'credit':round(reglement['montant_espece'],3),
                        'solde':round (solde_precedant + debit - credit,3),
                        'user':obj_user.name,
                        'date_report_precedent':ReportDatePiece,
                        'libelle_report_precedent':ReportLibellePiece,
                        'num_piece_report_precedent':ReportNumeroPiece,
                        'debit_report_precedent':ReportDebit,
                        'credit_report_precedent':ReportCredit,
                        'solde_precedant':solde_precedant,
                        'invoices':invoices,
                    } 
                    result.append(data)
                    
            #**************************************** Retenue a la source *********************************
            #cr.execute("SELECT reglement_retenu_source.id ,reglement_retenu_source.name,total_retenu, montant_retenu,date_retenu,retenue_id FROM reglement_retenu_source,retenue_src_line where reglement_retenu_source.id = retenue_src_line.retenu_src_id and  reglement_retenu_source.partner_id = %s and reglement_retenu_source.date_retenu <= %s and reglement_retenu_source.date_retenu >= %s and reglement_retenu_source.type='out' and reglement_retenu_source.recu='True' ",  (fournisseur_id,datefin,datedebut,))
            cr.execute("SELECT reglement_retenu_source.id ,total_retenu, date_retenu, reglement_retenu_source.name FROM reglement_retenu_source where  reglement_retenu_source.partner_id = %s and reglement_retenu_source.date_retenu <= %s and reglement_retenu_source.date_retenu >= %s and reglement_retenu_source.type_in_out='out'  ",  (fournisseur_id[0],datefin,datedebut,))
            retenues = cr.dictfetchall()

            for retenue in retenues: 
                #rim modif :: sttc 18/07/2014
                invoices=''
                liste_retenues=''
                retenue_client_obj = self.pool.get('reglement.retenu.source').browse(cr, uid, retenue['id'], context=context)
                #retenue_source = self.pool.get('reglement.retenu').browse(cr, uid, retenue['retenue_id'], context=context)
                #for invoice in retenue_client_obj.invoice_ids: 
                #    invoices += '[' + invoice.internal_number +']'
                #rim modif :: 24/07/2014 afficher les retenues ensemble::
                #for retenue_src in retenue_client_obj.retenue_src_lines:
                #    liste_retenues += '[' + retenue_src.retenue_id.code +']'
                #end rim modif :: 
                #debit += retenue['montant_retenu']
                #credit += retenue['montant_retenu']
                credit += retenue['total_retenu']
                date_retenu = retenue['date_retenu'].split("-")[2]+"/"+retenue['date_retenu'].split("-")[1]+"/"+retenue['date_retenu'].split("-")[0]
                data={
                    'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                    'raison_social':RaisonSocial,
                    'date_debut':datedebut,
                    'date_fin':datefin,
                    'date_piece':datetime.strptime(date_retenu, '%d/%m/%Y'),#date_retenu,
                    #'libelle':retenue_source.code,
                    'libelle':liste_retenues,
                    'num_piece':retenue['name'],
                    #'debit':round(retenue['montant_retenu'],3),
                    #'credit':0,
                    'debit':0,
                    #'credit':round(retenue['montant_retenu'],3),
                    'credit':round(retenue['total_retenu'],3),
                    'solde':round (solde_precedant + debit - credit,3),
                    'user':obj_user.name,
                    'date_report_precedent':ReportDatePiece,
                    'libelle_report_precedent':ReportLibellePiece,
                    'num_piece_report_precedent':ReportNumeroPiece,
                    'debit_report_precedent':ReportDebit,
                    'credit_report_precedent':ReportCredit,
                    'solde_precedant':solde_precedant,
                    #'invoices':invoices,
                    } 
                result.append(data)
                
            #**************************************** Facture Avoir Client  *********************************
            cr.execute("select * FROM account_invoice where type='out_refund' and partner_id = %s and date_invoice >= %s and date_invoice <= %s  ",  (fournisseur_id[0],datedebut,datefin,))
            invoices = cr.dictfetchall()
            for invoice in invoices:  
              
                #rim modif :: sttc :: 18/07/2014 ::
                invoices=''
                cr.execute("select * FROM reglement_detail_avoir where avoir_id=%s",(invoice['id'],))
                avoir_details = cr.dictfetchall()
               
                if len(avoir_details) > 0:
                    avoir_obj = self.pool.get('reglement.detail.avoir').browse(cr, uid,avoir_details[0]['id'], context=context)
                    reglement_obj = self.pool.get('reglement.paiement').browse(cr, uid,avoir_obj.reglement_id.id, context=context)
                    for detail in reglement_obj.reglement_detail: 
                        invoices += '[' + detail.invoice_id.internal_number +']'
              
                #debit += invoice['amount_total'] 
                credit += invoice['amount_total'] 
                date_invoice = invoice['date_invoice'].split("-")[2]+"/"+invoice['date_invoice'].split("-")[1]+"/"+invoice['date_invoice'].split("-")[0]
                data={
                    'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                    'raison_social':RaisonSocial,
              
                    'date_debut':datedebut,
                    'date_fin':datefin,
                    'date_piece':datetime.strptime(date_invoice, '%d/%m/%Y'),#date_invoice,
                    'libelle':'AVOIR',
                    'num_piece':invoice['internal_number'],
                    #'debit':round(invoice['amount_total'],3) ,
                    #'credit':0,
                    'debit':0,
                    'credit':round(invoice['amount_total'],3) ,
                    'solde':round (solde_precedant + debit - credit,3),
                    'user':obj_user.name,
                    'date_report_precedent':ReportDatePiece,
                    'libelle_report_precedent':ReportLibellePiece,
                    'num_piece_report_precedent':ReportNumeroPiece,
                    'debit_report_precedent':ReportDebit,
                    'credit_report_precedent':ReportCredit,
                    'solde_precedant':solde_precedant,
                    'invoices':invoices,
                    } 
                result.append(data) 
                
            #**************************************** PIECE PAIEMENT : CHQ et TRT ************************************
            print 'hi!!!!!!!!!!!'
            cr.execute("select reglement_piece.id as p_id,montant_piece,date_encaissement,date_echance,mode_reglement,num_cheque_traite,montant_piece FROM reglement_piece,reglement_mode where reglement_piece.mode_reglement = reglement_mode.id and reglement_piece.partner_id = %s and reglement_piece.type='out' and reglement_piece.date_encaissement >= %s and reglement_piece.date_encaissement <= %s and reglement_piece.state='cashed' and (reglement_mode.code ='CHQ' or  reglement_mode.code ='TRT')",  (fournisseur_id[0],datedebut,datefin,))
            pieces = cr.dictfetchall()
            for piece in pieces:   
                #rim modif :: sttc :: 18/07/2014 ::
                invoices=''
                cr.execute("select * FROM reglement_detail_piece where piece_id=%s",(piece['p_id'],))
                piece_details = cr.dictfetchall()
              
                if len(piece_details) > 0:
                    piece_obj = self.pool.get('reglement.detail.piece').browse(cr, uid, piece_details[0]['id'], context=context)
                    reglement_obj = self.pool.get('reglement.paiement').browse(cr, uid,piece_obj.reglement_id.id, context=context)
                    for detail in reglement_obj.reglement_detail: 
                        invoices += '[' + detail.invoice_id.internal_number +']'
               
                type_piece = ""
                #piece_paiement = self.pool.get('reglement.paiement').browse(cr, uid, piece['id'], context=context)
              
                #debit += piece['montant_piece']
                credit += piece['montant_piece']
                mode_paiement = self.pool.get('reglement.mode').browse(cr, uid, piece['mode_reglement'], context=context)
                type_piece = mode_paiement.designation
                
                #date_piece = piece['date_encaissement'].split("-")[2]+"/"+piece['date_encaissement'].split("-")[1]+"/"+piece['date_encaissement'].split("-")[0]
                date_piece = piece['date_encaissement']
                data={
                    'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                    'raison_social':RaisonSocial,
                    'date_debut':datedebut,
                    'date_fin':datefin,
                    'date_piece':datetime.strptime(date_piece, '%d/%m/%Y'),#date_piece,
                    'libelle':'PIECE PAIEMENT:'+type_piece,
                    'num_piece':piece['num_cheque_traite'],
                    #'debit':round(piece['montant_piece'],3),
                    #'credit':0,      
                    'debit':0,
                    'credit':round(piece['montant_piece'],3),
                    'solde':round (solde_precedant + debit - credit,3),
                    'user':obj_user.name,
                    'date_report_precedent':ReportDatePiece,
                    'libelle_report_precedent':ReportLibellePiece,
                    'num_piece_report_precedent':ReportNumeroPiece,
                    'debit_report_precedent':ReportDebit,
                    'credit_report_precedent':ReportCredit,
                    'solde_precedant':solde_precedant,
                    'invoices':invoices,
                    } 
                result.append(data)
               
            #**************************************** PIECE PAIEMENT : ESP VIR ************************************
            #date_obj_fin = datetime.strptime(datefin,'%d/%m/%Y')
            date_obj_fin = datefin
            #date_obj_debut = datetime.strptime(datedebut,'%d/%m/%Y')
            date_obj_debut = datedebut
            cr.execute("select reglement_piece.id as p_id,mode_reglement,montant_piece,num_cheque_traite,reglement_piece.date_echance as date_echance,reglement_piece.date_encaissement as date_piece  FROM reglement_piece,reglement_mode where reglement_piece.mode_reglement = reglement_mode.id and reglement_piece.partner_id = %s and reglement_piece.type='out' and reglement_piece.date_encaissement >= %s and reglement_piece.date_encaissement <= %s and (reglement_mode.code ='ESP' or  reglement_mode.code ='VIR')",  (fournisseur_id[0],date_obj_debut,date_obj_fin,))
            pieces = cr.dictfetchall()
            for piece in pieces:   
                #rim modif :: sttc :: 18/07/2014 ::
                invoices=''
                cr.execute("select * FROM reglement_detail_piece where piece_id=%s",(piece['p_id'],))
                piece_details = cr.dictfetchall()
              
                if len(piece_details) > 0:
                    piece_obj = self.pool.get('reglement.detail.piece').browse(cr, uid,piece_details[0]['id'], context=context)
                    reglement_obj = self.pool.get('reglement.paiement').browse(cr, uid,piece_obj.reglement_id.id, context=context)
                    for detail in reglement_obj.reglement_detail: 
                        invoices += '[' + detail.invoice_id.internal_number +']'
     
                type_piece = ""
                #piece_paiement = self.pool.get('reglement.paiement').browse(cr, uid, piece['id'], context=context)
              
                #debit += piece['montant_piece']
                credit += piece['montant_piece']
                mode_paiement = self.pool.get('reglement.mode').browse(cr, uid, piece['mode_reglement'], context=context)
                type_piece = mode_paiement.designation
                
                jour = (piece['date_piece'].split("-")[2]).split(" ")[0]
                date_piece = jour+"/"+piece['date_piece'].split("-")[1]+"/"+piece['date_piece'].split("-")[0]
                
                data={
                    'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                    'raison_social':RaisonSocial,
                    'date_debut':datedebut,
                    'date_fin':datefin,
                    'date_piece':datetime.strptime(date_piece, '%d/%m/%Y'),#date_piece,
                    'libelle':'PIECE PAIEMENT:'+type_piece,
                    'num_piece':piece['num_cheque_traite'],
                    #'debit':round(piece['montant_piece'],3),
                    #'credit':0,
                    'debit':0,
                    'credit':round(piece['montant_piece'],3),
                    'solde':round (solde_precedant + debit - credit,3),
                    'user':obj_user.name,
                    'date_report_precedent':ReportDatePiece,
                    'libelle_report_precedent':ReportLibellePiece,
                    'num_piece_report_precedent':ReportNumeroPiece,
                    'debit_report_precedent':ReportDebit,
                    'credit_report_precedent':ReportCredit,
                    'solde_precedant':solde_precedant,
                    'invoices':invoices,
                    } 
                result.append(data)

        #**************************************** AVANCE ************************************
          
            cr.execute("select *  FROM reglement_avance where reglement_avance.partner_id = %s and reglement_avance.type='client' and reglement_avance.date_avance >= %s and reglement_avance.date_avance <= %s ",  (fournisseur_id[0],datedebut,datefin,))
            pieces = cr.dictfetchall()
            for piece in pieces:   
                #rim modif :: sttc :: 18/07/2014 ::
                invoices=''
                cr.execute("select * FROM reglement_detail_avance where avance_id=%s",(piece['id'],))
                avance_details = cr.dictfetchall()
             
                if len(avance_details) > 0:
                    detail_avance_obj = self.pool.get('reglement.detail.avance').browse(cr, uid, avance_details[0]['id'], context=context)
                    reglement_obj = self.pool.get('reglement.paiement').browse(cr, uid,detail_avance_obj.reglement_id.id, context=context)
                    for detail in reglement_obj.reglement_detail: 
                        invoices += '[' + detail.invoice_id.internal_number +']'
               
                type_piece = ""
                #piece_paiement = self.pool.get('reglement.paiement').browse(cr, uid, piece['id'], context=context)
              
                #debit += piece['montant_avance']
                credit += piece['montant_avance']
                date_piece = piece['date_avance'].split("-")[2]+"/"+piece['date_avance'].split("-")[1]+"/"+piece['date_avance'].split("-")[0]
               
                data={
                    'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                    'raison_social':RaisonSocial,
                    'date_debut':datedebut,
                    'date_fin':datefin,
                    'date_piece':datetime.strptime(date_piece, '%d/%m/%Y'),#date_piece,
                    'libelle':'AVANCE',
                    'num_piece':'',
                    #'debit':round(piece['montant_avance'],3),
                    #'credit':0,
                    'debit':0,
                    'credit':round(piece['montant_avance'],3),
                    'solde':round (solde_precedant + debit - credit,3),
                    'user':obj_user.name,
                    'date_report_precedent':ReportDatePiece,
                    'libelle_report_precedent':ReportLibellePiece,
                    'num_piece_report_precedent':ReportNumeroPiece,
                    'debit_report_precedent':ReportDebit,
                    'credit_report_precedent':ReportCredit,
                    'solde_precedant':solde_precedant,
                    'invoices':invoices,
                    } 
                result.append(data)

            #rim modif :26/09/2014: sttc :: ajouter penalite de retard
            #**************************************** PENALITE ************************************
          
            #cr.execute("SELECT * FROM reglement_paiement where partner_id = %s and date_reglement <= %s and date_reglement >= %s and type='out' and state = 'close'",  (fournisseur_id[0],datefin,datedebut,))
            #reglements = cr.dictfetchall()
            #for reglement in reglements:
            #    paiement = self.pool.get('reglement.paiement').browse(cr, uid, reglement['id'], context=context)
            #    invoices =''
            #    #**************************************** montant penalite *********************************
            #    if reglement['montant_penalite'] > 0:
                    #rim modif :: sttc 18/07/2014
            #        for invoice in paiement.reglement_detail:
                        
            #            invoices += '[' + invoice.invoice_id.internal_number +']'
                    #end rim modif :: 
                    
                    #debit += reglement['montant_espece']
            #        credit += reglement['montant_penalite']
            #        date_reglement = reglement['date_reglement'].split("-")[2]+"/"+reglement['date_reglement'].split("-")[1]+"/"+reglement['date_reglement'].split("-")[0]
            #        data={
            #            'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
            #            'raison_social':RaisonSocial,
            #            'date_debut':datedebut,
            #            'date_fin':datefin,
            #            'date_piece':datetime.strptime(date_reglement, '%d/%m/%Y'),#date_reglement,
            #            'libelle':'PENALITE',
            #            'num_piece':'',
                        #'debit':round(reglement['montant_espece'],3),
                        #'credit':0,
            #            'debit':0,
            #            'credit':round(reglement['montant_penalite'],3),
            #            'solde':round (solde_precedant + debit - credit,3),
            #            'user':obj_user.name,
            #            'date_report_precedent':ReportDatePiece,
            #            'libelle_report_precedent':ReportLibellePiece,
            #            'num_piece_report_precedent':ReportNumeroPiece,
            #            'debit_report_precedent':ReportDebit,
            #            'credit_report_precedent':ReportCredit,
            #            'solde_precedant':solde_precedant,
            #            'invoices':invoices,
            #        } 
            #        result.append(data)
        
        result = sorted(result, key=lambda k: k['date_piece'])  
        
        i = 0
        debit = 0
        credit = 0
        for element in result:
            debit += round(element['debit'],3)
            credit += round(element['credit'],3)
            element['solde'] = round (solde_precedant + debit - credit,3)
            i += 1
        return result
jasper_report.report_jasper('report.jasper_rapport_releve_client_print', 'reglement.piece', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
