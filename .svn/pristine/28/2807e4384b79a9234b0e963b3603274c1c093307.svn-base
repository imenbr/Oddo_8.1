# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime, timedelta
import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
from openerp import api
class importation_produit(osv.osv):
    _name = "importation.produit"
    _description = "Importation Produit"


    @api.one
    @api.depends('importation_lines.price_subtotal_dt','importation_lines.price_subtotal_euro','importation_lines.DD','charges_importation_lines.amount_charge')
    def _amount_all(self):
        '''
           Methode qui calcule les montants suivants
           amount_untaxed
           amount_tax
           amount_total
           undiscount_total
           discount_total  
        '''  
		#self.amount_untaxed = sum(line.price_subtotal for line in self.devis_lines)


        
 
        self.amount_total_euro = sum(line.price_subtotal_euro for line in self.importation_lines)
        self.amount_total_dt = sum(line.price_subtotal_dt for line in self.importation_lines)
        self.amount_total_chrage_dt = sum(line.amount_charge for line in self.charges_importation_lines)
        self.amount_total_DD = sum(line.DD for line in self.importation_lines)





    _columns = {
        'name' : fields.char('Référence', required=True,readonly=True,states={'draft':[('readonly',False)]}),
        'state': fields.selection([('draft', 'Brouillon'),('confirm', 'Confirmé') ],),
        'date' : fields.datetime('Date', required=True,readonly=True,states={'draft':[('readonly',False)]}),
        'partner_id' : fields.many2one('res.partner', required=True,domain="[('supplier','=',True)]",string="Fournisseur", readonly=True, states={'draft':[('readonly',False)]}),
        'facture_id' : fields.many2one('account.invoice', required=True,string="Facture",readonly=True,states={'draft':[('readonly',False)]}),
        'taux': fields.float('Taux Douane',required=True, digits_compute= dp.get_precision('Payment Term'),readonly=True,states={'draft':[('readonly',False)]}),
        'marge_max': fields.many2one('marge.produit','Marge Max',required=True, digits_compute= dp.get_precision('Account'),readonly=True,states={'draft':[('readonly',False)]}),
        'marge_min': fields.many2one('marge.produit','Marge Min',required=True, digits_compute= dp.get_precision('Account'), readonly=True,states={'draft':[('readonly',False)]}),
        'amount_invoice_euro': fields.float('Montant Facture €', readonly=True, digits_compute= dp.get_precision('Account')),
        'amount_invoice_DT': fields.float('Montant Facture DT', readonly=True, digits_compute= dp.get_precision('Account')),
        'importation_lines': fields.one2many('importation.produit.line', 'importation_id', ' ',readonly=True,states={'draft':[('readonly',False)]}),        	'amount_total_euro':fields.float(string='Total €', digits_compute=dp.get_precision('Account'),
        store=True, readonly=True, compute='_amount_all', track_visibility='always'),
	'amount_total_dt':fields.float(string='Total DT', digits_compute=dp.get_precision('Account'),
        store=True, readonly=True, compute='_amount_all', track_visibility='always'),
        'charges_importation_lines': fields.one2many('charge.importation.produit.line', 'importation_id', ' '),       
	'amount_total_chrage_dt':fields.float(string='Total Charges DT', digits_compute=dp.get_precision('Account'),
        store=True, readonly=True, compute='_amount_all', track_visibility='always'),
        'categ_lines': fields.one2many('importation.produit.categ', 'importation_id'," "),   
	'amount_total_DD':fields.float(string='Total DD DT', digits_compute=dp.get_precision('Account'),
        store=True, readonly=True, compute='_amount_all', track_visibility='always'),    




    }
    _defaults = {
    	'state': 'draft',
    }

	
		
		
    def confirmer_homologation(self, cr, uid, ids, context):
    	##mettre a jour coeff rev du categorie
    	imporation_obj=self.browse(cr, uid, ids)
    	for line in imporation_obj.categ_lines:
    		#line.name.id
    		import_lines_ids=self.pool.get('importation.produit.line').search(cr, uid, [('importation_id','=',ids[0]),('categ_id','=',line.name.id)])
    		import_lines=self.pool.get('importation.produit.line').browse(cr, uid,import_lines_ids)
    		for line_impo in import_lines:
    			coeff=line_impo.coeff_rev
    		self.pool.get('product.category.douane').write(cr, uid, line.name.id,{ 'coeff_rev': coeff  })
    	self.write(cr, uid, ids,{ 'state': 'confirm'  })
    	return True
    def brouillon(self, cr, uid, ids, context):
    	self.write(cr, uid, ids,{ 'state': 'draft'  })
    	return True

    def button_calcul_categ(self, cr, uid, ids, context=None):

		imporation_obj=self.browse(cr, uid, ids)

		categ_ids = self.pool.get('product.category.douane').search(cr, uid, [])
		categ_obj = self.pool.get('product.category.douane').browse(cr, uid,categ_ids)
		if imporation_obj.categ_lines:
			for line in imporation_obj.categ_lines:
				self.pool.get('importation.produit.categ').unlink(cr, uid, line.id)

		if categ_obj :
			for categ in categ_obj:


				import_lines_ids=self.pool.get('importation.produit.line').search(cr, uid, [('importation_id','=',ids[0]),('categ_id','=',categ.id)])
				import_lines=self.pool.get('importation.produit.line').browse(cr, uid,import_lines_ids)
				if import_lines:
					montant_total_categ=0.0
					i=0
					while(i<5):
						if categ.category_lines[i]['frais_id'].name=="001":
							taux_1=categ.category_lines[i]['taux']
						if categ.category_lines[i]['frais_id'].name=="093":
							taux_2=categ.category_lines[i]['taux']
						if categ.category_lines[i]['frais_id'].name=="473":
							taux_3=categ.category_lines[i]['taux']
						if categ.category_lines[i]['frais_id'].name=="105":
							taux_4=categ.category_lines[i]['taux']
						if categ.category_lines[i]['frais_id'].name=="AIR":
							taux_5=categ.category_lines[i]['taux']
						i+=1
					for line in import_lines:

						montant_total_categ+=line.price_subtotal_dt
					#total=(montant_total_categ*categ.category_lines[0]['taux'])+(montant_total_categ*categ.category_lines[1]['taux'])+(montant_total_categ*categ.category_lines[2]['taux'])+(montant_total_categ*categ.category_lines[4]['taux'])
					for line in import_lines:
						#line.categ_id.id
						taux_DD= line.price_subtotal_dt / montant_total_categ

						FF=line.taux_FF*imporation_obj.amount_total_chrage_dt

						self.pool.get('importation.produit.line').write(cr, uid, line.id,{ 'taux_DD': taux_DD, 'FF':FF  })
					val={
						'name':categ.id,
						'taux_1':taux_1,
						'taux_2':taux_2,
						'taux_3':taux_3,
						'taux_4':taux_4,
						'taux_5':taux_5,
						'total':0.0,
						'importation_id':ids[0],
					}
					inv_id=self.pool.get('importation.produit.categ').create(cr,uid,val)






    def button_add_invoice(self, cr, uid, ids, context=None):
	 
		##ligne facture
		imporation_obj=self.browse(cr, uid, ids)
		print "*****************",imporation_obj.facture_id.id
		if not imporation_obj.taux :
			raise osv.except_osv(('Taux erroné'), ('Veuillez mentionner le Taux '))
		for invoice in self.pool.get('account.invoice').browse(cr, uid,imporation_obj.facture_id.id):
			amount_invoice_euro=invoice.amount_total
			amount_invoice_DT=amount_invoice_euro*imporation_obj.taux
		self.write(cr, uid, ids,{ 'amount_invoice_euro': amount_invoice_euro,'amount_invoice_DT': amount_invoice_DT,})
		invoice_lines_id = self.pool.get('account.invoice.line').search(cr, uid, [('invoice_id', '=', imporation_obj.facture_id.id)])
		invoice_lines_obj = self.pool.get('account.invoice.line').browse(cr, uid,invoice_lines_id)
		for line in invoice_lines_obj:
			product=self.pool.get('product.template').browse(cr, uid,line.product_id.id)
			print "categorieeeee====",product.categ_douane.id
			#if product.categ_douane.id:
			val={
				'product_id':line.product_id.id,
				'categ_id':product.categ_douane.id,
				'designation':line.name,
				'price_unit':line.price_unit,
				'product_qty':line.quantity,
				'price_subtotal_euro':line.price_subtotal,
				'price_subtotal_dt':line.price_subtotal * imporation_obj.taux,
				'taux_FF':(line.price_subtotal * imporation_obj.taux)/imporation_obj.amount_invoice_DT,
				'importation_id':ids[0],

			}
			#else :


			inv_id=self.pool.get('importation.produit.line').create(cr,uid,val)
		## ligne des frais fixes		
		charge_ids=self.pool.get('charge.importation.produit').search(cr, uid, [], context=context)
		charge_obj=self.pool.get('charge.importation.produit').browse(cr, uid, charge_ids)
		if charge_obj:
			for charge in charge_obj:
				val={
					'importation_id':ids[0],
					'charge_id':charge.id,
					'amount_charge':0.0
				}
				
				inv_id=self.pool.get('charge.importation.produit.line').create(cr,uid,val)


