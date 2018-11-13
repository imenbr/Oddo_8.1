# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import base64
#import os
#import netsvc

from datetime import datetime
import xlwt
from xlwt import Workbook
from ftplib import FTP
import StringIO

class category_products_wizard(osv.osv_memory):
    _name = "category.products.wizard"
    _description = " wizard to generate category products report"

    _columns = {
        
        'category_ids':fields.many2many('product.category',
                                    'product_category_rel',
                                    'product_id',
                                    'category_id','Categorie'),
        'report_type':fields.selection([("pdf","PDF"),
                                        ("xls","Excel"),
                                        ],'Type'),
        
        'state': fields.selection([('choose','choose'),
                                    ('get','get'),
                                   ]),
	'name': fields.char('Nom fichier', size=256),
	'db_datas': fields.binary('Data', oldname='datas'),

    }
    _defaults = { 
        'report_type': lambda *a: 'pdf',
        'state': lambda *a: 'choose',
        'name': lambda *a: 'Produit_Par_Categorie.xls',
    }
    def generate_file(self, cr, uid, ids,  context):
        '''
           Méthode qui génére un fichier excel pour les produits de chaque catégorie
           @return:db_datas and file name
        '''
        result=[]
        name_template=False
        name_category=False
        precedent_name_categorie='nouvelle categorie'
	name=' '
        x=1
      
 	test = Workbook()
        style_title=xlwt.easyxf('font:bold on,italic on;align:wrap on,vert centre,horiz centre;' "borders: top double,bottom double,left double,right double;")
        
        if x==1:
	    this = self.browse(cr, uid, ids)[0]
	    if this.name:
	        file_name=this.name
	    else:
	        file_name='Produit_Par_Categorie'
	    name="%s.xls" %(file_name)
	    for category_ids in this.category_ids:
		        category_id=category_ids.id    
		        cr.execute('''SELECT 
	  product_category.name as name_category, 
	  product_uom.name as uom, 
	  product_product.name_template as name_template, 
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
		                if name_category == precedent_name_categorie:
                                   
		                    feuil1.write(x,0,name_template)
		                    feuil1.write(x,1,default_code)
		                    feuil1.write(x,2,uom)
		                    feuil1.write(x,3,description)
		                else:
		                    x=1
		                    feuil1 = test.add_sheet(name_category)
		                    feuil1.write(0,0,'Produit',style_title)
		                    feuil1.write(0,1,u'Référence',style_title)
		                    feuil1.write(0,2,u'Unité',style_title)
		                    feuil1.write(0,3,u'Description',style_title)
		                    feuil1.col(0).width = 10000
		                    feuil1.col(1).width = 5000
		                    feuil1.col(2).width = 5000
		                    feuil1.col(3).width = 7000
		                    feuil1.write(x,0,name_template)
		                    feuil1.write(x,1,default_code)
		                    feuil1.write(x,2,uom)
		                    feuil1.write(x,3,description)
		                precedent_name_categorie=name_category
                              
		                x=x+1 
           
	    file_data=StringIO.StringIO()
	    o=test.save(file_data)   
	    out=base64.encodestring(file_data.getvalue())
           
        return self.write(cr, uid, ids, {'db_datas':out,'name':name}, context=context)

    def create_report(self, cr, uid, ids, context={}):
        '''
           Méthode qui génére le rapport
        '''
        data = self.read(cr,uid,ids,)[-1]
        print data,' create_report('
	res={}
	res={
            'type'         : 'ir.actions.report.xml',
            'report_name'   : 'jasper_report_category_product_print',
            'datas': {
                    'model':'product.category',
                    'id': context.get('active_ids') and context.get('active_ids')[0] or False,
                    'ids': context.get('active_ids') and context.get('active_ids') or [],
                    'report_type': data['report_type'],
                    'form':data
                    },
            'nodestroy': False
        }
        return res

category_products_wizard()
