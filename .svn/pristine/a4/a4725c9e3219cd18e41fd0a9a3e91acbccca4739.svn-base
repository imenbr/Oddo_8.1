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
        if 'form' in data:
            ModeReglement = ''
            draft = 'draft'
            false = 'False'
            StatePiece = ''
            free = 'free'
            pimpaid = 'pimpaid'
            integrated = 'integrated'
            impaid = 'impaid'
            cashed = 'cashed'
            NameFournisseur = ''
            cr.execute("SELECT parametre1,parametre2 FROM res_company WHERE id = 1")
            obj_company = cr.dictfetchone()
            header1 = obj_company['parametre1']
            header2 = obj_company['parametre2'] 
            obj_user = self.pool.get('res.users').browse(cr, uid, uid)
            datedebut = data['form']['date_debut']
            datefin = data['form']['date_fin']
            etatpiece = data['form']['etat_cheque']
            banque_id = data['form']['banque_id']
            fournisseur_id = data['form']['fournisseur_id']
            
            cr.execute("SELECT * FROM res_partner where id = %s ",(fournisseur_id,))
            ObjectFournisseur = cr.dictfetchone()
            
            NameFournisseur = ObjectFournisseur["name"]
            
            mode_reglement_id = data['form']['mode_reglement_id']
            
            if (str(mode_reglement_id)) != 'False':
                cr.execute("SELECT id, code, designation FROM reglement_mode WHERE id = %s ",(mode_reglement_id,))
                ModeReglement = cr.dictfetchone()
                
            else :
                  ModeReglement = 'None'
            #rim modif 14/04/2014 
            #if str(ModeReglement) != 'None':
            if ModeReglement != 'None':
            #end rim modif 14/04/2014 
               if ((str(ModeReglement['code']) == 'TRT') or (str(ModeReglement['code']) == 'CHQ')):
                    
                    if str(etatpiece) == str(false):
                       if str(banque_id) == str(false):
                          
                          #cr.execute("SELECT reglement_piece.id, reglement_piece.create_uid, reglement_piece.create_date, reglement_piece.write_date, reglement_piece.write_uid, reglement_piece.banque_id, reglement_piece.date_echance  , reglement_piece.num_compte, reglement_piece.num_cheque_traite, reglement_piece.state, reglement_piece.montant_paye, reglement_piece.agence, reglement_piece.titulaire, reglement_piece.code_piece, reglement_piece.partner_id, reglement_piece.mode_reglement, reglement_piece.nature_piece, reglement_piece.montant_piece,res_partner.name as name_partener,reglement_mode.designation as mode_reglement FROM reglement_piece left outer join res_partner on reglement_piece.partner_id = res_partner.id left outer join reglement_mode on reglement_piece.mode_reglement = reglement_mode.id where date_echance >= %s and date_echance <= %s and reglement_piece.state != 'draft' and reglement_mode.id = %s ",(datedebut,datefin,mode_reglement_id))
                          cr.execute("SELECT * FROM reglement_piece rp left outer join reglement_mode rm on rp.mode_reglement = rm.id where rp.state != 'draft'   and rp.date_echance >= %s and rp.date_echance <= %s and rm.id = %s and rp.partner_id = %s",(datedebut,datefin,mode_reglement_id,fournisseur_id))
                          #cr.execute("SELECT * FROM reglement_piece rp left outer join reglement_banque rb on rp.banque_id = rb.id left outer join reglement_mode rm on rp.mode_reglement = rm.id where rp.state != 'draft'  and rp.date_echance >= %s and rp.date_echance <= %s rm.id = %s ",(datedebut,datefin,mode_reglement_id)) jointure avec banque
                          liste_reglementpiece= cr.dictfetchall()
                          if len(liste_reglementpiece) > 0:
                             res = liste_reglementpiece
                             
                             for ReglementPiece in liste_reglementpiece:
                                 #Partenaire = ReglementPiece['name_partener']
                                 NumCheque_Traite = ReglementPiece['num_cheque_traite']
                                 DateEcheance = ReglementPiece['date_echance']
                                 MontantPiece = round(ReglementPiece['montant_piece'],3)
                                 NaturePiece = ReglementPiece['nature_piece']
                                 print 'aaa',NaturePiece
                                 ModeReglement = ReglementPiece['designation']
                                 EtatPiece = ReglementPiece['state']
                                 if str(EtatPiece) == str(free): 
                                    StatePiece = 'Libre'
                                 if str(EtatPiece) == str(integrated): 
                                    StatePiece = 'Intégré'
                                 if str(EtatPiece) == str(pimpaid): 
                                    StatePiece = 'Partiellement Payé'
                                 if str(EtatPiece) == str(impaid):  
                                    StatePiece = 'Impayé'
                                 if str(EtatPiece) == str(cashed):  
                                    StatePiece = 'En caissé'
                                 if NaturePiece == 'notre_piece':
                                       NaturePiece = 'Notre Pièce'
                                 else:
                                       NaturePiece = 'Pièce client'
                                 DateEcheance = DateEcheance.split('-')[2]+'/'+DateEcheance.split('-')[1]+'/'+DateEcheance.split('-')[0]
                                 data={
                                 'header1':header1,
                                 'header2':header2,
                                 'partenaire':NameFournisseur,
                                 'num_cheque_traite':NumCheque_Traite,
                                 'date_echeance':DateEcheance,
                                 'montant_piece':MontantPiece,
                                 'nature_piece':NaturePiece,
                                 'mode_reglement':ModeReglement,
                                 'etat_piece':StatePiece,
                                 'nom_banque':'',
                                 'user':obj_user.name,
                                 } 
                                 result.append(data)
                       else :
                             
                             cr.execute(" Select * from reglement_banque where id = %s ", (banque_id,))
                             banque=cr.dictfetchone()
                             nom_banque= banque['code']
                            
                             #cr.execute("SELECT reglement_piece.id, reglement_piece.create_uid, reglement_piece.create_date, reglement_piece.write_date, reglement_piece.write_uid, reglement_piece.banque_id, reglement_piece.date_echance, reglement_piece.num_compte, reglement_piece.num_cheque_traite, reglement_piece.state, reglement_piece.montant_paye, reglement_piece.agence, reglement_piece.titulaire, reglement_piece.code_piece, reglement_piece.partner_id, reglement_piece.mode_reglement, reglement_piece.nature_piece, reglement_piece.montant_piece,res_partner.name as name_partener,reglement_mode.designation as mode_reglement FROM reglement_piece left outer join res_partner on reglement_piece.partner_id = res_partner.id left outer join reglement_mode on reglement_piece.mode_reglement = reglement_mode.id  where reglement_piece.state != 'draft' and  date_echance >= %s and date_echance <= %s and reglement_piece.banque_id = %s and reglement_mode.id = %s ",(datedebut,datefin,banque_id,mode_reglement_id))
                             cr.execute("SELECT * FROM reglement_piece rp left outer join reglement_banque rb on rp.banque_id = rb.id left outer join reglement_mode rm on rp.mode_reglement = rm.id where rp.state != 'draft' and rp.date_echance >= %s and rp.date_echance <= %s and rm.id = %s and rp.partner_id = %s ",(datedebut,datefin,mode_reglement_id,fournisseur_id))
                             liste_reglementpiece= cr.dictfetchall()
                             if len(liste_reglementpiece) > 0:
                                res = liste_reglementpiece
                                for ReglementPiece in liste_reglementpiece:
                                    #Partenaire = ReglementPiece['name_partener']
                                    NumCheque_Traite = ReglementPiece['num_cheque_traite']
                                    DateEcheance = ReglementPiece['date_echance']
                                    MontantPiece = round(ReglementPiece['montant_piece'],3)
                                    NaturePiece = ReglementPiece['nature_piece']
                                    print 'aaa',NaturePiece
                                    ModeReglement = ReglementPiece['designation']
                                    EtatPiece = ReglementPiece['state']
                                    if str(EtatPiece) == str(free): 
                                       StatePiece = 'Libre'
                                    if str(EtatPiece) == str(integrated): 
                                       StatePiece = 'Intégré'
                                    if str(EtatPiece) == str(pimpaid): 
                                       StatePiece = 'Partiellement Payé'
                                    if str(EtatPiece) == str(impaid):  
                                       StatePiece = 'Impayé'
                                    if str(EtatPiece) == str(cashed):  
                                       StatePiece = 'En caissé'
                                    if NaturePiece == 'notre_piece':
                                       NaturePiece = 'Notre Pièce'
                                    else:
                                       NaturePiece = 'Pièce client'
                                    if NaturePiece == 'notre_piece':
                                       NaturePiece = 'Notre Pièce'
                                    else:
                                       NaturePiece = 'Pièce client'
                                    DateEcheance = DateEcheance.split('-')[2]+'/'+DateEcheance.split('-')[1]+'/'+DateEcheance.split('-')[0]
                                    data={
                                    'header1':header1,
                                    'header2':header2,
                                    'partenaire':NameFournisseur,
                                    'num_cheque_traite':NumCheque_Traite,
                                    'date_echeance':DateEcheance,
                                    'montant_piece':MontantPiece,
                                    'nature_piece':NaturePiece,
                                    'mode_reglement':ModeReglement,
                                    'etat_piece':StatePiece,
                                    'nom_banque':nom_banque,
                                    'user':obj_user.name,
                                    } 
                                    result.append(data)
                    else :
                          
                          if str(banque_id) == str(false):
                             
                             #cr.execute("SELECT reglement_piece.id, reglement_piece.create_uid, reglement_piece.create_date, reglement_piece.write_date, reglement_piece.write_uid, reglement_piece.banque_id, reglement_piece.date_echance  , reglement_piece.num_compte, reglement_piece.num_cheque_traite, reglement_piece.state, reglement_piece.montant_paye, reglement_piece.agence, reglement_piece.titulaire, reglement_piece.code_piece, reglement_piece.partner_id, reglement_piece.mode_reglement, reglement_piece.nature_piece, reglement_piece.montant_piece,res_partner.name as name_partener,reglement_mode.designation as mode_reglement FROM reglement_piece left outer join res_partner on reglement_piece.partner_id = res_partner.id left outer join reglement_mode on reglement_piece.mode_reglement = reglement_mode.id where date_echance >= %s and date_echance <= %s and reglement_piece.state = %s and reglement_mode.id = %s ",(datedebut,datefin,etatpiece,mode_reglement_id))
                             #cr.execute("SELECT * FROM reglement_piece rp left outer join reglement_banque rb on rp.banque_id = rb.id left outer join reglement_mode rm on rp.mode_reglement = rm.id where rp.state = %s and rp.date_echance >= %s and rp.date_echance <= %s rm.id = %s and rp.partner_id = %s ",(etatpiece,datedebut,datefin,mode_reglement_id,fournisseur_id)) jointure avec banque
                             cr.execute("SELECT * FROM reglement_piece rp left outer join reglement_mode rm on rp.mode_reglement = rm.id where rp.state != 'draft' and rp.state = %s   and rp.date_echance >= %s and rp.date_echance <= %s and rm.id = %s and rp.partner_id = %s",(etatpiece,datedebut,datefin,mode_reglement_id,fournisseur_id))
                             liste_reglementpiece= cr.dictfetchall()
                             if len(liste_reglementpiece) > 0:
                                res = liste_reglementpiece
                                for ReglementPiece in liste_reglementpiece:
                                    #Partenaire = ReglementPiece['name_partener']
                                    NumCheque_Traite = ReglementPiece['num_cheque_traite']
                                    DateEcheance = ReglementPiece['date_echance']
                                    MontantPiece = round(ReglementPiece['montant_piece'],3)
                                    NaturePiece = ReglementPiece['nature_piece']
                                    ModeReglement = ReglementPiece['designation']
                                    EtatPiece = ReglementPiece['state']
                                    if str(EtatPiece) == str(free): 
                                       StatePiece = 'Libre'
                                    if str(EtatPiece) == str(integrated): 
                                       StatePiece = 'Intégré'
                                    if str(EtatPiece) == str(pimpaid): 
                                       StatePiece = 'Partiellement Payé'
                                    if str(EtatPiece) == str(impaid):  
                                       StatePiece = 'Impayé'
                                    if str(EtatPiece) == str(cashed):  
                                       StatePiece = 'En caissé'
                                    if NaturePiece == 'notre_piece':
                                       NaturePiece = 'Notre Pièce'
                                    else:
                                       NaturePiece = 'Pièce client'
                                    DateEcheance = DateEcheance.split('-')[2]+'/'+DateEcheance.split('-')[1]+'/'+DateEcheance.split('-')[0]
                                    data={
                                    'header1':header1,
                                    'header2':header2,
                                    'partenaire':NameFournisseur,
                                    'num_cheque_traite':NumCheque_Traite,
                                    'date_echeance':DateEcheance,
                                    'montant_piece':MontantPiece,
                                    'nature_piece':NaturePiece,
                                    'mode_reglement':ModeReglement,
                                    'etat_piece':StatePiece,
                                    'nom_banque':'',
                                    'user':obj_user.name,
                                    } 
                                    result.append(data)
                          else : 
                                
                                cr.execute(" Select * from reglement_banque where id = %s ", (banque_id,))
                                banque=cr.dictfetchone()
                                nom_banque= banque['code']
                                #cr.execute("SELECT reglement_piece.id, reglement_piece.create_uid, reglement_piece.create_date, reglement_piece.write_date, reglement_piece.write_uid, reglement_piece.banque_id, reglement_piece.date_echance  , reglement_piece.num_compte, reglement_piece.num_cheque_traite, reglement_piece.state, reglement_piece.montant_paye, reglement_piece.agence, reglement_piece.titulaire, reglement_piece.code_piece, reglement_piece.partner_id, reglement_piece.mode_reglement, reglement_piece.nature_piece, reglement_piece.montant_piece,res_partner.name as name_partener,reglement_mode.designation as mode_reglement FROM reglement_piece left outer join res_partner on reglement_piece.partner_id = res_partner.id left outer join reglement_mode on reglement_piece.mode_reglement = reglement_mode.id where date_echance >= %s and date_echance <= %s and reglement_piece.state = %s  and reglement_piece.banque_id = %s and reglement_mode.id = %s ",(datedebut,datefin,etatpiece,banque_id,mode_reglement_id))
                                cr.execute("SELECT * FROM reglement_piece rp left outer join reglement_banque rb on rp.banque_id = rb.id left outer join reglement_mode rm on rp.mode_reglement = rm.id where rp.state != 'draft' and rp.state = %s and rp.date_echance >= %s and rp.date_echance <= %s and rm.id = %s and rp.partner_id = %s ",(etatpiece,datedebut,datefin,mode_reglement_id,fournisseur_id))
                                liste_reglementpiece= cr.dictfetchall()
                                if len(liste_reglementpiece) > 0:
                                   res = liste_reglementpiece
                                   for ReglementPiece in liste_reglementpiece:
                                       Partenaire = ReglementPiece['name_partener']
                                       NumCheque_Traite = ReglementPiece['num_cheque_traite']
                                       DateEcheance = ReglementPiece['date_echance']
                                       MontantPiece = round(ReglementPiece['montant_piece'],3)
                                       NaturePiece = ReglementPiece['nature_piece']
                                       ModeReglement = ReglementPiece['designation']
                                       EtatPiece = ReglementPiece['state']
                                       if str(EtatPiece) == str(free): 
                                          StatePiece = 'Libre'
                                       if str(EtatPiece) == str(integrated): 
                                          StatePiece = 'Intégré'
                                       if str(EtatPiece) == str(pimpaid): 
                                          StatePiece = 'Partiellement Payé'
                                       if str(EtatPiece) == str(impaid):  
                                          StatePiece = 'Impayé'
                                       if str(EtatPiece) == str(cashed):  
                                          StatePiece = 'En caissé'
                                       if NaturePiece == 'notre_piece':
                                           NaturePiece = 'Notre Pièce'
                                       else:
                                           NaturePiece = 'Pièce client'
                                       DateEcheance = DateEcheance.split('-')[2]+'/'+DateEcheance.split('-')[1]+'/'+DateEcheance.split('-')[0]
                                       data={
                                       'header1':header1,
                                       'header2':header2,
                                       'partenaire':NameFournisseur,
                                       'num_cheque_traite':NumCheque_Traite,
                                       'date_echeance':DateEcheance,
                                       'montant_piece':MontantPiece,
                                       'nature_piece':NaturePiece,
                                       'mode_reglement':ModeReglement,
                                       'etat_piece':StatePiece,
                                       'nom_banque':nom_banque,
                                       'user':obj_user.name,
                                       } 
                                       result.append(data)


            




            
            #rim modif 14/04/2014 ::
            #if str(ModeReglement) == 'None':
            if ModeReglement == 'None':
            #end rim modif 14/04/2014 ::
                    if str(etatpiece) == str(false):
                       if str(banque_id) == str(false):
                          
                          #cr.execute("SELECT reglement_piece.id, reglement_piece.create_uid, reglement_piece.create_date, reglement_piece.write_date, reglement_piece.write_uid, reglement_piece.banque_id, reglement_piece.date_echance  , reglement_piece.num_compte, reglement_piece.num_cheque_traite, reglement_piece.state, reglement_piece.montant_paye, reglement_piece.agence, reglement_piece.titulaire, reglement_piece.code_piece, reglement_piece.partner_id, reglement_piece.mode_reglement, reglement_piece.nature_piece, reglement_piece.montant_piece,res_partner.name as name_partener,reglement_mode.designation as mode_reglement FROM reglement_piece left outer join res_partner on reglement_piece.partner_id = res_partner.id left outer join reglement_mode on reglement_piece.mode_reglement = reglement_mode.id where date_echance >= %s and date_echance <= %s and reglement_piece.state != 'draft' and reglement_mode.id = %s ",(datedebut,datefin,mode_reglement_id))
                          cr.execute("SELECT * FROM reglement_piece rp left outer join reglement_mode rm on rp.mode_reglement = rm.id where rp.state != 'draft'   and rp.date_echance >= %s and rp.date_echance <= %s  and rp.partner_id = %s",(datedebut,datefin,fournisseur_id))
                          #cr.execute("SELECT * FROM reglement_piece rp left outer join reglement_banque rb on rp.banque_id = rb.id left outer join reglement_mode rm on rp.mode_reglement = rm.id where rp.state != 'draft'  and rp.date_echance >= %s and rp.date_echance <= %s rm.id = %s ",(datedebut,datefin,mode_reglement_id)) jointure avec banque
                          liste_reglementpiece= cr.dictfetchall()
                          if len(liste_reglementpiece) > 0:
                             res = liste_reglementpiece
                             
                             for ReglementPiece in liste_reglementpiece:
                                 #Partenaire = ReglementPiece['name_partener']
                                 NumCheque_Traite = ReglementPiece['num_cheque_traite']
                                 DateEcheance = ReglementPiece['date_echance']
                                 MontantPiece = round(ReglementPiece['montant_piece'],3)
                                 NaturePiece = ReglementPiece['nature_piece']
                                 ModeReglement = ReglementPiece['designation']
                                 EtatPiece = ReglementPiece['state']
                                 if str(EtatPiece) == str(free): 
                                    StatePiece = 'Libre'
                                 if str(EtatPiece) == str(integrated): 
                                    StatePiece = 'Intégré'
                                 if str(EtatPiece) == str(pimpaid): 
                                    StatePiece = 'Partiellement Payé'
                                 if str(EtatPiece) == str(impaid):  
                                    StatePiece = 'Impayé'
                                 if str(EtatPiece) == str(cashed):  
                                    StatePiece = 'En caissé'
                                 if NaturePiece == 'notre_piece':
                                       NaturePiece = 'Notre Pièce'
                                 else:
                                       NaturePiece = 'Pièce client'
                                 DateEcheance = DateEcheance.split('-')[2]+'/'+DateEcheance.split('-')[1]+'/'+DateEcheance.split('-')[0]
                                 data={
                                 'header1':header1,
                                 'header2':header2,
                                 'partenaire':NameFournisseur,
                                 'num_cheque_traite':NumCheque_Traite,
                                 'date_echeance':DateEcheance,
                                 'montant_piece':MontantPiece,
                                 'nature_piece':NaturePiece,
                                 'mode_reglement':ModeReglement,
                                 'etat_piece':StatePiece,
                                 'nom_banque':'',
                                 'user':obj_user.name,
                                 } 
                                 result.append(data)
                       else :
                             
                             cr.execute(" Select * from reglement_banque where id = %s ", (banque_id,))
                             banque=cr.dictfetchone()
                             nom_banque= banque['code']
                            
                             #cr.execute("SELECT reglement_piece.id, reglement_piece.create_uid, reglement_piece.create_date, reglement_piece.write_date, reglement_piece.write_uid, reglement_piece.banque_id, reglement_piece.date_echance, reglement_piece.num_compte, reglement_piece.num_cheque_traite, reglement_piece.state, reglement_piece.montant_paye, reglement_piece.agence, reglement_piece.titulaire, reglement_piece.code_piece, reglement_piece.partner_id, reglement_piece.mode_reglement, reglement_piece.nature_piece, reglement_piece.montant_piece,res_partner.name as name_partener,reglement_mode.designation as mode_reglement FROM reglement_piece left outer join res_partner on reglement_piece.partner_id = res_partner.id left outer join reglement_mode on reglement_piece.mode_reglement = reglement_mode.id  where reglement_piece.state != 'draft' and  date_echance >= %s and date_echance <= %s and reglement_piece.banque_id = %s and reglement_mode.id = %s ",(datedebut,datefin,banque_id,mode_reglement_id))
                             cr.execute("SELECT * FROM reglement_piece rp left outer join reglement_banque rb on rp.banque_id = rb.id left outer join reglement_mode rm on rp.mode_reglement = rm.id where rp.state != 'draft' and rp.date_echance >= %s and rp.date_echance <= %s  and rp.partner_id = %s ",(datedebut,datefin,fournisseur_id))
                             liste_reglementpiece= cr.dictfetchall()
                             if len(liste_reglementpiece) > 0:
                                res = liste_reglementpiece
                                for ReglementPiece in liste_reglementpiece:
                                    #Partenaire = ReglementPiece['name_partener']
                                    NumCheque_Traite = ReglementPiece['num_cheque_traite']
                                    DateEcheance = ReglementPiece['date_echance']
                                    MontantPiece = round(ReglementPiece['montant_piece'],3)
                                    NaturePiece = ReglementPiece['nature_piece']
                                    ModeReglement = ReglementPiece['designation']
                                    EtatPiece = ReglementPiece['state']
                                    if str(EtatPiece) == str(free): 
                                       StatePiece = 'Libre'
                                    if str(EtatPiece) == str(integrated): 
                                       StatePiece = 'Intégré'
                                    if str(EtatPiece) == str(pimpaid): 
                                       StatePiece = 'Partiellement Payé'
                                    if str(EtatPiece) == str(impaid):  
                                       StatePiece = 'Impayé'
                                    if str(EtatPiece) == str(cashed):  
                                       StatePiece = 'En caissé'
                                    if NaturePiece == 'notre_piece':
                                       NaturePiece = 'Notre Pièce'
                                    else:
                                       NaturePiece = 'Pièce client'
                                    DateEcheance = DateEcheance.split('-')[2]+'/'+DateEcheance.split('-')[1]+'/'+DateEcheance.split('-')[0]
                                    data={
                                    'header1':header1,
                                    'header2':header2,
                                    'partenaire':NameFournisseur,
                                    'num_cheque_traite':NumCheque_Traite,
                                    'date_echeance':DateEcheance,
                                    'montant_piece':MontantPiece,
                                    'nature_piece':NaturePiece,
                                    'mode_reglement':ModeReglement,
                                    'etat_piece':StatePiece,
                                    'nom_banque':nom_banque,
                                    'user':obj_user.name,
                                    } 
                                    result.append(data)
                    else :
                          
                          if str(banque_id) == str(false):
                             
                             #cr.execute("SELECT reglement_piece.id, reglement_piece.create_uid, reglement_piece.create_date, reglement_piece.write_date, reglement_piece.write_uid, reglement_piece.banque_id, reglement_piece.date_echance  , reglement_piece.num_compte, reglement_piece.num_cheque_traite, reglement_piece.state, reglement_piece.montant_paye, reglement_piece.agence, reglement_piece.titulaire, reglement_piece.code_piece, reglement_piece.partner_id, reglement_piece.mode_reglement, reglement_piece.nature_piece, reglement_piece.montant_piece,res_partner.name as name_partener,reglement_mode.designation as mode_reglement FROM reglement_piece left outer join res_partner on reglement_piece.partner_id = res_partner.id left outer join reglement_mode on reglement_piece.mode_reglement = reglement_mode.id where date_echance >= %s and date_echance <= %s and reglement_piece.state = %s and reglement_mode.id = %s ",(datedebut,datefin,etatpiece,mode_reglement_id))
                             #cr.execute("SELECT * FROM reglement_piece rp left outer join reglement_banque rb on rp.banque_id = rb.id left outer join reglement_mode rm on rp.mode_reglement = rm.id where rp.state = %s and rp.date_echance >= %s and rp.date_echance <= %s rm.id = %s and rp.partner_id = %s ",(etatpiece,datedebut,datefin,mode_reglement_id,fournisseur_id)) jointure avec banque
                             cr.execute("SELECT * FROM reglement_piece rp left outer join reglement_mode rm on rp.mode_reglement = rm.id where rp.state != 'draft' and rp.state = %s   and rp.date_echance >= %s and rp.date_echance <= %s and rp.partner_id = %s",(etatpiece,datedebut,datefin,fournisseur_id))
                             liste_reglementpiece= cr.dictfetchall()
                             if len(liste_reglementpiece) > 0:
                                res = liste_reglementpiece
                                for ReglementPiece in liste_reglementpiece:
                                    #Partenaire = ReglementPiece['name_partener']
                                    NumCheque_Traite = ReglementPiece['num_cheque_traite']
                                    DateEcheance = ReglementPiece['date_echance']
                                    MontantPiece = round(ReglementPiece['montant_piece'],3)
                                    NaturePiece = ReglementPiece['nature_piece']
                                    ModeReglement = ReglementPiece['designation']
                                    EtatPiece = ReglementPiece['state']
                                    if str(EtatPiece) == str(free): 
                                       StatePiece = 'Libre'
                                    if str(EtatPiece) == str(integrated): 
                                       StatePiece = 'Intégré'
                                    if str(EtatPiece) == str(pimpaid): 
                                       StatePiece = 'Partiellement Payé'
                                    if str(EtatPiece) == str(impaid):  
                                       StatePiece = 'Impayé'
                                    if str(EtatPiece) == str(cashed):  
                                       StatePiece = 'En caissé'
                                    if NaturePiece == 'notre_piece':
                                       NaturePiece = 'Notre Pièce'
                                    else:
                                       NaturePiece = 'Pièce client'
                                    DateEcheance = DateEcheance.split('-')[2]+'/'+DateEcheance.split('-')[1]+'/'+DateEcheance.split('-')[0]
                                    data={
                                    'header1':header1,
                                    'header2':header2,
                                    'partenaire':NameFournisseur,
                                    'num_cheque_traite':NumCheque_Traite,
                                    'date_echeance':DateEcheance,
                                    'montant_piece':MontantPiece,
                                    'nature_piece':NaturePiece,
                                    'mode_reglement':ModeReglement,
                                    'etat_piece':StatePiece,
                                    'nom_banque':'',
                                    'user':obj_user.name,
                                    } 
                                    result.append(data)
                          else : 
                                
                                cr.execute(" Select * from reglement_banque where id = %s ", (banque_id,))
                                banque=cr.dictfetchone()
                                nom_banque= banque['code']
                                #cr.execute("SELECT reglement_piece.id, reglement_piece.create_uid, reglement_piece.create_date, reglement_piece.write_date, reglement_piece.write_uid, reglement_piece.banque_id, reglement_piece.date_echance  , reglement_piece.num_compte, reglement_piece.num_cheque_traite, reglement_piece.state, reglement_piece.montant_paye, reglement_piece.agence, reglement_piece.titulaire, reglement_piece.code_piece, reglement_piece.partner_id, reglement_piece.mode_reglement, reglement_piece.nature_piece, reglement_piece.montant_piece,res_partner.name as name_partener,reglement_mode.designation as mode_reglement FROM reglement_piece left outer join res_partner on reglement_piece.partner_id = res_partner.id left outer join reglement_mode on reglement_piece.mode_reglement = reglement_mode.id where date_echance >= %s and date_echance <= %s and reglement_piece.state = %s  and reglement_piece.banque_id = %s and reglement_mode.id = %s ",(datedebut,datefin,etatpiece,banque_id,mode_reglement_id))
                                cr.execute("SELECT * FROM reglement_piece rp left outer join reglement_banque rb on rp.banque_id = rb.id left outer join reglement_mode rm on rp.mode_reglement = rm.id where rp.state != 'draft' and rp.state = %s and rp.date_echance >= %s and rp.date_echance <= %s and rp.partner_id = %s ",(etatpiece,datedebut,datefin,fournisseur_id))
                                liste_reglementpiece= cr.dictfetchall()
                                if len(liste_reglementpiece) > 0:
                                   res = liste_reglementpiece
                                   for ReglementPiece in liste_reglementpiece:
                                       Partenaire = ReglementPiece['name_partener']
                                       NumCheque_Traite = ReglementPiece['num_cheque_traite']
                                       DateEcheance = ReglementPiece['date_echance']
                                       MontantPiece = round(ReglementPiece['montant_piece'],3)
                                       NaturePiece = ReglementPiece['nature_piece']
                                       
                                       ModeReglement = ReglementPiece['designation']
                                       EtatPiece = ReglementPiece['state']
                                       if str(EtatPiece) == str(free): 
                                          StatePiece = 'Libre'
                                       if str(EtatPiece) == str(integrated): 
                                          StatePiece = 'Intégré'
                                       if str(EtatPiece) == str(pimpaid): 
                                          StatePiece = 'Partiellement Payé'
                                       if str(EtatPiece) == str(impaid):  
                                          StatePiece = 'Impayé'
                                       if str(EtatPiece) == str(cashed):  
                                          StatePiece = 'En caissé'
                                       if NaturePiece == 'notre_piece':
                                           NaturePiece = 'Notre Pièce'
                                       else:
                                           NaturePiece = 'Pièce client'
                                       DateEcheance = DateEcheance.split('-')[2]+'/'+DateEcheance.split('-')[1]+'/'+DateEcheance.split('-')[0]
                                       data={
                                       'header1':header1,
                                       'header2':header2,
                                       'partenaire':NameFournisseur,
                                       'num_cheque_traite':NumCheque_Traite,
                                       'date_echeance':DateEcheance,
                                       'montant_piece':MontantPiece,
                                       'nature_piece':NaturePiece,
                                       'mode_reglement':ModeReglement,
                                       'etat_piece':StatePiece,
                                       'nom_banque':nom_banque,
                                       'user':obj_user.name,
                                       } 
                                       result.append(data)
            if len(res) == 0:
               data={
               'header1':header1,
               'header2':header2,
               'partenaire':'',
               'num_cheque_traite':'',
               'date_echeance':'',
               'montant_piece':0,
               'nature_piece':'',
               'mode_reglement':'',
               'etat_piece':'',
               'nom_banque':'',
               'user':obj_user.name,
               } 
               result.append(data)

        return result
jasper_report.report_jasper('report.jasper_liste_cheque_print', 'reglement.piece', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
