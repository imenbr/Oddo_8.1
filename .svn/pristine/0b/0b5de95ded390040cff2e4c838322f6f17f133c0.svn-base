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
                                                                                                            
            cr.execute("SELECT parametre1,parametre2 FROM res_company WHERE id = 1")                 
            obj_company = cr.dictfetchone()
            header1 = obj_company['parametre1']
            header2 = obj_company['parametre2'] 
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

            
            ReportDatePiece = datedebut
            
            fournisseur_id = data['form']['fournisseur_id']
            
            cr.execute(" Select * from res_partner where id = %s ", (fournisseur_id,))
            Fournisseur=cr.dictfetchone()
            RaisonSocial = Fournisseur['name']
            MatriculeFiscale = Fournisseur['mf']
            #first line
            #**************************************** montant en espece precedant *********************************
            cr.execute("SELECT * FROM reglement_paiement where partner_id = %s and date_reglement <= %s and state = 'close' and type='in' ",  (fournisseur_id,datedebut,))
            reglements = cr.dictfetchall()
            for reglement in reglements:                
                if reglement['montant_espece'] > 0:
                    ReportCredit += reglement['montant_espece']
            #**************************************** Retenue a la source precedant *********************************
            cr.execute("SELECT * FROM reglement_retenu_source where partner_id = %s and date_retenu <= %s and state = 'close' ",  (fournisseur_id,datedebut,))
            retenues = cr.dictfetchall()
            for retenue in retenues: 
                ReportCredit += retenue['total_retenu']
            #**************************************** Facture Fournisseur precedant *********************************
            cr.execute("select * FROM account_invoice where  state!='draft' and state!='cancel' and type='in_invoice' and partner_id = %s and date_invoice <= %s  ",  (fournisseur_id,datedebut,))
            invoices = cr.dictfetchall()
            for invoice in invoices:   
                ReportDebit += invoice['amount_total']
            #**************************************** Facture Avoir Fournisseur precedant *********************************
            cr.execute("select * FROM account_invoice where  state!='draft' and state!='cancel' and  type='in_refund' and partner_id = %s and date_invoice <= %s  ",  (fournisseur_id,datedebut,))
            invoices = cr.dictfetchall()
            for invoice in invoices:  
                ReportDebit += invoice['amount_total'] * (-1) 
            #**************************************** PIECE PAIEMENT precedant ************************************
            cr.execute("select * FROM reglement_piece where partner_id = %s and create_date <= %s  ",  (fournisseur_id,datedebut,))
            pieces = cr.dictfetchall()
            for piece in pieces:  
                ReportCredit += piece['montant_piece']

            #data={
            #        'header1':header1,
            #        'header2':header2,
            #        'raison_social':RaisonSocial,
            #        'matricule_fiscale':MatriculeFiscale,
                    #'date_debut':datedebut,
                    #'date_fin':datefin,
                    #'date_piece':'',
                    #'libelle':'',
                    #'num_piece':'',
                    #'debit':0,
                    #'credit':0,
            #        'user':obj_user.name,
            #        'date_report_precedent':ReportDatePiece,
            #        'libelle_report_precedent':ReportLibellePiece,
            #        'num_piece_report_precedent':ReportNumeroPiece,
            #        'debit_report_precedent':ReportDebit,
            #        'credit_report_precedent':ReportCredit,
            #    } 
            #result.append(data)
            #**************************************** Total precedant ************************************            
            solde_precedant = round (ReportDebit - ReportCredit,3)
            #**************************************** montant en espece *********************************
            cr.execute("SELECT * FROM reglement_paiement where partner_id = %s and date_reglement <= %s and date_reglement >= %s and state = 'close' and type='in' ",  (fournisseur_id,datefin,datedebut,))
            reglements = cr.dictfetchall()
            for reglement in reglements:
                paiement = self.pool.get('reglement.paiement').browse(cr, uid, reglement['id'], context=context)
                #**************************************** montant en espece *********************************
                if reglement['montant_espece'] > 0:
                    credit += reglement['montant_espece']
                    date_reglement = reglement['date_reglement'].split("-")[2]+"/"+reglement['date_reglement'].split("-")[1]+"/"+reglement['date_reglement'].split("-")[0]
                    data={
                    'header1':header1,
                    'header2':header2,
                    'raison_social':RaisonSocial,
                    'matricule_fiscale':MatriculeFiscale,
                    'date_debut':datedebut,
                    'date_fin':datefin,
                    'date_piece':date_reglement,
                    'libelle':'ESPECE',
                    'num_piece':'',
                    'debit':0,
                    'credit':reglement['montant_espece'],
                    'solde':round (debit - credit,3),
                    'user':obj_user.name,
                    'date_report_precedent':ReportDatePiece,
                    'libelle_report_precedent':ReportLibellePiece,
                    'num_piece_report_precedent':ReportNumeroPiece,
                    'debit_report_precedent':ReportDebit,
                    'credit_report_precedent':ReportCredit,
                    'solde_precedant':solde_precedant,
                    } 
                    result.append(data)
                
            #**************************************** Retenue a la source *********************************
            cr.execute("SELECT * FROM reglement_retenu_source where partner_id = %s and date_retenu <= %s and date_retenu >= %s and state = 'close' ",  (fournisseur_id,datefin,datedebut,))
            retenues = cr.dictfetchall()
            for retenue in retenues: 
                retenue_source = self.pool.get('reglement.retenu.source').browse(cr, uid, retenue['id'], context=context)
                credit += retenue['total_retenu']
                date_retenu = retenue['date_retenu'].split("-")[2]+"/"+retenue['date_retenu'].split("-")[1]+"/"+retenue['date_retenu'].split("-")[0]
                data={
                    'header1':header1,
                    'header2':header2,
                    'raison_social':RaisonSocial,
                    'matricule_fiscale':MatriculeFiscale,
                    'date_debut':datedebut,
                    'date_fin':datefin,
                    'date_piece':date_retenu,
                    'libelle':retenue_source.retenu_id.code,
                    'num_piece':'',
                    'debit':0,
                    'credit':retenue['total_retenu'],
                    'solde':round (debit - credit,3),
                    'user':obj_user.name,
                    'date_report_precedent':ReportDatePiece,
                    'libelle_report_precedent':ReportLibellePiece,
                    'num_piece_report_precedent':ReportNumeroPiece,
                    'debit_report_precedent':ReportDebit,
                    'credit_report_precedent':ReportCredit,
                    'solde_precedant':solde_precedant,
                    } 
                result.append(data) 
            #**************************************** Facture Fournisseur  *********************************
            cr.execute("select * FROM account_invoice where  state!='draft' and state!='cancel' and type='in_invoice' and partner_id = %s and date_invoice >= %s and date_invoice <= %s  ",  (fournisseur_id,datedebut,datefin,))
            invoices = cr.dictfetchall()
            for invoice in invoices:   
                debit += invoice['amount_total']
                date_invoice = invoice['date_invoice'].split("-")[2]+"/"+invoice['date_invoice'].split("-")[1]+"/"+invoice['date_invoice'].split("-")[0]
                data={
                    'header1':header1,
                    'header2':header2,
                    'raison_social':RaisonSocial,
                    'matricule_fiscale':MatriculeFiscale,
                    'date_debut':datedebut,
                    'date_fin':datefin,
                    'date_piece':date_invoice,
                    'libelle':'Facture',
                    'num_piece':invoice['number'],
                    'debit':invoice['amount_total'],
                    'credit':0,
                    'solde':round (debit - credit,3),
                    'user':obj_user.name,
                    'date_report_precedent':ReportDatePiece,
                    'libelle_report_precedent':ReportLibellePiece,
                    'num_piece_report_precedent':ReportNumeroPiece,
                    'debit_report_precedent':ReportDebit,
                    'credit_report_precedent':ReportCredit,
                    'solde_precedant':solde_precedant,
                    } 
                result.append(data)
            #**************************************** Facture Avoir Fournisseur  *********************************
            cr.execute("select * FROM account_invoice where  state!='draft' and state!='cancel' and  type='in_refund' and partner_id = %s and date_invoice >= %s and date_invoice <= %s  ",  (fournisseur_id,datedebut,datefin,))
            invoices = cr.dictfetchall()
            for invoice in invoices:  
                debit += invoice['amount_total'] * (-1) 
                date_invoice = invoice['date_invoice'].split("-")[2]+"/"+invoice['date_invoice'].split("-")[1]+"/"+invoice['date_invoice'].split("-")[0]
                data={
                    'header1':header1,
                    'header2':header2,
                    'raison_social':RaisonSocial,
                    'matricule_fiscale':MatriculeFiscale,
                    'date_debut':datedebut,
                    'date_fin':datefin,
                    'date_piece':date_invoice,
                    'libelle':'AVOIR',
                    'num_piece':invoice['number'],
                    'debit':invoice['amount_total'] * (-1),
                    'credit':0,
                    'solde':round (debit - credit,3),
                    'user':obj_user.name,
                    'date_report_precedent':ReportDatePiece,
                    'libelle_report_precedent':ReportLibellePiece,
                    'num_piece_report_precedent':ReportNumeroPiece,
                    'debit_report_precedent':ReportDebit,
                    'credit_report_precedent':ReportCredit,
                    'solde_precedant':solde_precedant,
                    } 
                result.append(data) 
            #**************************************** PIECE PAIEMENT ************************************
            cr.execute("select * FROM reglement_piece where partner_id = %s and create_date >= %s and create_date <= %s  ",  (fournisseur_id,datedebut,datefin,))
            pieces = cr.dictfetchall()
            for piece in pieces:   
                type_piece = ""
                piece_paiement = self.pool.get('reglement.paiement').browse(cr, uid, piece['id'], context=context)
                #if piece_paiement.mode_reglement:
                #    print 'piece_paiement.mode_reglement',piece_paiement.mode_reglement
                credit += piece['montant_piece']
                mode_paiement = self.pool.get('reglement.mode').browse(cr, uid, piece['mode_reglement'], context=context)
                type_piece = mode_paiement.designation
                jour = (piece['create_date'].split("-")[2]).split(" ")[0]
                date_piece = jour+"/"+piece['create_date'].split("-")[1]+"/"+piece['create_date'].split("-")[0]
                data={
                    'header1':header1,
                    'header2':header2,
                    'raison_social':RaisonSocial,
                    'matricule_fiscale':MatriculeFiscale,
                    'date_debut':datedebut,
                    'date_fin':datefin,
                    'date_piece':date_piece,
                    'libelle':'PIECE PAIEMENT:'+type_piece,
                    'num_piece':piece['num_cheque_traite'],
                    'debit':0,
                    'credit':piece['montant_piece'],
                    'solde':round (debit - credit,3),
                    'user':obj_user.name,
                    'date_report_precedent':ReportDatePiece,
                    'libelle_report_precedent':ReportLibellePiece,
                    'num_piece_report_precedent':ReportNumeroPiece,
                    'debit_report_precedent':ReportDebit,
                    'credit_report_precedent':ReportCredit,
                    'solde_precedant':solde_precedant,
                    } 
                result.append(data)   
        return result
jasper_report.report_jasper('report.jasper_rapport_grand_livre_print', 'reglement.piece', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
