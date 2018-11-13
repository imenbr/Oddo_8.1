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
        ReportCredit=0.000
        ReportCreditNull=0.000
        ReportDebit=0.000
        ReportDebitNull=0.000
        ReportDatePiece=''
        ReportLibellePiece='REPORT DE LA PERIODE PRECEDANTE'
        ReportNumeroPiece=''
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
            #Report de la période précendente
            #**********************************bon Livraison Achat*************************
            #cr.execute("select sum(amount_total) as amount_total FROM stock_picking where invoice_state = '2binvoiced' and state = 'done' and type = 'in' and partner_id = %s  and date_done < %s ", (fournisseur_id,datedebut,))
            #BlAchat = cr.dictfetchone()
            #print 'BlAchat!!!!!!!',BlAchat
            #Test = BlAchat['amount_total']
            #if str(Test) == 'None':
            #   ReportCreditNull = 0.000
            #   ReportCredit = ReportCredit + ReportCreditNull
            #   print ' Non Enter ReportCredit!!!!!!!',ReportCredit

            #else :
            #      ReportCredit = ReportCredit + BlAchat['amount_total']
            #      print 'ReportCredit else!!!!!!!',ReportCredit
            #**********************************End bon Livraison Achat*************************
            #**********************************Facture Achat*************************
            cr.execute("select sum(amount_total) as amount_total FROM account_invoice where  state='open' and type='in_invoice' and partner_id = %s  and date_invoice < %s", (fournisseur_id,datedebut,))
            FactureAchat = cr.dictfetchone()
            print 'FactureAchat!!!!!!!',FactureAchat
            Test = FactureAchat['amount_total']
            if str(Test) == 'None':
               ReportCreditNull = 0.000
               ReportCredit = ReportCredit + ReportCreditNull
               print 'Non Enter ReportCredit!!!!!!!',ReportCredit
            else :
                  ReportCredit = ReportCredit + FactureAchat['amount_total']
                  print 'ReportCredit else!!!!!!!',ReportCredit
            #**********************************End Facture Achat*************************
            #**********************************Avoir Facture Achat*************************
            cr.execute("select sum(amount_total) as amount_total FROM account_invoice where  type='in_refund' and partner_id = %s  and date_invoice < %s ",  (fournisseur_id,datedebut,))
            AvoireFactureAchat = cr.dictfetchone()
            print 'AvoireFactureAchat!!!!!!!',AvoireFactureAchat
            Test = AvoireFactureAchat['amount_total']
            if str(Test) == 'None':
               ReportDebitNull = 0.000
               ReportDebit = ReportDebit + ReportDebitNull
               print 'Non Enter Debit!!!!!!!'
            else :
                  ReportDebit = ReportDebit + AvoireFactureAchat['amount_total']
                  print 'ReportDebit else!!!!!!!',ReportDebit
            #**********************************End Avoir Facture Achat*************************
            #**********************************Avance Fournisseur*************************
            cr.execute("select sum(montant_avance) as montant_avance FROM reglement_avance where  state !='draft'  and  partner_id = %s  and date_avance < %s",  (fournisseur_id,datedebut,))
            AvanceFournisseur = cr.dictfetchone()
            print 'AvanceFournisseur!!!!!!!',AvanceFournisseur
            Test = AvanceFournisseur['montant_avance']
            if str(Test) == 'None':
               ReportDebitNull = 0.000
               ReportDebit = ReportDebit + ReportDebitNull
               print 'Non Enter Debit!!!!!!!'
            else :
                   ReportDebit = ReportDebit + AvanceFournisseur['montant_avance']
                   print 'ReportDebit else!!!!!!!',ReportDebit
                   
            #**********************************End Avance Fournisseur*************************
            #**********************************Reglement Fournisseur *************************
            #**********************************Reglement Fournisseur Debiteur**************************
            cr.execute("SELECT sum(total_retenu) as total_retenu from reglement_retenu_source where state='close'  and partner_id = %s and date_retenu < %s ",  (fournisseur_id,datedebut,))
            ReglementTotalRetenue = cr.dictfetchone()
            print 'ReglementTotalRetenue!!!!!!!',ReglementTotalRetenue
            Test = ReglementTotalRetenue['total_retenu']
            if str(Test) == 'None':
               ReportDebitNull = 0.000
               ReportDebit = ReportDebit + ReportDebitNull
               print 'Non Enter Debit!!!!!!!'
            else :
                   ReportDebit = ReportDebit + ReglementTotalRetenue['total_retenu']
                   print 'ReportDebit else!!!!!!!',ReportDebit
            cr.execute("SELECT sum(total_ttc - total_reste_a_payer) as total_recu from reglement_retenu_source where state ='close' and partner_id = %s and date_retenu < %s ",  (fournisseur_id,datedebut,))
            ReglementTotalRecue = cr.dictfetchone()
            print 'ReglementTotalRecue!!!!!!!',ReglementTotalRecue
            Test = ReglementTotalRecue['total_recu']
            if str(Test) == 'None':
               ReportDebitNull = 0.000
               ReportDebit = ReportDebit + ReportDebitNull
               print 'Non Enter Debit!!!!!!!'
            else :
                  ReportDebit = ReportDebit + ReglementTotalRecue['total_recu']
                  print 'ReportDebit else!!!!!!!',ReportDebit
            cr.execute("SELECT sum(rd.montant_rest) as montantrestant FROM reglement_detail rd left outer join reglement_paiement rp on rd.reglement_id = rp.id where rp.state ='close' and rp.partner_id = %s  and rp.date_reglement < %s ",  (fournisseur_id,datedebut,))
            ReglementMontantRestant = cr.dictfetchone()
            print 'ReglementMontantRestant!!!!!!!',ReglementMontantRestant
            Test = ReglementMontantRestant['montantrestant']
            if str(Test) == 'None':
               ReportDebitNull = 0.000
               ReportDebit = ReportDebit + ReportDebitNull
               print 'Non Enter Debit!!!!!!!'
            else :
                  ReportDebit = ReportDebit + ReglementMontantRestant['montantrestant']
                  print 'ReportDebit else!!!!!!!',ReportDebit
            #**********************************End Reglement Fournisseur Debiteur**************************
            #**********************************Reglement Fournisseur Crediteur**************************
            cr.execute("SELECT sum(total_retenu) as totalretenu from reglement_retenu_source rrs left join account_invoice aci on rrs.invoice_id= aci.id where aci.type='out_invoice' and aci.state='open' and rrs.state='close' and rrs.partner_id = %s and rrs.date_retenu < %s",  (fournisseur_id,datedebut,))
            ReglementTotalRetenue = cr.dictfetchone()
            print 'ReglementTotalRetenue!!!!!!!',ReglementTotalRetenue
            Test = ReglementTotalRetenue['totalretenu']
            if str(Test) == 'None':
               ReportCreditNull = 0.000
               ReportCredit = ReportCredit + ReportCreditNull
               print 'Non Enter ReportCredit!!!!!!!',ReportCredit
            else :
                   ReportCredit = ReportCredit + ReglementTotalRetenue['total_retenu']
                   print 'ReportCredit else!!!!!!!',ReportCredit
            cr.execute("SELECT sum(rda.ttc - rda.montant_rest) as total_recu FROM reglement_detail_avoir rda left join reglement_paiement rp on rda.reglement_id = rp.id  where rp.state ='close'  and rp.partner_id = %s  and rp.date_reglement < %s",  (fournisseur_id,datedebut,))
            ReglementTotalRecue = cr.dictfetchone()
            print 'ReglementTotalRecue!!!!!!!',ReglementTotalRecue
            Test = ReglementTotalRecue['total_recu']
            if str(Test) == 'None':
               ReportCreditNull = 0.000
               ReportCredit = ReportCredit + ReportCreditNull
               print 'Non Enter ReportCredit!!!!!!!',ReportCredit
            else :
                  ReportCredit = ReportCredit + ReglementTotalRecue['total_recu']
                  print 'ReportCredit else!!!!!!!',ReportCredit
            cr.execute("SELECT sum(rda.montant_rest) as montantrestant FROM reglement_detail_avoir rda left join reglement_paiement rp on rda.reglement_id = rp.id  where rp.state ='close'  and rp.partner_id = %s  and rp.date_reglement < %s",  (fournisseur_id,datedebut,))
            ReglementMontantRestant = cr.dictfetchone()
            print 'ReglementMontantRestant!!!!!!!',ReglementMontantRestant
            Test = ReglementMontantRestant['montantrestant']
            if str(Test) == 'None':
               ReportCreditNull = 0.000
               ReportCredit = ReportCredit + ReportCreditNull
               print 'Non Enter ReportCredit!!!!!!!',ReportCredit
            else :
                  ReportCredit = ReportCredit + ReglementMontantRestant['montantrestant']
                  print 'ReportCredit else!!!!!!!',ReportCredit
            #**********************************End Reglement Fournisseur Crediteur**************************
            #**********************************Impayee Fournisseur Crediteur****************************************
            cr.execute("SELECT sum(rdi.montant) as montantrecu FROM reglement_detail_impaye rdi left outer join reglement_paiement rp on rdi.reglement_id = rp.id  left outer join reglement_piece regpiece on rdi.piece_id = regpiece.id  where rp.state='close' and rp.partner_id = %s and rp.date_reglement < %s",  (fournisseur_id,datedebut,))
            ImpyeeFournisseur = cr.dictfetchone()
            print 'ImpyeeFournisseur!!!!!!!',ImpyeeFournisseur
            Test = ImpyeeFournisseur['montantrecu']
            if str(Test) == 'None':
               ReportCreditNull = 0.000
               ReportCredit = ReportCredit + ReportCreditNull
               print 'Non Enter ReportCredit!!!!!!!',ReportCredit
            else :
                   ReportCredit = ReportCredit + ImpyeeFournisseur['montantrecu']
                   print 'ReportCredit else!!!!!!!',ReportCredit
            #**********************************EndImpayee Fournisseur Crediteur****************************************
            #**********************************End Reglement Fournisseur*************************
            #End Report de la période précendente 
            #Region Bon Livraison Achat 
            cr.execute("select date_done as datepiece,'Bon Livraison Achat' as libelle,name as numeropiece,0 as debit,amount_total as credit FROM stock_picking where invoice_state ='2binvoiced' and state ='done' and type ='in' and partner_id = %s and date_done >= %s and date_done <= %s ", (fournisseur_id,datedebut,datefin,))
            ListeBonLivraisonAchat = cr.dictfetchall()
            print 'ListeBonLivraisonAchat!!!!!!',ListeBonLivraisonAchat
            if str(ListeBonLivraisonAchat) !='None':
               if len(ListeBonLivraisonAchat) > 0:
                  for BonLivraisonAchat in ListeBonLivraisonAchat:
                      datetpiece0 = BonLivraisonAchat['datepiece'].split("-")[0]
                      datetpiece1 = BonLivraisonAchat['datepiece'].split("-")[1]
                      datetpiece2 = BonLivraisonAchat['datepiece'].split("-")[2]
                      datetpiece3 = datetpiece2.split(" ")[0]
                      datetpiece = datetpiece3 +"/"+ datetpiece1 +"/"+ datetpiece0
                      libellepiece= BonLivraisonAchat['libelle']
                      numeropiece= BonLivraisonAchat['numeropiece']
                      debit= BonLivraisonAchat['debit']
                      credit= BonLivraisonAchat['credit']
                      data={
                      'header1':header1,
                      'header2':header2,
                      'raison_social':RaisonSocial,
                      'matricule_fiscale':MatriculeFiscale,
                      'date_debut':datedebut,
                      'date_fin':datefin,
                      'date_piece':datetpiece,
                      'libelle':libellepiece,
                      'num_piece':numeropiece,
                      'debit':debit,
                      'credit':credit,
                      'user':obj_user.name,
                      'date_report_precedent':ReportDatePiece,
                      'libelle_report_precedent':ReportLibellePiece,
                      'num_piece_report_precedent':ReportNumeroPiece,
                      'debit_report_precedent':ReportDebit,
                      'credit_report_precedent':ReportCredit,  
                      } 
                      result.append(data)
                      result2.append(data)
            #End Region Bon Livraison Achat
            #Region Facture Achat Non Reglée
            cr.execute("select date_invoice as datepiece,'Facture Achat' as libelle,number as numeropiece,0 as debit,amount_total as credit,partner_id FROM account_invoice where  state='open' and type='in_invoice' and partner_id = %s and date_invoice >= %s and date_invoice <= %s ",(fournisseur_id,datedebut,datefin,))
            ListeFactureAchat = cr.dictfetchall()
            print 'ListeFactureAchat!!!!!!',ListeFactureAchat
            if str(ListeFactureAchat) !='None':
               if len(ListeFactureAchat) > 0:
                  for FactureAchat in ListeFactureAchat:
                      datetpiece0 = FactureAchat['datepiece'].split("-")[0]
                      datetpiece1 = FactureAchat['datepiece'].split("-")[1]
                      datetpiece2 = FactureAchat['datepiece'].split("-")[2]
                      datetpiece3 = datetpiece2.split(" ")[0]
                      datetpiece = datetpiece3 +"/"+ datetpiece1 +"/"+ datetpiece0
                      libellepiece= FactureAchat['libelle']
                      numeropiece= FactureAchat['numeropiece']
                      debit= FactureAchat['debit']
                      credit= FactureAchat['credit']
                      data={
                      'header1':header1,
                      'header2':header2,
                      'raison_social':RaisonSocial,
                      'matricule_fiscale':MatriculeFiscale,
                      'date_debut':datedebut,
                      'date_fin':datefin,
                      'date_piece':datetpiece,
                      'libelle':libellepiece,
                      'num_piece':numeropiece,
                      'debit':debit,
                      'credit':credit,
                      'user':obj_user.name,
                      'date_report_precedent':ReportDatePiece,
                      'libelle_report_precedent':ReportLibellePiece,
                      'num_piece_report_precedent':ReportNumeroPiece,
                      'debit_report_precedent':ReportDebit,
                      'credit_report_precedent':ReportCredit,  
                      } 
                      result.append(data)
                      result2.append(data)
            #End Region Facture Achat Non Reglée
            #Region Avoire Sur Facture none enter*****
            cr.execute("select date_invoice as datepiece,'Avoir Sur Facture' as libelle,number as numeropiece,amount_total as debit,0 as credit FROM account_invoice where  type='in_refund' and partner_id = %s and date_invoice >= %s and date_invoice <= %s ",(fournisseur_id,datedebut,datefin,))
            ListeAvoireFactureAchat = cr.dictfetchall()
            print 'Avoire Sur Facture C Bon!!!!!!!!'
            if str(ListeAvoireFactureAchat) !='None':
               if len(ListeAvoireFactureAchat) > 0:
                  for AvoireFactureAchat in ListeAvoireFactureAchat:
                      datetpiece0 = AvoireFactureAchat['datepiece'].split("-")[0]
                      datetpiece1 = AvoireFactureAchat['datepiece'].split("-")[1]
                      datetpiece2 = AvoireFactureAchat['datepiece'].split("-")[2]
                      datetpiece3 = datetpiece2.split(" ")[0]
                      datetpiece = datetpiece3 +"/"+ datetpiece1 +"/"+ datetpiece0
                      libellepiece= AvoireFactureAchat['libelle']
                      numeropiece= AvoireFactureAchat['numeropiece']
                      debit= AvoireFactureAchat['debit']
                      credit= AvoireFactureAchat['credit']
                      data={
                      'header1':header1,
                      'header2':header2,
                      'raison_social':RaisonSocial,
                      'matricule_fiscale':MatriculeFiscale,
                      'date_debut':datedebut,
                      'date_fin':datefin,
                      'date_piece':datetpiece,
                      'libelle':libellepiece,
                      'num_piece':numeropiece,
                      'debit':debit,
                      'credit':credit,
                      'user':obj_user.name,
                      'date_report_precedent':ReportDatePiece,
                      'libelle_report_precedent':ReportLibellePiece,
                      'num_piece_report_precedent':ReportNumeroPiece,
                      'debit_report_precedent':ReportDebit,
                      'credit_report_precedent':ReportCredit,  
                      } 
                      result.append(data)
                      result2.append(data)
            #End Avoire Sur Facture
            #Region Avance Fournisseur none enter*****
            cr.execute("select date_avance as datepiece,'Avance Fournisseur' as libelle,code_avance as numeropiece,montant_avance as debit,0 as credit,partner_id FROM reglement_avance where  state !='draft'  and  partner_id = %s and date_avance >= %s and date_avance <= %s ",(fournisseur_id,datedebut,datefin,))
            ListeAvanceFournisseur = cr.dictfetchall()
            print 'Avance Fournisseu C Bon!!!!!!!!!!'
            if str(ListeAvanceFournisseur) !='None':
               if len(ListeAvanceFournisseur) > 0:
                  for AvanceFournisseur in ListeAvanceFournisseur:
                      datetpiece0 = AvanceFournisseur['datepiece'].split("-")[0]
                      datetpiece1 = AvanceFournisseur['datepiece'].split("-")[1]
                      datetpiece2 = AvanceFournisseur['datepiece'].split("-")[2]
                      datetpiece3 = datetpiece2.split(" ")[0]
                      datetpiece = datetpiece3 +"/"+ datetpiece1 +"/"+ datetpiece0
                      libellepiece= AvanceFournisseur['libelle']
                      numeropiece= AvanceFournisseur['numeropiece']
                      debit= AvanceFournisseur['debit']
                      credit= AvanceFournisseur['credit']
                      data={
                      'header1':header1,
                      'header2':header2,
                      'raison_social':RaisonSocial,
                      'matricule_fiscale':MatriculeFiscale,
                      'date_debut':datedebut,
                      'date_fin':datefin,
                      'date_piece':datetpiece,
                      'libelle':libellepiece,
                      'num_piece':numeropiece,
                      'debit':debit,
                      'credit':credit,
                      'user':obj_user.name,
                      'date_report_precedent':ReportDatePiece,
                      'libelle_report_precedent':ReportLibellePiece,
                      'num_piece_report_precedent':ReportNumeroPiece,
                      'debit_report_precedent':ReportDebit,
                      'credit_report_precedent':ReportCredit,  
                      } 
                      result.append(data)
                      result2.append(data)
            #End Region Avance Fournisseur
            #Region Reglement Fournisseur
            cr.execute("select date_reglement as datepiece,'Reglement Fournisseur' as libelle,code_reglement as numeropiece,montant_espece as debit,0 as credit,partner_id FROM reglement_paiement where  state ='close' and montant_espece <> 0 and partner_id = %s  and date_reglement >= %s and date_reglement <= %s ",(fournisseur_id,datedebut,datefin,))
            ListeReglementFournisseur = cr.dictfetchall()
            print 'Reglement Fournisseur C Bon!!!!!!!!!!'
            if str(ListeReglementFournisseur) !='None':
               if len(ListeReglementFournisseur) > 0:
                  for ReglementFournisseur in ListeReglementFournisseur:
                      datetpiece0 = ReglementFournisseur['datepiece'].split("-")[0]
                      datetpiece1 = ReglementFournisseur['datepiece'].split("-")[1]
                      datetpiece2 = ReglementFournisseur['datepiece'].split("-")[2]
                      datetpiece3 = datetpiece2.split(" ")[0]
                      datetpiece = datetpiece3 +"/"+ datetpiece1 +"/"+ datetpiece0
                      libellepiece= ReglementFournisseur['libelle']
                      numeropiece= ReglementFournisseur['numeropiece']
                      debit= ReglementFournisseur['debit']
                      credit= ReglementFournisseur['credit']
                      data={
                      'header1':header1,
                      'header2':header2,
                      'raison_social':RaisonSocial,
                      'matricule_fiscale':MatriculeFiscale,
                      'date_debut':datedebut,
                      'date_fin':datefin,
                      'date_piece':datetpiece,
                      'libelle':libellepiece,
                      'num_piece':numeropiece,
                      'debit':debit,
                      'credit':credit,
                      'user':obj_user.name,
                      'date_report_precedent':ReportDatePiece,
                      'libelle_report_precedent':ReportLibellePiece,
                      'num_piece_report_precedent':ReportNumeroPiece,
                      'debit_report_precedent':ReportDebit,
                      'credit_report_precedent':ReportCredit,  
                      } 
                      result.append(data)
                      result2.append(data)
            #End Region Reglement Fournisseur
            #Region Reglement Retenue  enter*****
            cr.execute("select reglement_retenu_source.date_retenu as datepiece,'Retenue Sur Reglement' as libelle,reglement_retenu.code as numeropiece,reglement_retenu_source.total_retenu as debit,0 as credit,reglement_retenu_source.partner_id FROM reglement_retenu_source left outer join reglement_retenu on reglement_retenu_source.retenu_id = reglement_retenu.id where   reglement_retenu_source.state ='close' and reglement_retenu_source.total_retenu <> 0  and   reglement_retenu_source.partner_id= %s and date_retenu >= %s and date_retenu <= %s ",(fournisseur_id,datedebut,datefin,))
            ListeReglementRetenue = cr.dictfetchall()
            print 'Reglement Retenue C Bon!!!!!!!!!!'
            if str(ListeReglementRetenue) != 'None':
               if len(ListeReglementRetenue) > 0:
                  for ReglementRetenue in ListeReglementRetenue:
                      datetpiece0 = ReglementRetenue['datepiece'].split("-")[0]
                      datetpiece1 = ReglementRetenue['datepiece'].split("-")[1]
                      datetpiece2 = ReglementRetenue['datepiece'].split("-")[2]
                      datetpiece3 = datetpiece2.split(" ")[0]
                      datetpiece = datetpiece3 +"/"+ datetpiece1 +"/"+ datetpiece0
                      libellepiece= ReglementRetenue['libelle']
                      numeropiece= ReglementRetenue['numeropiece']
                      debit= ReglementRetenue['debit']
                      credit= ReglementRetenue['credit']
                      data={
                      'header1':header1,
                      'header2':header2,
                      'raison_social':RaisonSocial,
                      'matricule_fiscale':MatriculeFiscale,
                      'date_debut':datedebut,
                      'date_fin':datefin,
                      'date_piece':datetpiece,
                      'libelle':libellepiece,
                      'num_piece':numeropiece,
                      'debit':debit,
                      'credit':credit,
                      'user':obj_user.name,
                      'date_report_precedent':ReportDatePiece,
                      'libelle_report_precedent':ReportLibellePiece,
                      'num_piece_report_precedent':ReportNumeroPiece,
                      'debit_report_precedent':ReportDebit,
                      'credit_report_precedent':ReportCredit,  
                       
                      } 
                      result.append(data)
                      result2.append(data)
            #End Region Reglement Retenue
            #Region Region Reglement Fournisseur Sur LesFactures  Impyees********************* none enter*****
            cr.execute("SELECT distinct(rp.id) as idreglementimpayee FROM reglement_detail_impaye rdi left outer join reglement_paiement rp on rdi.reglement_id = rp.id  where rp.state='close' and rp.partner_id = %s and rp.date_reglement >= %s and rp.date_reglement <= %s ",(fournisseur_id,datedebut,datefin,))
            ReglementImpayee = cr.dictfetchone()
            print 'ReglementImpayee!!!!!!!',ReglementImpayee
            if str(ReglementImpayee) != 'None':
               if len(ReglementImpayee) > 0:
                  IdReglementImpayee = ReglementImpayee['idreglementimpayee']
                  if str(IdReglementImpayee) =='None':
                     print 'IdReglementImpayee!!!!',IdReglementImpayee
                  else :
                        cr.execute("SELECT  res_partner.ref as fournisseur, regpiece.id as numpiece, res_partner.id as idfr ,rdi.date_echance as datepiece, reglement_mode.designation as desreglement,regpiece.num_cheque_traite as numchequetraite,0 as debit, sum(rdi.montant) as credit FROM reglement_detail_impaye rdi left outer join reglement_paiement rp on rdi.reglement_id = rp.id left outer join reglement_piece regpiece on rdi.piece_id = regpiece.id  left outer join reglement_mode on  regpiece.mode_reglement = reglement_mode.id left outer join res_partner on regpiece.partner_id = res_partner.id where rp.state='close' and res_partner.id = %s and rdi.date_echance >= %s and rdi.date_echance <= %s and rp.id = %s group by res_partner.ref , rdi.date_echance , reglement_mode.designation,regpiece.num_cheque_traite,res_partner.id,regpiece.id ",(fournisseur_id,datedebut,datefin,IdReglementImpayee))
                        ListeReglementImpayee = cr.dictfetchall()
                        for ReglementImpayeeFR in ListeReglementImpayee:
                            datetpiece = ReglementImpayeeFR['datepiece']
                            Annee = datetpiece.split("-")[0]
                            Mois = datetpiece.split("-")[1]
                            Jour = datetpiece.split("-")[2]
                            datetpiece = Jour +"/"+ Mois +"/"+ Annee
                            impayee ='Impayee'
                            LibelleModeReglement = ReglementImpayeeFR['desreglement']
                            Num = 'N°'
                            NuChequeTraite = ReglementImpayeeFR['numchequetraite']
                            libellepiece = impayee +' '+ LibelleModeReglement +' '+  Num +' ' + NuChequeTraite
                            numeropiece = ReglementImpayeeFR['numpiece']
                            debit= ReglementImpayeeFR['debit']
                            credit= ReglementImpayeeFR['credit']
                            data={
                            'header1':header1,
                            'header2':header2,
                            'raison_social':RaisonSocial,
                            'matricule_fiscale':MatriculeFiscale,
                            'date_debut':datedebut,
                            'date_fin':datefin,
                            'date_piece':datetpiece,
                            'libelle':libellepiece,
                            'num_piece':numeropiece,
                            'debit':debit,
                            'credit':credit,
                            'user':obj_user.name,
                            'date_report_precedent':ReportDatePiece,
                            'libelle_report_precedent':ReportLibellePiece,
                            'num_piece_report_precedent':ReportNumeroPiece,
                            'debit_report_precedent':ReportDebit,
                            'credit_report_precedent':ReportCredit,  
                           
                            } 
                            result.append(data)
                            result2.append(data)
            #End Region Reglement Fournisseur Sur LesFactures  Impyees*********************
            #Region GainPerte
            #End Region GainPerte
            if len(result2) == 0:
               data={
               'header1':header1,
               'header2':header2,
               'raison_social':RaisonSocial,
               'matricule_fiscale':MatriculeFiscale,
               'date_debut':datedebut,
               'date_fin':datefin,
               'date_piece':'',
               'libelle':'',
               'num_piece':'',
               'debit':0,
               'credit':0,
               'user':obj_user.name,
               'date_report_precedent':ReportDatePiece,
               'libelle_report_precedent':ReportLibellePiece,
               'num_piece_report_precedent':ReportNumeroPiece,
               'debit_report_precedent':ReportDebit,
               'credit_report_precedent':ReportCredit,
               } 
               result.append(data)
        return result
jasper_report.report_jasper('report.jasper_grand_livre_commercial_print', 'xxxxx', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
