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
            from_date = data['form']['date_from']
            to_date = data['form']['date_to']
            employee_id = data['form']['employee_id']
            total=0
            dateAuj = time.strftime('%d-%m-%Y %H:%M')
            holidays_status_ids = self.pool.get('hr.holidays.status').search(cr, uid, [])#('date','>=',from_date),('date','<=',to_date),
            
            holidays_status_objs = self.pool.get('hr.holidays.status').browse(cr, uid, holidays_status_ids)
            employee = self.pool.get('hr.employee').browse(cr, uid, employee_id[0])
            if holidays_status_objs:
                for status in holidays_status_objs:


                        holidays_ids = self.pool.get('hr.holidays').search(cr, uid, [('date_from','>=',from_date),('date_to','<=',to_date),('employee_id','=',employee_id[0]),('holiday_status_id','=',status.id)])

                        holidays_objs = self.pool.get('hr.holidays').browse(cr, uid, holidays_ids)
                        if holidays_objs :
                            for holiday in holidays_objs :
                       
                                data={
                                    'employee':holiday.employee_id["name"],
                                    'date_from':holiday.date_from,
                                    'date_to':holiday.date_to,
                                    'number_jr':holiday.number_of_days_temp,
                                    'status':status.name,
                                    'descr':holiday.name,

                                    'etat':dict(self.pool.get('hr.holidays').fields_get(cr, uid, allfields=['state'], context=context)['state']['selection'])[holiday.state],#reg.state.name,

                                    'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                                    'dateAuj':dateAuj,
                                    'from_date':from_date,
                                    'to_date':to_date,
                                    'dateAuj':dateAuj,
                                    
                                } 
                                result.append(data)
                        else :
                            data={
                                        'employee':employee.name,
                                        'descr':'',

                                        'date_from':'',
                                        'date_to':'',
                                        'number_jr':'',
                                        'status':status.name,

                                        'etat':'',
                                        'from_date':from_date,
                                        'to_date':to_date,


                                        'stat_path' :os.getcwd()+"/openerp/addons/office_stat/",
                                        'dateAuj':dateAuj,
                                        
                            } 
                            result.append(data)
                        
        return result

jasper_report.report_jasper('report.jasper_conge_print', 'hr.holidays', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
