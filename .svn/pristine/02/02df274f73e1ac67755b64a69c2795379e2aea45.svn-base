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
            datedebut = data['form']['date_debut']
            datefin = data['form']['date_fin']
            
            company = self.pool.get('res.company').browse(cr,uid,1)
            
            comp_address = company.street
            comp_tel = company.phone
            comp_fax = company.fax
            
            StatePiece = ''
            if data['form']['partner_ids'] and data['form']['type_paiement'] ==False:
                partner_ids = data['form']['partner_ids']
                #cr.execute("SELECT * FROM reglement_piece,reglement_mode where type='in' and state!='cashed' and date_echance >= %s and date_echance <= %s and reglement_piece.mode_reglement = reglement_mode.id and reglement_mode.code='CHQ' AND reglement_piece.partner_id=%s",(datedebut,datefin,partner_id[0]))
                for partner_id in partner_ids :
                    cr.execute("SELECT * FROM reglement_piece,reglement_mode where type='in' and state!='cashed' and date_echance >= %s and date_echance <= %s and reglement_piece.mode_reglement = reglement_mode.id and (reglement_mode.code='CHQ' or reglement_mode.code='TRT') AND reglement_piece.partner_id = %s",(datedebut,datefin,partner_id))
#we choose the date and the type
            elif data['form']['type_paiement'] and data['form']['partner_ids'] == False:
                type_paiement = data['form']['type_paiement']
                mode = self.pool.get('reglement.mode').browse(cr,uid,type_paiement[0])
                cr.execute("SELECT * FROM reglement_piece,reglement_mode where type='in' and state!='cashed' and date_echance >= %s and date_echance <= %s and reglement_piece.mode_reglement = %s and reglement_mode.code= %s ",(datedebut,datefin,type_paiement[0],mode.code))
#we choose the date,the partner and the type
            elif data['form']['partner_ids'] and data['form']['type_paiement']:
                partner_ids = data['form']['partner_ids']
                type_paiement = data['form']['type_paiement']
                mode = self.pool.get('reglement.mode').browse(cr,uid,type_paiement[0])
                for partner_id in partner_ids :
                    cr.execute("SELECT * FROM reglement_piece,reglement_mode where type='in' and state!='cashed' and date_echance >= %s and date_echance <= %s and reglement_piece.mode_reglement = %s and reglement_mode.code= %s  AND reglement_piece.partner_id = %s",(datedebut,datefin,type_paiement[0],mode.code,partner_id))
            elif datedebut and datefin:
                #cr.execute("SELECT * FROM reglement_piece,reglement_mode where type='in' and state!='cashed' and date_echance >= %s and date_echance <= %s and reglement_piece.mode_reglement = reglement_mode.id and reglement_mode.code='CHQ'",(datedebut,datefin,)) 
                cr.execute("SELECT * FROM reglement_piece,reglement_mode where type='in' and state!='cashed' and date_echance >= %s and date_echance <= %s and reglement_piece.mode_reglement = reglement_mode.id and (reglement_mode.code='CHQ' or reglement_mode.code='TRT')",(datedebut,datefin,))
            else:
                cr.execute("SELECT * FROM reglement_piece,reglement_mode where type='in' and state!='cashed' and reglement_piece.mode_reglement = reglement_mode.id and (reglement_mode.code='CHQ' or reglement_mode.code='TRT')")          
            liste_reglementpiece= cr.dictfetchall()
            if len(liste_reglementpiece) > 0:
             
                for ReglementPiece in liste_reglementpiece:
                   
                    NumCheque_Traite = ReglementPiece['num_cheque_traite']
                    DateEcheance = ReglementPiece['date_echance']
                    MontantPiece = round(ReglementPiece['montant_piece'],3)
                    NaturePiece = ReglementPiece['nature_piece']
                    ModeReglement = ReglementPiece['designation']
                    EtatPiece = ReglementPiece['state']
                    partner = self.pool.get('res.partner').browse(cr, uid, ReglementPiece['partner_id'], context=context)
                  
                    if str(EtatPiece) == 'free': 
                        StatePiece = 'Libre'
                    if str(EtatPiece) == 'integrated': 
                                    StatePiece = 'Intégré'
                    if str(EtatPiece) == 'pimpaid': 
                                    StatePiece = 'Partiellement Payé'
                    if str(EtatPiece) == 'impaid':  
                                    StatePiece = 'Impayé'
                    if str(EtatPiece) == 'cashed':  
                                    StatePiece = 'Encaissé'
                    if NaturePiece == 'notre_piece':
                                       NaturePiece = 'Notre Pièce'
                    else:
                                       NaturePiece = 'Pièce client'
                    DateEcheance = DateEcheance.split('-')[2]+'/'+DateEcheance.split('-')[1]+'/'+DateEcheance.split('-')[0]
                    
                    data={
                        'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                        'company_address':comp_address,   
                        'company_tel':comp_tel,  
                        'company_fax':comp_fax,        
                                 'partenaire':partner.name,
                                 'num_cheque_traite':NumCheque_Traite,
                                 'date_echeance':DateEcheance,
                                 'montant_piece':MontantPiece,
                                 'nature_piece':NaturePiece,
                                 'mode_reglement':ModeReglement,
                                 'etat_piece':StatePiece,
                     
                    } 
                    result.append(data)
                   
            else:
               
               data={
               'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
               'company_address':comp_address,   
               'company_tel':comp_tel,  
               'company_fax':comp_fax,  
               'partenaire':'',
               'num_cheque_traite':'',
               'date_echeance':'',
               'montant_piece':0,
               'nature_piece':'',
               'mode_reglement':'',
               'etat_piece':'',
             
            
               } 
               result.append(data)

        return result
jasper_report.report_jasper('report.jasper_liste_cheque_fournisseur_print', 'reglement.piece', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
