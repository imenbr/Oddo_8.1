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
import openerp.addons.decimal_precision as dp

from openerp.osv import fields, osv

from openerp.tools.translate import _
from datetime import date, datetime
import time
from dateutil import relativedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from openerp import SUPERUSER_ID, api
from openerp.tools.float_utils import float_compare, float_round

class stock_picking(osv.osv):

    _name = 'stock.picking'
    _inherit = 'stock.picking'
    
    def _get_picking_tax(self, cr, uid, ids, context=None):                         
        result = {}
        for tax in self.pool.get('stock.picking.tax').browse(cr, uid, ids, context=context):
            result[tax.picking_id.id] = True           

        return result.keys() 

    def _get_move(self, cr, uid, ids, context=None):            
        result = {}
        for line in self.pool.get('stock.move').browse(cr, uid, ids, context=context):
            result[line.picking_id.id] = True             
        return result.keys()

    def _amount_all(self, cr, uid, ids, name, args, context=None): 
        '''
           Methode qui calcule et retourne les montants suivants
           @return:amount_untaxed
           @return:amount_tax
           @return:amount_total
           @return:undiscount_total
           @return:discount_total
           
        '''        
        res = {}                 
        for pick in self.browse(cr, uid, ids, context=context):
            res[pick.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
                'undiscount_total': 0.0,
                'discount_total': 0.0,
            }

            for line in pick.move_lines:
                res[pick.id]['amount_untaxed'] += line.price_subtotal
                res[pick.id]['discount_total'] += line.product_qty * line.price_unit * ((line.discount or 0.0)/100.0)
                res[pick.id]['undiscount_total'] += line.product_qty * line.price_unit
               
            for line in pick.tax_line:
                res[pick.id]['amount_tax'] += line.amount
            
            res[pick.id]['amount_total'] = res[pick.id]['amount_tax'] + res[pick.id]['amount_untaxed']
            return res

    _columns = {    
        #'purchase_id': fields.many2one('purchase.order', 'Commande',states={'done':[('readonly',True)]},),
        #'do_filter':fields.boolean('Filtrer les produits selon BC'),
        
        'discount_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'),method=True, string='Total Remise',
            store=True,
            multi='all'),
        'undiscount_total': fields.function(_amount_all, method=True, digits_compute=dp.get_precision('Account'), string='Total HT',
            store=True,
            multi='all'),
        'amount_untaxed': fields.function(_amount_all, method=True, digits_compute=dp.get_precision('Account'), string='Untaxed',
            store={
                 'stock.picking': (lambda self, cr, uid, ids, c={}: ids, ['move_lines'], 20),
                 'stock.picking.tax': (_get_picking_tax, None, 20),
                 'stock.move': (_get_move, ['price_unit','move_tax_id','quantity','discount','picking_id'], 20),
            },
            multi='all'),
        'amount_tax': fields.function(_amount_all, method=True, digits_compute=dp.get_precision('Account'), string='Tax',
            store={
                'stock.picking': (lambda self, cr, uid, ids, c={}: ids, ['move_lines'], 20),
                'stock.picking.tax': (_get_picking_tax, None, 20),
                'stock.move': (_get_move, ['price_unit','move_tax_id','quantity','discount','picking_id'], 20),
            },
            multi='all'),
        'amount_total': fields.function(_amount_all, method=True, digits_compute=dp.get_precision('Account'), string='Total',
            store={
                'stock.picking': (lambda self, cr, uid, ids, c={}: ids, ['move_lines'], 20),
                'stock.picking.tax': (_get_picking_tax, None, 20),
                'stock.move': (_get_move, ['price_unit','move_tax_id','quantity','discount','picking_id'], 20),
            },
            multi='all'),

        'account_id': fields.many2one('account.account', 'Account', readonly=True, states={'draft':[('readonly',False)]}, help="The partner account used for this invoice."),
        'tax_line': fields.one2many('stock.picking.tax', 'picking_id', 'Tax Lines', readonly=True, states={'draft':[('readonly',False)]}),
        #TODO à vérifier ces 2 champs s ils sont necessaires
        'number_invoice': fields.char('Code Facture', size=32, help="Unique number of the invoice"),
        'internal_number_invoice': fields.char('Numéro', size=32,readonly=True,states={'draft':[('readonly',False)]}, help="Unique number of the invoice"),
        #'invoice_state': fields.selection([
        #    ("invoiced", "Invoiced"),
        #    ("2binvoiced", "To Be Invoiced"),
        #    ("none", "Not Applicable")], "Invoice Control",
        #     readonly=True),
    }

    _defaults = {
        #'invoice_state': '2binvoiced',
    }

    #def onchange_filter(self, cr, uid, ids, do_filter, purchase_id, context=None):
    #    if (do_filter == True and purchase_id != False):
    #        #maj du domain
    #        cr.execute("select * from purchase_order_line where order_id = %s",(purchase_id,))
    #        products = cr.dictfetchall() 
    #        if len(products) != 0:
    #            if len(products) == 1:
    #                for product in products:
    #                    pick = "('id','=',"+str(product['product_id'])+")"   
    #            else : 
    #                pick='('
    #                for product in products:
    #                    pick=pick+str(product['product_id'])+','
    #                pick = pick[:-1]
    #                pick=pick+')'
    #                pick = "('id','in',"+pick+")"
    #        else :  
    #            pick = "('id','=',0)"
    #        return {'value':{'product_domain': pick}}
    #    return {'value':{'product_domain': "('id','>',0)"}}    

    @api.cr_uid_ids_context
    def do_enter_transfer_details(self, cr, uid, picking, context=None):
        '''
           Modifier la methode pour mettre à jour les taxes
        '''
        if not context:
            context = {}

        context.update({
            'active_model': self._name,
            'active_ids': picking,
            'active_id': len(picking) and picking[0] or False
        })

        created_id = self.pool['stock.transfer_details'].create(cr, uid, {'picking_id': len(picking) and picking[0] or False}, context)
        #rimbd
        self.reset_taxes(cr, uid, picking, context)
        return self.pool['stock.transfer_details'].wizard_view(cr, uid, created_id, context)

    def button_reset_taxes(self, cr, uid, ids, context=None):           
        self.reset_taxes(cr, uid, ids, context)
        return True

    def reset_taxes(self, cr, uid, ids, context=None):            
        val = self.pool.get('stock.picking').browse(cr, uid, ids[0]).name
        if context is None:
            context = {}
        ctx = context.copy()
        ait_obj = self.pool.get('stock.picking.tax')
        for id in ids:
            partner = self.browse(cr, uid, id, context=ctx).partner_id
            if partner.lang:
               cr.execute("DELETE FROM stock_picking_tax WHERE picking_id=%s AND manual is False", (id,))
               ctx.update({'lang': partner.lang})
            for taxe in ait_obj.compute(cr, uid, id, context=ctx).values():
                ait_obj.create(cr, uid, taxe)  
        # Update the stored value (fields.function), so we write to trigger recompute
        self.pool.get('stock.picking').write(cr, uid, ids, {'move_lines':[]}, context=ctx)
	self.pool.get('stock.picking').write(cr, uid, ids, {'state':'draft'}, context=ctx) #   29/07 modification etat du bon reception cree a partir du purchase order        
        return True