importation_produit()


class importation_produit_line(osv.osv):
    _name = "importation.produit.line"
    _description = "Importation Produit Line"



    @api.one
    @api.depends('price_unit','product_qty','product_id', 'importation_id.taux','importation_id.categ_lines.total' )#, 'devis_id.currency_id')'importation_id.amount_total_chrage_dt'
    def _amount_line(self):
        '''
           Methode qui permet de calculer le sous total d'une ligne
        '''
        if self.importation_id.taux:
		
		    #taxes = self.tax_ids.compute_all(price, self.product_qty, product=self.product_id, partner=self.devis_id.partner_id)
		    self.price_subtotal_euro = self.price_unit * self.product_qty
		    self.price_subtotal_dt = self.price_subtotal_euro * self.importation_id.taux
		    #print "000000",self.importation_id.currency_id.rate_silent
		    #self.FF=self.importation_id.amount_total_chrage_dt*self.taux_FF
		    total=0.0

		    for categ in self.importation_id.categ_lines:

		    	if categ.name.id==self.categ_id.id:
		    		print "daaaaaaaaaaans ifff categ egaux"
		    		total=categ.total
		    self.DD=self.taux_DD*total
		    self.price_subtotal_revient_dt=self.price_subtotal_dt+self.DD+self.FF
		    self.price_unit_revient_dt=self.price_subtotal_revient_dt / self.product_qty
		    self.marge_min=self.price_unit_revient_dt * self.importation_id.marge_min.taux
		    self.marge_max=self.price_unit_revient_dt * self.importation_id.marge_max.taux
		    self.coeff_rev=self.price_unit_revient_dt / self.price_unit

		
    @api.one
    @api.depends('importation_id.amount_total_chrage_dt')
    def _amount_FF(self):
    	self.FF=self.importation_id.amount_total_chrage_dt*self.taux_FF

	@api.one
	@api.depends('importation_id.categ_lines.total',)
	def _amount_DD(self):
		total=0.0
		for categ in self.importation_id.categ_lines:
			if categ.name.id==self.categ_id.id:
				print "daaaaaaaaaaans ifff categ egaux"
				total=categ.total
		self.DD=self.taux_DD*total

    _columns = {

        'importation_id' : fields.many2one('importation.produit' , 'Importation Produit' , ondelete='cascade'),
        'categ_id' : fields.many2one('product.category.douane' , 'NGP' ,  ),
        #'state': fields.selection([('draft', 'Brouillon'),('confirm', 'Confirmé') ],),
        'product_id': fields.many2one('product.product', 'Produit', ondelete='restrict',),
        'designation': fields.char('Désignation ',),
        'taux_FF': fields.float('% FF', digits_compute= dp.get_precision('Account'),),
        'taux_DD': fields.float('% DD', digits_compute= dp.get_precision('Account'),),
        'FF': fields.float('F Fixes', digits_compute= dp.get_precision('Account'),),#compute='_amount_FF',
        'DD': fields.float(string='DD', digits_compute= dp.get_precision('Account'),
        store=True,),#compute='_amount_DD'
        'price_unit': fields.float('PU €', digits_compute= dp.get_precision('Account'),readonly=True,),
        'product_qty': fields.float('Qté',digits_compute= dp.get_precision('Discount'),readonly=True,),
        'price_subtotal_dt': fields.float('Prix Total DT', digits_compute= dp.get_precision('Account'),store=True, readonly=True, compute='_amount_line'),
        'price_subtotal_revient_dt': fields.float('Prix Total Revient', digits_compute= dp.get_precision('Account'),store=True, readonly=True, compute='_amount_line'),
        'price_unit_revient_dt': fields.float('Prix U revient', digits_compute= dp.get_precision('Account'),readonly=True,compute='_amount_line'),
        'marge_min': fields.float('Marge Min', digits_compute= dp.get_precision('Account'),readonly=True,compute='_amount_line'),
        'marge_max': fields.float('Marge Max', digits_compute= dp.get_precision('Account'),readonly=True,compute='_amount_line'),
        'coeff_rev': fields.float('Coeff rev', digits_compute= dp.get_precision('Account'),readonly=True,compute='_amount_line'),
        'price_subtotal_euro':fields.float(string='Prix Total €', digits_compute= dp.get_precision('Account'),
        store=True, readonly=True, compute='_amount_line'),


    }


    _defaults = {
        'product_qty': lambda *a: 1.00,

        'price_unit': lambda *a:  0.0,
    }


    def product_id_change(self, cr, uid, ids, product,  context=None):

	res_final = {}
        if product:
            #les informations sur le produit
            product_obj = self.pool.get('product.product').browse(cr,uid,product,context=context)

            product_categ_obj = self.pool.get('product.category').browse(cr,uid,product_obj.categ_id.id,context=context)
            

            designation=product_obj.name_template
            if product_obj.categ_douane.id:

            	res_final = {'value':{'designation':designation ,'categ_id':product_obj.categ_douane.id}}
            else :
            	res_final = {'value':{'designation':designation ,}}
        return res_final


