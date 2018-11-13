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
#import time
#from lxml import etree
#import pdb
#import string
#import re
#import netsvc
#import pooler
#import stock

from datetime import datetime
from dateutil.relativedelta import relativedelta
import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools.float_utils import float_compare
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP

class purchase_order_line(osv.osv):

    _name = 'purchase.order.line'
    _inherit = 'purchase.order.line'

    def _amount_line(self, cr, uid, ids, prop, arg, context=None):
        '''
           Modifier cette methode pour mettre en considération la remise
        '''
        res = {}
        cur_obj=self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        for line in self.browse(cr, uid, ids, context=context):
            price = line.price_unit * (1 - line.discount * 0.01)
            taxes = tax_obj.compute_all(cr, uid, line.taxes_id, price, line.product_qty, line.product_id, line.order_id.partner_id)
            
            cur = line.order_id.pricelist_id.currency_id
            res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])
        
        return res

    _columns = {
        'default_code' : fields.char('Référence', size=64),
        'ref_supplier' : fields.char('Référence Fournisseur', size=64),
        'price_unit': fields.float('Unit Price', required=True, digits_compute=dp.get_precision('Account')),
        'discount': fields.float('Remise',digits_compute=dp.get_precision('Account')),
        'price_subtotal': fields.function(_amount_line, method=True, string='Subtotal', digits_compute=dp.get_precision('Account')),
        #'rest_product_qty': fields.float('Quantite non Livrée', digits=(16,2)),
        'name_prod_supplier' : fields.char('Désignation Fournisseur', size=64),
    }

    def onchange_product_id(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, state='draft', context=None, discount=False,
            ref_supplier=False, name_prod_supplier=False):
        """
        onchange handler of product_id.
        Modifier cette fonction pour prendre en compte les propositions des prix fournisseurs
        """
        
        if context is None:
            context = {}

        res = {'value': {'price_unit': price_unit or 0.0, 'name': name or '', 'product_uom' : uom_id or False}}
        if not product_id:
            return res

        product_product = self.pool.get('product.product')
        product_uom = self.pool.get('product.uom')
        res_partner = self.pool.get('res.partner')
        product_pricelist = self.pool.get('product.pricelist')
        account_fiscal_position = self.pool.get('account.fiscal.position')
        account_tax = self.pool.get('account.tax')

        # - check for the presence of partner_id and pricelist_id
        #if not partner_id:
        #    raise osv.except_osv(_('No Partner!'), _('Select a partner in purchase order to choose a product.'))
        #if not pricelist_id:
        #    raise osv.except_osv(_('No Pricelist !'), _('Select a price list in the purchase order form before choosing a product.'))

        # - determine name and notes based on product in partner lang.
        context_partner = context.copy()
        if partner_id:
            lang = res_partner.browse(cr, uid, partner_id).lang
            context_partner.update( {'lang': lang, 'partner_id': partner_id} )
        product = product_product.browse(cr, uid, product_id, context=context_partner)
        #call name_get() with partner in the context to eventually match name and description in the seller_ids field
        dummy, name = product_product.name_get(cr, uid, product_id, context=context_partner)[0]
        if product.description_purchase:
            name += '\n' + product.description_purchase
        res['value'].update({'name': name})

        # - set a domain on product_uom
        res['domain'] = {'product_uom': [('category_id','=',product.uom_id.category_id.id)]}

        # - check that uom and product uom belong to the same category
        product_uom_po_id = product.uom_po_id.id
        if not uom_id:
            uom_id = product_uom_po_id

        if product.uom_id.category_id.id != product_uom.browse(cr, uid, uom_id, context=context).category_id.id:
            if context.get('purchase_uom_check') and self._check_product_uom_group(cr, uid, context=context):
                res['warning'] = {'title': _('Warning!'), 'message': _('Selected Unit of Measure does not belong to the same category as the product Unit of Measure.')}
            uom_id = product_uom_po_id

        res['value'].update({'product_uom': uom_id})

        # - determine product_qty and date_planned based on seller info
        if not date_order:
            date_order = fields.datetime.now()


        supplierinfo = False
        #rimbd modif
        supplier_price = False
        #end rimbd modif
        precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Product Unit of Measure')
        for supplier in product.seller_ids:
            if partner_id and (supplier.name.id == partner_id):
                supplierinfo = supplier
                #rimbd modif
                discount = supplierinfo.supplier_discount
                ref_supplier = supplierinfo.product_code
                name_prod_supplier = supplierinfo.product_name
                supplier_price = supplierinfo.prix
                #end rimbd modif 
                if supplierinfo.product_uom.id != uom_id:
                    res['warning'] = {'title': _('Warning!'), 'message': _('The selected supplier only sells this product by %s') % supplierinfo.product_uom.name }
                min_qty = product_uom._compute_qty(cr, uid, supplierinfo.product_uom.id, supplierinfo.min_qty, to_uom_id=uom_id)
                if float_compare(min_qty , qty, precision_digits=precision) == 1: # If the supplier quantity is greater than entered from user, set minimal.
                    if qty:
                        res['warning'] = {'title': _('Warning!'), 'message': _('The selected supplier has a minimal quantity set to %s %s, you should not purchase less.') % (supplierinfo.min_qty, supplierinfo.product_uom.name)}
                    qty = min_qty
        dt = self._get_date_planned(cr, uid, supplierinfo, date_order, context=context).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        qty = qty or 1.0
        res['value'].update({'date_planned': date_planned or dt})
        if qty:
            res['value'].update({'product_qty': qty})
            
        price = price_unit
        if price_unit is False or price_unit is None:
            # - determine price_unit and taxes_id
            if pricelist_id:
                date_order_str = datetime.strptime(date_order, DEFAULT_SERVER_DATETIME_FORMAT).strftime(DEFAULT_SERVER_DATE_FORMAT)
                price = product_pricelist.price_get(cr, uid, [pricelist_id],
                        product.id, qty or 1.0, partner_id or False, {'uom': uom_id, 'date': date_order_str})[pricelist_id]
            else:
                price = product.standard_price
        #rimbd modif 
        if supplier_price:
            price = supplier_price
        else:
            price = product.standard_price
        res['value'].update({'default_code': product.default_code,
                             'discount':discount,
                             'ref_supplier': ref_supplier,
                             'name_prod_supplier':name_prod_supplier})
        #end rimbd modif
        taxes = account_tax.browse(cr, uid, map(lambda x: x.id, product.supplier_taxes_id))
        fpos = fiscal_position_id and account_fiscal_position.browse(cr, uid, fiscal_position_id, context=context) or False
        taxes_ids = account_fiscal_position.map_tax(cr, uid, fpos, taxes)
        res['value'].update({'price_unit': price, 'taxes_id': taxes_ids})
        return res


