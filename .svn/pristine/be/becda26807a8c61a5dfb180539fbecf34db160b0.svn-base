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
            #dateAuj = time.strftime('%d-%m-%Y %H:%M')

            employee_ids=pool.get('hr.employee').search(cr, uid, [('slip_ids','!=','')])
            employee_objs=pool.get('hr.employee').browse(cr, uid, employee_ids)
            date= datetime.now().strftime('%d-%m-%Y')
            if employee_objs:
                for employee in employee_objs:
                    net=0
                    brut=0
                    cnss=0
                    irpp=0
                    avance=0
                    nb_jour=0
                    nb_heure=0
                    nb_heure_supp=0
                    company=pool.get('res.company').browse(cr, uid, employee.company_id.id)
                    payslip_ids = pool.get('hr.payslip').search(cr, uid, [('date_from','>=',from_date),('date_to','<=',to_date),('employee_id','=',employee.id)])
                    payslip_objs = pool.get('hr.payslip').browse(cr, uid, payslip_ids)

                    
                   
                    if payslip_objs:
                        for pay in payslip_objs:
                            hr_payslip_line_ids = self.pool.get('hr.payslip.line').search(cr, uid, [('slip_id', '=', pay.id)])
                            hr_payslip_line_obj = self.pool.get('hr.payslip.line').browse(cr,uid,hr_payslip_line_ids)

                            hr_worked_days_ids = self.pool.get('hr.payslip.worked_days').search(cr, uid, [('payslip_id', '=', pay.id)])
                            hr_worked_days_obj = self.pool.get('hr.payslip.worked_days').browse(cr,uid,hr_worked_days_ids)
                            for hr_payslip_line in hr_payslip_line_obj :
                                if hr_payslip_line.code=='NET' :
                    		        net+=hr_payslip_line.total
                                if hr_payslip_line.code=='BRUT' :
                    		        brut+=hr_payslip_line.total
                                if hr_payslip_line.code=='CNSS' :
                    		        cnss+=hr_payslip_line.total
                                if hr_payslip_line.code=='IRPP' :
                    		        irpp+=hr_payslip_line.total
                            if hr_worked_days_obj:
                                for worked_days in hr_worked_days_obj :
                                    if worked_days.code=='WORK100':
                                        nb_jour+=worked_days.number_of_days
                                        nb_heure+=worked_days.number_of_hours
                                    if worked_days.code=='HS25' or worked_days.code=='HS50':
                                        nb_heure_supp+=worked_days.number_of_hours


                            hr_payslip_input_ids = self.pool.get('hr.payslip.input').search(cr, uid, [('payslip_id', '=', pay.id)])
                            hr_payslip_input_obj = self.pool.get('hr.payslip.input').browse(cr,uid,hr_payslip_input_ids)
                            if hr_payslip_input_obj:
                                for payinput in hr_payslip_input_obj :
                                    if payinput.code=='AV':
                                        avance+=payinput.amount



                    data={
                        'net':net,
                        'brut':brut,

                        'employee':employee.name,
                        'matricule':employee.num_chezemployeur,
                        'stat_path' :os.getcwd()+"/addons/pay_report/",
                        'nb_jour':nb_jour,
                        'nb_heure':nb_heure,
                        'nb_heure_supp':nb_heure_supp,
                        'cnss':cnss, 
                        'irpp':irpp,
                        'date':date,
                        'avance':avance,
                        'nap':net-avance,
                        'from_date':from_date,
                        'to_date':to_date,
                        'company_name':company.name,
                        'company_street':company.street,
                        'company_street2':company.street2,
                        'company_city':company.city,
                        'company_zip':company.zip,
                     
                    } 
                    result.append(data)
            else :
                   data={
                            'net':'',
                            'brut':'',
                            'employee':employee.name,
                            'matricule':employee.num_chezemployeur,
                            'stat_path' :os.getcwd()+"/addons/pay_report/",
                            'nb_jour':'',
                            'nb_heure':'',
                            'nb_heure_supp':'',
                            'cnss':'',
                            'irpp':'',
                            'date':date,
                            'avance':avance,
                            'nap':net-avance,
                            'from_date':from_date,
                            'to_date':to_date,
                            'company_name':company.name,
                            'company_street':company.street,
                            'company_street2':company.street2,
                            'company_city':company.city,
                            'company_zip':company.zip,

                            
                        } 
                   result.append(data)         
        return result

jasper_report.report_jasper('report.jasper_decompte_salaire_print', 'hr.payslip', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