class stock_move(osv.osv):
    _name = 'stock.move'
    _inherit = 'stock.move'

    def _amount_line(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        res = {}
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        for line in self.browse(cr, uid, ids):
            
            price = line.price_unit * (1-(line.discount or 0.0)/100.0)
            taxes = line.move_tax_id.compute_all(price, line.product_uom_qty, product=line.product_id, partner=line.picking_id.partner_id)
            
            res[line.id] = taxes['total']
            #if line.picking_id:
            #   cur = line.picking_id.currency_id
   
        #if self.invoice_id:
        #    self.price_subtotal = self.invoice_id.currency_id.round(self.price_subtotal)
            
        return res

    #def create(self, cr, uid, vals, context=None):
    #    origin = vals['origin']
    #    po_object = self.pool.get('purchase.order')
    #    po_ids = po_object.search(cr, uid, [('name', '=', origin)], context=context)
    #    print 'po_ids!!!!!!!!!!!!!!!!',po_ids
    #    picking_id = self.pool.get('stock.picking').browse(cr, uid,vals['picking_id'], context=context)
    #    print 'picking_id!!!!!!!!!!!!!!!!',picking_id
    #    if (len(po_ids) > 0):
    #        purchase_id = po_ids[0]
    #        po = po_object.browse(cr, uid, purchase_id, context=context)
    #        cr.execute('''SELECT purchase_order_line.id as pol_id FROM purchase_order, purchase_order_line WHERE purchase_order.id = purchase_order_line.order_id
    #    AND purchase_order.id =%s
    #    AND purchase_order_line.product_id=%s
    #    ''',(purchase_id,vals['product_id'],))
    #        do_filter = picking_id.do_filter
    #        result = cr.dictfetchone()
    #        print 'result!!!!!!!!!!!!!!!!',result
    #        if result:
                
    #            purchase_line_id = result['pol_id']
    #            if (do_filter != False and purchase_id != False and vals['purchase_line_id'] == False):
    #                vals['purchase_line_id'] = result['pol_id']         
        
    #    res = super(stock_move, self).create(cr, uid, vals, context)
    #    return res 

    _columns = {
        'price_unit': fields.float('Prix unitaire', digits_compute= dp.get_precision('Account'), help="Technical field used to record the product cost set by the user during a picking confirmation (when average price costing method is used)"),
        #'product_reste_qty':fields.float('Qte Non Livrée', digits_compute= dp.get_precision('Account')),  
        #'product_order_qty':fields.float('Qte Commandee', digits_compute= dp.get_precision('Account')),
        'price_subtotal':fields.function(_amount_line,method=True,digits_compute=dp.get_precision('Account'), string='Sous total', type="float", store=True,),
        'discount': fields.float('Remise',digits=(16,2)),
        'move_tax_id': fields.many2many('account.tax', 'stock_move_tax', 'move_id', 'tax_id', 'Taxes', domain=[('parent_id','=',False)]),
        'account_id': fields.many2one('account.account', 'Account', domain=[('type','<>','view'), ('type', '<>', 'closed')], help="The income or expense account related to the selected product."),
        'default_code' : fields.char('Reference', size=64),
        #'prod_qty_stock':fields.float('Qte Disponible', digits_compute= dp.get_precision('Account')),
        
    }

    def onchange_product_id(self, cr, uid, ids, prod_id=False, loc_id=False, loc_dest_id=False, partner_id=False):#,purchase_order=False,bc_filter = False):
        
        """
        Modifier cette methode pour prendre en considération les propositions de (prix, remise) fournisseurs 
        On change of product id, if finds UoM, UoS, quantity and UoS quantity.
        @param prod_id: Changed Product id
        @param loc_id: Source location id
        @param loc_dest_id: Destination location id
        @param partner_id: Address id of partner
        @return: Dictionary of values
        """
        if not prod_id:
            return {}
        user = self.pool.get('res.users').browse(cr, uid, uid)
        lang = user and user.lang or False
        if partner_id:
            addr_rec = self.pool.get('res.partner').browse(cr, uid, partner_id)
            if addr_rec:
                lang = addr_rec and addr_rec.lang or False
        ctx = {'lang': lang}

        product = self.pool.get('product.product').browse(cr, uid, [prod_id], context=ctx)[0]
        uos_id = product.uos_id and product.uos_id.id or False
        #result = {
        #    'name': product.partner_ref,
        #    'product_uom': product.uom_id.id,
        #    'product_uos': uos_id,
        #    'product_uom_qty': 1.00,
        #    'product_uos_qty': self.pool.get('stock.move').onchange_quantity(cr, uid, ids, prod_id, 1.00, product.uom_id.id, uos_id)['value']['product_uos_qty'],
        #}
        #if loc_id:
        #    result['location_id'] = loc_id
        #if loc_dest_id:
        #    result['location_dest_id'] = loc_dest_id

        #rimbd
        if type == 2:
           taxes =  product.taxes_id
        else:
           taxes =  product.supplier_taxes_id
        fposition_id = False
        fpos_obj = self.pool.get('account.fiscal.position')
        fpos = fposition_id and fpos_obj.browse(cr, uid, fposition_id, context=context) or False
        tax_id = fpos_obj.map_tax(cr, uid, fpos, taxes)
        #product_reste_qty = 0
        #product_order_qty = 0
        price = 0
        remise = 0
        
        if prod_id != False:
            cr.execute("""
                      SELECT prix,supplier_discount
		      FROM product_supplierinfo, product_product
		      WHERE 
		      product_product.product_tmpl_id = product_supplierinfo.product_tmpl_id 
		      AND product_supplierinfo.name=%s AND product_product.id=%s 
		      """,(partner_id,prod_id))
            line = cr.dictfetchone()
            if line :
	        price=line['prix'] 
                remise=line['supplier_discount']  
   
        result = {
            'name': product.partner_ref,
	    'default_code':product.default_code,
            'product_uom': product.uom_id.id,
            'product_uom_qty': 1.00,
            'product_uos': uos_id,
            'move_tax_id': tax_id,
            'product_qty': 1.00,
            'product_uos_qty' : self.pool.get('stock.move').onchange_quantity(cr, uid, ids, prod_id, 1.00, product.uom_id.id, uos_id)['value']['product_uos_qty'],
            #'product_reste_qty': product_reste_qty,
            #'product_order_qty': product_order_qty,
            'price_unit': price,
	    'discount':remise,
        }   
        if loc_id:
            result['location_id'] = loc_id
        if loc_dest_id:
            result['location_dest_id'] = loc_dest_id         
        return {'value': result}

    def attribute_price(self, cr, uid, move, context=None):
        """
            Attribute price to move, important in inter-company moves or receipts with only one partner
            Modifier cette methode pour mettre à jour le prix, la remise et les taxes 
            à partir des BC dans le cas du BC vente
        """
        if not move.price_unit:
            #If type is out (Bon de livraison)
            if move.picking_type_id.id == 2:
                sale_order = self.pool.get('sale.order').search(cr, uid, [('name', '=', move.origin)], context=context)
                
                sale_line = self.pool.get('sale.order.line').search(cr, uid, [('order_id', '=', sale_order[0]),('product_id','=',move.product_id.id)], context=context)
                
                sale = self.pool.get('sale.order.line').browse(cr, uid, sale_line[0])
                price = sale.price_unit
                discount = sale.discount
                self.write(cr, uid, [move.id], {'price_unit': price,'discount':discount,'move_tax_id':[(6, 0, [x.id for x in sale.tax_id])]})
            else:
                price = move.product_id.standard_price
                self.write(cr, uid, [move.id], {'price_unit': price})

class stock_picking_tax(osv.osv):
    _name = "stock.picking.tax"
    _description = "Picking Tax"

    def _count_factor(self, cr, uid, ids, name, args, context=None):
        res = {}
        for picking_tax in self.browse(cr, uid, ids, context=context):
            res[picking_tax.id] = {
                'factor_base': 1.0,
                'factor_tax': 1.0,
            }
            if picking_tax.amount <> 0.0:
                factor_tax = picking_tax.tax_amount / picking_tax.amount
                res[picking_tax.id]['factor_tax'] = factor_tax

            if picking_tax.base <> 0.0:
                factor_base = picking_tax.base_amount / picking_tax.base
                res[picking_tax.id]['factor_base'] = factor_base
        return res

    _columns = {
        'picking_id': fields.many2one('stock.picking', 'Move', ondelete='cascade', select=True),
        'name': fields.char('Tax Description', size=64, required=True),
        'account_id': fields.many2one('account.account', 'Tax Account', required=True, domain=[('type','<>','view'),('type','<>','income'), ('type', '<>', 'closed')]),
        'base': fields.float('Base', digits_compute=dp.get_precision('Account')),
        'amount': fields.float('Amount', digits_compute=dp.get_precision('Account')),
        'manual': fields.boolean('Manual'),
        'sequence': fields.integer('Sequence', help="Gives the sequence order when displaying a list of invoice tax."),
        'base_code_id': fields.many2one('account.tax.code', 'Base Code', help="The account basis of the tax declaration."),
        'base_amount': fields.float('Base Code Amount', digits_compute=dp.get_precision('Account')),
        'tax_code_id': fields.many2one('account.tax.code', 'Tax Code', help="The tax basis of the tax declaration."),
        'tax_amount': fields.float('Tax Code Amount', digits_compute=dp.get_precision('Account')),
        'company_id': fields.related('account_id', 'company_id', type='many2one', relation='res.company', string='Company', store=True, readonly=True),
        'factor_base': fields.function(_count_factor, method=True, string='Multipication factor for Base code', type='float', multi="all"),
        'factor_tax': fields.function(_count_factor, method=True, string='Multipication factor Tax code', type='float', multi="all")
    }

    def base_change(self, cr, uid, ids, base, currency_id=False, company_id=False, date_picking=False):
        cur_obj = self.pool.get('res.currency')
        company_obj = self.pool.get('res.company')
        company_currency = False
        factor = 1
        if ids:
            factor = self.read(cr, uid, ids[0], ['factor_base'])['factor_base']
        if company_id:
            company_currency = company_obj.read(cr, uid, [company_id], ['currency_id'])[0]['currency_id'][0]
        if currency_id and company_currency:
            base = cur_obj.compute(cr, uid, currency_id, company_currency, base*factor, context={'date': date_picking or time.strftime('%Y-%m-%d')}, round=False)
        return {'value': {'base_amount':base}}

    def amount_change(self, cr, uid, ids, amount, currency_id=False, company_id=False, date_picking=False):
        cur_obj = self.pool.get('res.currency')
        company_obj = self.pool.get('res.company')
        company_currency = False
        factor = 1
        if ids:
            factor = self.read(cr, uid, ids[0], ['factor_tax'])['factor_tax']
        if company_id:
            company_currency = company_obj.read(cr, uid, [company_id], ['currency_id'])[0]['currency_id'][0]
        if currency_id and company_currency:
            amount = cur_obj.compute(cr, uid, currency_id, company_currency, amount*factor, context={'date': date_picking or time.strftime('%Y-%m-%d')}, round=False)
        return {'value': {'tax_amount': amount}}

    _order = 'sequence'
    _defaults = {
        'manual': 1,
        'base_amount': 0.0,
        'tax_amount': 0.0,
    }

    def compute(self, cr, uid, picking_id, context=None):           
        tax_grouped = {}
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        picking = self.pool.get('stock.picking').browse(cr, uid, picking_id, context=context)
        #cur = picking.currency_id
        company_currency = picking.company_id.currency_id.id

        for line in picking.move_lines:
            prod = self.pool.get('product.product').browse(cr, uid, line.product_id, context=context)
            price=line.price_unit* (1-(line.discount or 0.0)/100.0)
            for tax in tax_obj.compute_all(cr, uid, line.move_tax_id, price, line.product_qty, line.product_id, picking.partner_id)['taxes']:
                val={}
                val['picking_id'] = picking.id
                val['name'] = tax['name'][-5:].replace('-','')
                val['amount'] = tax['amount']
                val['manual'] = False
                val['sequence'] = tax['sequence']
                val['base'] = tax['price_unit'] * line['product_qty']

                if picking.picking_type_id in (1,2):
                    val['base_code_id'] = tax['base_code_id']
                    val['tax_code_id'] = tax['tax_code_id']
                    
                    val['base_amount'] = cur_obj.compute(cr, uid, company_currency, company_currency, val['base'] * tax['base_sign'], context={'date': picking.date or time.strftime('%Y-%m-%d')}, round=False)
                    
                    val['tax_amount'] = cur_obj.compute(cr, uid, company_currency, company_currency, val['amount'] * tax['tax_sign'], context={'date': picking.date or time.strftime('%Y-%m-%d')}, round=False)
                    val['account_id'] = tax['account_collected_id'] or line.account_id.id
                else:
                    val['base_code_id'] = tax['ref_base_code_id']
                    val['tax_code_id'] = tax['ref_tax_code_id']
                    
                    val['base_amount'] = cur_obj.compute(cr, uid, company_currency, company_currency, val['base'] * tax['ref_base_sign'], context={'date': picking.date or time.strftime('%Y-%m-%d')}, round=False)
                    
                    val['tax_amount'] = cur_obj.compute(cr, uid, company_currency, company_currency, val['amount'] * tax['ref_tax_sign'], context={'date': picking.date or time.strftime('%Y-%m-%d')}, round=False)
                    val['account_id'] = tax['account_paid_id'] or line.account_id.id

                key = (val['tax_code_id'], val['base_code_id'], val['account_id'])
                if not key in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base'] += val['base']
                    tax_grouped[key]['base_amount'] += val['base_amount']
                    tax_grouped[key]['tax_amount'] += val['tax_amount']

        return tax_grouped

stock_picking_tax()

class stock_inventory(osv.osv):
    
    _name = "stock.inventory"
    _inherit = "stock.inventory"
 
    #def create(self, cr, uid, vals, context=None):
    #   '''
    #      Add inventory reference sequence
    #      @return: new created stock_inventory id
    #   '''
    #   vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'stock.inventory.sequence')
    #   return super(stock_inventory, self).create(cr, uid, vals, context)

    _columns = {
        'name': fields.char('Inventory Reference', size=64, readonly=True),
    }

class stock_inventory_line(osv.osv):

    _name = "stock.inventory.line"
    _inherit = "stock.inventory.line"

    def _quantity_compute(self, cr, uid, ids, field, args, context=None,):
        '''
           Calculer l'écart entre la quantité théorique et la quentité réelle
        '''
	res = {}
	for inv_obj in self.browse(cr,uid,ids,context=context):
            if (inv_obj.theoretical_qty - inv_obj.product_qty) >= 0:
                quantity_difference = inv_obj.theoretical_qty - inv_obj.product_qty
            else:
                quantity_difference = inv_obj.product_qty - inv_obj.theoretical_qty
        	
        res[inv_obj.id] = quantity_difference
	return res

    @api.onchange('product_qty') 
    def check_product_qty_change(self):
         if (self.theoretical_qty - self.product_qty) >= 0:
             self.quantity_difference = self.theoretical_qty - self.product_qty
         else:
             self.quantity_difference = self.product_qty - self.theoretical_qty

    _columns = {
        'quantity_difference': fields.function(_quantity_compute, method=True, string='Quantity difference',type='float',store=True),
        
    }
    
stock_inventory_line()