purchase_order_line()


class purchase_order(osv.osv):
   
    _name = 'purchase.order'
    _inherit = 'purchase.order'
    #STATE_SELECTION = [
    #    ('draft', 'Draft PO'),
    #    ('sent', 'RFQ'),
    #    ('bid', 'Bid Received'),
    #    ('confirmed', 'Waiting Approval'),
    #    ('approved', 'Purchase Confirmed'),
    #    ('except_picking', 'Shipping Exception'),
    #    ('except_invoice', 'Invoice Exception'),
    #    ('done', 'Done'),
    #    ('cancel', 'Cancelled')
    #]
    #_track = {
    #    'state': {
    #        'purchase.mt_rfq_confirmed': lambda self, cr, uid, obj, ctx=None: obj.state == 'confirmed',
    #        'purchase.mt_rfq_approved': lambda self, cr, uid, obj, ctx=None: obj.state == 'approved',
    #        'purchase.mt_rfq_done': lambda self, cr, uid, obj, ctx=None: obj.state == 'done',
    #    },
    #}

    def _shipped_rate(self, cr, uid, ids, name, arg, context=None):
        if not ids: return {}
        res = {}
        for id in ids:
            res[id] = [0.0,0.0]
        cr.execute('''SELECT
                p.order_id, sum(m.product_qty), m.state
            FROM
                stock_move m
            LEFT JOIN
                purchase_order_line p on (p.id=m.purchase_line_id)
            WHERE
                p.order_id IN %s GROUP BY m.state, p.order_id''',(tuple(ids),))
        for oid,nbr,state in cr.fetchall():
            if state=='cancel':
                continue
            if state=='done':
                res[oid][0] += nbr or 0.0
                res[oid][1] += nbr or 0.0
            else:
                res[oid][1] += nbr or 0.0
        for r in res:
            if not res[r][1]:
                res[r] = 0.0
            else:
                res[r] = 100.0 * res[r][0] / res[r][1]
        return res

    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('purchase.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()

    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        '''
           Modifier la methode par defaut pour prendre en consideration la remise
        '''
        res = {}
        cur_obj=self.pool.get('res.currency')
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
            }
            val = val1 = 0.0
            cur = order.pricelist_id.currency_id
            for line in order.order_line:
               #rimbd 
               val1 += line.price_subtotal
               #for c in self.pool.get('account.tax').compute_all(cr, uid, line.taxes_id, line.price_unit, line.product_qty, line.product_id, order.partner_id)['taxes']:
               price = line.price_unit * (1 - line.discount * 0.01)
               for c in self.pool.get('account.tax').compute_all(cr, uid, line.taxes_id, price, line.product_qty, line.product_id, order.partner_id)['taxes']:
                    val += c.get('amount', 0.0)
                    
            res[order.id]['amount_tax']=cur_obj.round(cr, uid, cur, val)
            res[order.id]['amount_untaxed']=cur_obj.round(cr, uid, cur, val1)
            res[order.id]['amount_total']=res[order.id]['amount_untaxed'] + res[order.id]['amount_tax']
        return res

    _columns = {

        'name': fields.char('Order Reference', size=64, required=True, select=True,states={'confirmed':[('readonly',True)],           'approved':[('readonly',True)],'done':[('readonly',True)]}, help="unique number of the purchase order,computed automatically when the purchase order is created"),
	'pricelist_id':fields.many2one('product.pricelist', 'Pricelist', states={'confirmed':[('readonly',True)], 'approved':[('readonly',True)],'done':[('readonly',True)]}, help="The pricelist sets the currency used for this purchase order. It also computes the supplier price for the selected products/quantities."),
        'date_shipping':fields.date('Date de Livraison',states={'confirmed':[('readonly',True)], 'approved':[('readonly',True)]}, help="Date de livraison"),
       
        #'address_destination': fields.many2one('res.partner.address', 'Adresse Livraison',states={'confirmed':[('readonly',True)], 'approved':[('readonly',True)]},help="Adresse de livraison."),
        'location_id': fields.many2one('stock.location', 'Destination', required=True, domain=[('usage','<>','view')],states={'confirmed':[('readonly',True)], 'approved':[('readonly',True)]}),
        
        'resiliation_cause': fields.selection([('non_confirm','Produit pas conforme à nos besoins'),('retard','Retard de livraison'),('rupture','Rupture de votre stock'),('other','Autres')], 'Cause Resiliation',states={'confirmed':[('readonly',True)], 'approved':[('readonly',True)],'done':[('readonly',True)]}),
        'amount_untaxed': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Untaxed Amount',
            store={
                'purchase.order.line': (_get_order, None, 10),
            }, multi="sums", help="The amount without tax", track_visibility='always'),
        'amount_tax': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Taxes',
            store={
                'purchase.order.line': (_get_order, None, 10),
            }, multi="sums", help="The tax amount"),
        'amount_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total',
            store={
                'purchase.order.line': (_get_order, None, 10),
            }, multi="sums", help="The total amount"),
	
        'shipped_rate': fields.function(_shipped_rate, string='Received Ratio', type='float'),
	#'state': fields.selection(STATE_SELECTION, 'State', readonly=True, help="The state of the purchase order or the quotation request. A quotation is a purchase order in a 'Draft' state. Then the order has to be confirmed by the user, the state switch to 'Confirmed'. Then the supplier must confirm the order to change the state to 'Approved'. When the purchase order is paid and received, the state becomes 'Done'. If a cancel action occurs in the invoice or in the reception of goods, the state becomes in exception.", select=True),
        
        'dest_address_id':fields.many2one('res.partner.address', 'Destination Address',
            states={'done':[('readonly',True)]},
            help="Put an address if you want to deliver directly from the supplier to the customer." \
                "In this case, it will remove the warehouse link and set the customer location."
        ),
        #ce champ est ajouté pour stopper la generation automatique des factures à partir du BC
        'create_invoice':fields.boolean('Générer facture'),
}
    _defaults = {
        
        #'partner_address_id': lambda self, cr, uid, context: context.get('partner_id', False) and self.pool.get('res.partner').address_get(cr, uid, [context['partner_id']], ['default'])['default'],
        #'pricelist_id': lambda self, cr, uid, context: context.get('partner_id', False) and self.pool.get('res.partner').browse(cr, uid, context['partner_id']).property_product_pricelist_purchase.id,
        #'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'purchase.order', context=c),
        'create_invoice':False,
    }

    def _prepare_order_line_move(self, cr, uid, order, order_line, picking_id, group_id, context=None):
        
        ''' prepare the stock move data from the PO line. This function returns a list of dictionary ready to be used in stock.move's create()'''
        product_uom = self.pool.get('product.uom')
        price_unit = order_line.price_unit
        #if order_line.product_uom.id != order_line.product_id.uom_id.id:
            #price_unit *= order_line.product_uom.factor / order_line.product_id.uom_id.factor
        #if order.currency_id.id != order.company_id.currency_id.id:
            #we don't round the price_unit, as we may want to store the standard price with more digits than allowed by the currency
            #price_unit = self.pool.get('res.currency').compute(cr, uid, order.currency_id.id, order.company_id.currency_id.id, price_unit, round=False, context=context)
        res = []
        move_template = {
            'name': order_line.name or '',
            'product_id': order_line.product_id.id,
            'product_uom': order_line.product_uom.id,
            'product_uos': order_line.product_uom.id,
            'date': order.date_order,
            'date_expected': fields.date.date_to_datetime(self, cr, uid, order_line.date_planned, context),
            'location_id': order.partner_id.property_stock_supplier.id,
            'location_dest_id': order.location_id.id,
            'picking_id': picking_id,
            'partner_id': order.dest_address_id.id or order.partner_id.id,
            'move_dest_id': False,
            'state': 'draft',
            'purchase_line_id': order_line.id,
            'company_id': order.company_id.id,
            'price_unit': price_unit,
            'picking_type_id': order.picking_type_id.id,
            'group_id': group_id,
            'procurement_id': False,
            'origin': order.name,
            'route_ids': order.picking_type_id.warehouse_id and [(6, 0, [x.id for x in order.picking_type_id.warehouse_id.route_ids])] or [],
            'warehouse_id':order.picking_type_id.warehouse_id.id,
            'invoice_state': order.invoice_method == 'picking' and '2binvoiced' or 'none',
            #rimbd
            'discount':order_line.discount,
            'move_tax_id':[(6, 0, [x.id for x in order_line.taxes_id])] or [],
            #rimbd modif
            #'product_reste_qty':order_line.product_qty,  
            #'product_order_qty':order_line.product_qty,
        }
        
        diff_quantity = order_line.product_qty
        for procurement in order_line.procurement_ids:
            procurement_qty = product_uom._compute_qty(cr, uid, procurement.product_uom.id, procurement.product_qty, to_uom_id=order_line.product_uom.id)
            tmp = move_template.copy()
            tmp.update({
                'product_uom_qty': min(procurement_qty, diff_quantity),
                'product_uos_qty': min(procurement_qty, diff_quantity),
                'move_dest_id': procurement.move_dest_id.id,  #move destination is same as procurement destination
                'group_id': procurement.group_id.id or group_id,  #move group is same as group of procurements if it exists, otherwise take another group
                'procurement_id': procurement.id,
                'invoice_state': procurement.rule_id.invoice_state or (procurement.location_id and procurement.location_id.usage == 'customer' and procurement.invoice_state=='picking' and '2binvoiced') or (order.invoice_method == 'picking' and '2binvoiced') or 'none', #dropship case takes from sale
                'propagate': procurement.rule_id.propagate,
            })
            diff_quantity -= min(procurement_qty, diff_quantity)
            res.append(tmp)
        #if the order line has a bigger quantity than the procurement it was for (manually changed or minimal quantity), then
        #split the future stock move in two because the route followed may be different.
        if float_compare(diff_quantity, 0.0, precision_rounding=order_line.product_uom.rounding) > 0:
            move_template['product_uom_qty'] = diff_quantity
            move_template['product_uos_qty'] = diff_quantity
            res.append(move_template)
       
        return res
    
    #def action_picking_create(self, cr, uid, ids, context=None):
    #    for order in self.browse(cr, uid, ids):
    #        picking_vals = {
    #            'picking_type_id': order.picking_type_id.id,
    #            'partner_id': order.dest_address_id.id or order.partner_id.id,
    #            'date': max([l.date_planned for l in order.order_line]),
    #            'origin': order.name,
    #            #rimbd modif
    #            'purchase_id':order.id,
    #            'do_filter':True,
    #        }
    #        picking_id = self.pool.get('stock.picking').create(cr, uid, picking_vals, context=context)
    #        self._create_stock_moves(cr, uid, order, order.order_line, picking_id, context=context)
       
purchase_order()



