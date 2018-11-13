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

import string
import re
from openerp.osv import osv, fields, expression
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp import api
class product_product(osv.osv):

    #def calculer_prix(self, cr, uid, ids, context={}):
    #    result = {}
    #    price=0.00
    #    cr.execute("""SELECT product_tmpl_id
#		      FROM  product_product
#		      where
#		      product_product.id=%s
#		      """,(ids[0],))
#        id_tmp = cr.dictfetchone()['product_tmpl_id']
#        cr.execute("""SELECT Avg(prix * (1 - supplier_discount * 0.01)) AS avg_price
#		      FROM product_supplierinfo, product_product
#		      WHERE
#		      product_product.product_tmpl_id = product_supplierinfo.product_id and
#		      product_supplierinfo.product_id=%s
#                      GROUP BY product_supplierinfo.product_id
#		      """,(id_tmp,)) 
#        line = cr.dictfetchone()
#        if line :
#	    price=line['avg_price']
#	    result['standard_price'] = price
#	    product_template_obj = self.pool.get('product.template')
#	    product_template_obj.write(cr, uid, id_tmp, {'standard_price':price}, context=context)
#        return {'value': result}

    _name = 'product.product'
    _inherit = 'product.product'
    _columns = {
        #rim modif 14/04/2014
        #'fodec':fields.boolean('FODEC'), 
    }
product_product()


class product_supplierinfo(osv.osv):

    @api.one
    #@api.depends('price_unit', 'discount', 'tax_ids', 'product_qty',
        #'product_id', 'devis_id.partner_id')#, 'devis_id.currency_id')
    @api.depends('prix', 'rate','currency_id')#, 'devis_id.currency_id')
    def _amount_line(self):
        '''
           Methode qui permet de calculer le sous total d'une ligne de devis
        '''
	if self.currency_id:
		
		#taxes = self.tax_ids.compute_all(price, self.product_qty, product=self.product_id, partner=self.devis_id.partner_id)
		self.price_subtotal = self.prix / self.rate

    _name = 'product.supplierinfo'
    _inherit = 'product.supplierinfo'
    _columns = {
        'prix': fields.float('Prix',digits_compute=dp.get_precision('Account'), required=True),
        'currency_id': fields.many2one('res.currency', 'Currency', required=True),
        'supplier_discount':fields.float('Remise'),
        'price_subtotal': fields.float(string='Prix Monnaie Locale', digits= dp.get_precision('Account'),
        store=True, compute='_amount_line'),
	'rate': fields.float('rate',digits_compute=dp.get_precision('Account')), 

     
    }

    def currency_id_change(self, cr, uid, ids, currency, context=None):

	res_final = {}
	if currency:
		    #les informations sur le produit
		currency_obj = self.pool.get('res.currency').browse(cr,uid,currency,context=context)
		print "raaaaaaaaaaaate : =====",currency_obj.rate_silent
		    #designation=product_obj.name_template
		rate = currency_obj.rate_silent
		    #les informations sur les taxes du produit
		    #taxes = self.pool.get('product.product').browse(cr,uid,product,context=context)

		res_final = {'value':{'rate':rate}}
	return res_final

product_supplierinfo()


class product_template(osv.osv):

    _name = 'product.template'
    _inherit = 'product.template'
    _columns = {
        'affichage': fields.boolean('Pour affichage'), 
	'purchase_price': fields.float('Purchase Price', digits_compute=dp.get_precision('Product Price')),       
    }
    _defaults = {
        'purchase_price': 1,
    }
product_template()



    