importation_produit_line()

class charge_importation_produit(osv.osv):

    _name = "charge.importation.produit"
    _description = "Charge Importation Produit"


    _columns = {

        'name' : fields.char("Name" ,required=True),





    }
charge_importation_produit()

class importation_produit_categ(osv.osv):

    _name = "importation.produit.categ"
    _description = "importation produit par categ"





    _columns = {

        'importation_id' : fields.many2one('importation.produit' , 'Homologation' , ondelete='cascade',readonly=True),
        'name' : fields.many2one('product.category.douane',"Catégorie" ,required=True),
        'taux_1' : fields.float('001' ,required=True,digits_compute= dp.get_precision('Account')),
        'taux_2' : fields.float('093' ,required=True,digits_compute= dp.get_precision('Account')),
        'taux_3' : fields.float('473' ,required=True,digits_compute= dp.get_precision('Account')),
        'taux_4' : fields.float('105' ,required=True,digits_compute= dp.get_precision('Account')),
        'taux_5' : fields.float('AIR' ,digits_compute= dp.get_precision('Account')),
        'total' : fields.float(string='Total', digits_compute= dp.get_precision('Account')),




    }




importation_produit_categ()



class frais_var_produit(osv.osv):

    _name = "frais.var.produit"
    _description = "Frais Variable Importation Produit"


    _columns = {

        'name' : fields.char('Name' ,required=True),
        #'taux' : fields.float('Taux Douane' ,required=True),





    }
frais_var_produit()

class marge_produit(osv.osv):
    _name = "marge.produit"
    _description = "Les marges Max et Min des Produits"
    
    
    
    _columns = {
    	'name' : fields.char('Name' ,required=True),
    	'taux' : fields.float('Taux ' ,required=True),
    }
    
    
    
    

marge_produit()

class charge_importation_produit_line(osv.osv):
    _name = "charge.importation.produit.line"
    _description = "Charge Importation Produit"



    _columns = {
        'importation_id' : fields.many2one('importation.produit' , 'Importation Produit' , ondelete='cascade'),
        'charge_id' : fields.many2one('charge.importation.produit' ,'Type Charge'),
        'amount_charge': fields.float('Montant', digits_compute= dp.get_precision('Account')),


    }
    _defaults = {
		"importation_id": lambda self, cr, uid, c: c.get('importation_id', False),
	}
charge_importation_produit_line()


