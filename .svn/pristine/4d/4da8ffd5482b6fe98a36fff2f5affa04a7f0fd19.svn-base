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
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime
import JasperDataParser  
from openerp.JasperReports import *
from openerp.jasper_reports import jasper_report
import base64

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
        name_template=False
        name_category=False
        if 'form' in data:
            category_ids = data['form']['category_ids']
            
            #cr.execute("SELECT parametre1,parametre2 FROM res_company WHERE id = 1")
            #obj_company = cr.dictfetchone()
            header1 = 'header1'#obj_company['parametre1']
            header2 = 'header2'#obj_company['parametre2']
            obj_user = self.pool.get('res.users').browse(cr, uid, uid)
            
            #cr.execute('SELECT logo FROM res_company WHERE id=1')
            #logos = cr.dictfetchall()
            #for logo in logos:
            #      logo=logo['logo']
                  
            for category_id in category_ids: 
                cr.execute('''SELECT 
  product_category.name as name_category, 
  product_uom.name as uom, 
  product_product.name_template as name_template, 
  product_template.image as image, 
  product_product.default_code as default_code,
  product_template.description as description
FROM 
  public.product_category, 
  public.product_product, 
  public.product_template, 
  public.product_uom
WHERE 
  product_product.product_tmpl_id = product_template.id AND
  product_template.uom_id = product_uom.id AND
  product_template.categ_id = product_category.id AND
  product_category.id=%s
order by name_template
                    ''', (category_id,))
                products = cr.dictfetchall()
                for product in products:
                    if product:
                        default_code = product['default_code']
                        name_template = product['name_template']
                        name_category = product['name_category']
                        description = product['description']
                        uom = product['uom']
                        
                        if product['image']:
                            image = product['image']
                            name_file_image='/home/odoo/image/%s' %(default_code)
                            open(name_file_image, 'wb').write(base64.decodestring(str(image)))
                        else:   
                            name_file_image=False
                        
                        data={
                            'name_file_image':name_file_image,
                            'header1':header1,
                            'header2':header2,
                            'default_code':default_code,
                            'name_template':name_template,
                            'description':description,
                            'name_category':name_category,
                            'uom':uom,
                            'user':obj_user.name,
                        } 
                        result.append(data)
        return result

jasper_report.report_jasper('report.jasper_report_category_product_print', 'product.category', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
