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
import time, datetime
from datetime import datetime
import os
import calendar
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

            annee = data['form']['annee']
            date= datetime.now().strftime('%d-%m-%Y')

            employee_ids=pool.get('hr.employee').search(cr, uid, [('slip_ids','!=','')])
            employee_objs=pool.get('hr.employee').browse(cr, uid, employee_ids)

            if employee_objs:
                for employee in employee_objs:
                    if employee.chef_famille :
                        chef_famille='O'
                    else:
                         chef_famille='N'
                    if employee.marital=='single' :
                        marital='C'
                    elif employee.marital=='married' :
                        marital='M'
                    else :
                        marital=' '
                    if employee.street and employee.street2 and employee.city:
                        adresse=employee.street+" "+employee.street2+" "+employee.city
                    else :
                        adresse= " "
                    imposable=0
                    irpp=0
                    company=pool.get('res.company').browse(cr, uid, employee.company_id.id)
                    from_date=datetime(int(annee),1,calendar.monthrange(int(annee),1)[1])
                    to_date=datetime(int(annee),12,calendar.monthrange(int(annee),12)[1])
                    payslip_ids = pool.get('hr.payslip').search(cr, uid, [('date_from','>=',from_date),('date_to','<=',to_date),('employee_id','=',employee.id)])
                    payslip_objs = pool.get('hr.payslip').browse(cr, uid, payslip_ids)
                   
                    if payslip_objs:
                        for pay in payslip_objs:
                            hr_payslip_line_ids = self.pool.get('hr.payslip.line').search(cr, uid, [('slip_id', '=', pay.id)])

                            hr_payslip_line_obj = self.pool.get('hr.payslip.line').browse(cr,uid,hr_payslip_line_ids)


                            for hr_payslip_line in hr_payslip_line_obj :
                                if hr_payslip_line.code=='C_IMP' :
                    		        imposable+=hr_payslip_line.total
                                if hr_payslip_line.code=='IRPP' :
                    		        irpp+=hr_payslip_line.total

                    data={

                        'cin':employee.num_cin,
                        'employee':employee.name,
                        'matricule':employee.num_chezemployeur,
                        'stat_path' :os.getcwd()+"/addons/pay_report/",
                        'adresse':adresse,
                        'situation':marital,
                        'chef_famille':chef_famille, 
                        'irpp':irpp,
                        'enfant':employee.children ,
                        'imposable':imposable,
                        'net':imposable-irpp,
                        'annee':annee,
                        'date':date,
                        'company_name':company.name,
                        'company_street':company.street,
                        'company_street2':company.street2,
                        'company_city':company.city,
                        'company_zip':company.zip,
                     
                    } 
                    result.append(data)
            else :
                   data={
                            'net':0.00,
                            'cin':employee.num_cin,
                            'employee':employee.name,
                            'matricule':employee.num_chezemployeur,
                            'stat_path' :os.getcwd()+"/addons/pay_report/",
                            'adresse':adresse,
                            'situation':marital,
                            'chef_famille':chef_famille,
                            'irpp':0.00,
                            'enfant':employee.children,
                            'imposable':0.00,
                            'annee':annee,
                            'date':date,
                            'company_name':company.name,
                            'company_street':company.street,
                            'company_street2':company.street2,
                            'company_city':company.city,
                            'company_zip':company.zip,

                            
                        } 
                   result.append(data)         
                    

        return result

jasper_report.report_jasper('report.jasper_impot_print', 'hr.payslip', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
