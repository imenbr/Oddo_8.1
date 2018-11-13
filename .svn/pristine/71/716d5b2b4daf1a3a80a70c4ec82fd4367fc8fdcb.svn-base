# -*- encoding: utf-8 -*-
# -*- encoding: ISO-8859-1 -*-
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

from datetime import datetime,timedelta
import base64
import os
import calendar
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

            trimestre = data['form']['trimestre']
            year= datetime.now().year 
            date= datetime.now().strftime('%d-%m-%Y')
            print "000000000000000000000000000000000   A",(datetime.now() - timedelta(days=7)).date()


            a_reporter=0.00
            j=int(trimestre)
            employee_ids=pool.get('hr.employee').search(cr, uid, [('slip_ids','!=','')])
            employee_objs=pool.get('hr.employee').browse(cr, uid, employee_ids)

            if employee_objs:

                for employee in employee_objs:
                    
                    res={}
                    res[1]=0.0
                    res[2]=0.0
                    res[3]=0.0
                    company=pool.get('res.company').browse(cr, uid, employee.company_id.id)
                    mois=(2*j)+(j+(-2)) #+j 
                    print "******",mois

                    ## Fiche de paie 1
                    from_date1=datetime(year,mois,1)
                    print "from_date1mmmmmmmmmmmmmm",from_date1
                    to_date1=datetime(year,mois,calendar.monthrange(year,mois)[1])

                    
                    payslip_ids1 = pool.get('hr.payslip').search(cr, uid, [('date_from','=',from_date1),('date_to','=',to_date1),('employee_id','=',employee.id)])
                    payslip_objs1 = pool.get('hr.payslip').browse(cr, uid, payslip_ids1)

                    ## Fiche de paie 2
                    from_date2=datetime(year,mois+1,1)
                    to_date2=datetime(year,mois+1,calendar.monthrange(year,mois+1)[1])#

                    payslip_ids2 = pool.get('hr.payslip').search(cr, uid, [('date_from','=',from_date2),('date_to','=',to_date2),('employee_id','=',employee.id)])
                    payslip_objs2 = pool.get('hr.payslip').browse(cr, uid, payslip_ids2)

                    ## Fiche de paie 3
                    from_date3=datetime(year,mois+2,1)
                    to_date3=datetime(year,mois+2,calendar.monthrange(year,mois+2)[1])#

                    payslip_ids3 = pool.get('hr.payslip').search(cr, uid, [('date_from','=',from_date3),('date_to','=',to_date3),('employee_id','=',employee.id)])
                    payslip_objs3 = pool.get('hr.payslip').browse(cr, uid, payslip_ids3)
                       
                    if payslip_objs1:
                        for pay1 in payslip_objs1:

                            hr_payslip_line_ids = self.pool.get('hr.payslip.line').search(cr, uid, [('slip_id', '=', pay1.id)])
                            hr_payslip_line_obj = self.pool.get('hr.payslip.line').browse(cr,uid,hr_payslip_line_ids)

                            for hr_payslip_line in hr_payslip_line_obj :
                                if hr_payslip_line.code=='BRUT' :
                    		        res[1]=hr_payslip_line.total
                    if payslip_objs2:
                        for pay2 in payslip_objs2:

                            hr_payslip_line_ids = self.pool.get('hr.payslip.line').search(cr, uid, [('slip_id', '=', pay2.id)])
                            hr_payslip_line_obj = self.pool.get('hr.payslip.line').browse(cr,uid,hr_payslip_line_ids)

                            for hr_payslip_line in hr_payslip_line_obj :
                                if hr_payslip_line.code=='BRUT' :
                    		        res[2]=hr_payslip_line.total

                    if payslip_objs3:
                        for pay3 in payslip_objs3:

                            hr_payslip_line_ids = self.pool.get('hr.payslip.line').search(cr, uid, [('slip_id', '=', pay3.id)])
                            hr_payslip_line_obj = self.pool.get('hr.payslip.line').browse(cr,uid,hr_payslip_line_ids)

                            for hr_payslip_line in hr_payslip_line_obj :
                                if hr_payslip_line.code=='BRUT' :
                    		        res[3]=hr_payslip_line.total

                    		        
                    a_reporter+=res[1]+res[2]+res[3]
                                

                    data={
                        'brut1':res[1],
                        'brut2':res[2],
                        'brut3':res[3],
                        'total':res[1]+res[2]+res[3],
                        'a_reporter':a_reporter,
                        'employee':employee.name,
                        'matricule':employee.num_chezemployeur,
                        'cnss':employee.matricule_cnss, 
                        'trimestre':trimestre,
                        'year':year,
                        'date':date,
                        'company_name':company.name,
                        'company_street':company.street,
                        'company_street2':company.street2,
                        'company_city':company.city,
                        'company_zip':company.zip,
                        'company_vat':company.vat[2:-8],
                     
                    } 
                    result.append(data)

                    
            else :
                   data={
                            'brut1':res[0],
                            'brut2':res[1],
                            'brut3':res[2],
                            'total':res[0]+res[1]+res[2],
                            'matricule':employee.num_chezemployeur,
                            'cnss':employee.matricule_cnss,
                            'trimestre':trimestre,
                            'year':year,
                            'date':date,
                            'company_name':company.name,
                            'company_street':company.street,
                            'company_street2':company.street2,
                            'company_city':company.city,
                            'company_zip':company.zip,
                            'company_vat':company.vat[2:-8],

                            
                        } 
                   result.append(data)         
        return result

jasper_report.report_jasper('report.jasper_declaration_cnss_print', 'hr.payslip', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
