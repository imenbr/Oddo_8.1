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
class sale_devis(osv.osv):
    _name = "sale.devis"
    _description = "Sales Devis"

    def draft(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'draft'})
        return True

    def envoyer(self, cr, uid, ids, context):
        '''
           Methode du workflow: changer l'état du devis à l'état envoyé
        ''' 
        self.reset_taxes(cr, uid, ids, context) 
        self.write(cr, uid, ids, {'state': 'sent'})
        return True

    def confirmer(self, cr, uid, ids, context):  
        '''
           Methode du workflow: permet la confirmation du devis et la création du Bon de commande
        '''   
        self.reset_taxes(cr, uid, ids, context) 
        self.write(cr, uid, ids, {'state': 'confirmed'})
        for devis in self.browse(cr, uid, ids):         
            vals = {
                'name':self.pool.get('ir.sequence').get(cr, uid, 'sale.order'),
                'partner_id':devis.partner_id.id,
                'date_order': devis.date,
                'state':'draft',
            }
            new_id = self.pool.get('sale.order').create(cr, uid, vals)
            sale_order = self.pool.get('sale.order').browse(cr, uid, new_id)           
            for ligne in devis.devis_lines:
                ligne_vals = {
                    'order_id':new_id,
                    'product_id':ligne.product_id.id,
                    'name':ligne.product_id.name,
                    'price_unit':ligne.price_unit,
                    'discount':ligne.discount,
                    'product_uom_qty':ligne.product_qty,
                    'tax_id':[(6, 0, [x.id for x in ligne.tax_ids])],                  
                }
                new_line_id = self.pool.get('sale.order.line').create(cr, uid, ligne_vals)              
        return True

    def create(self, cr, uid, vals, context=None):
        vals['reference']= self.pool.get('ir.sequence').get(cr, uid, 'sale.devis') 
        new_id = super(sale_devis,self).create(cr, uid, vals, context=context) 
        return new_id

    def action_view_order(self, cr, uid, ids, context=None):
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')

        result = mod_obj.get_object_reference(cr, uid, 'sale', 'action_order_tree')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        #choose the view_mode accordingly
        if len(ids)>1:
            result['domain'] = "[('id','in',["+','.join(map(str, ids))+"])]"
        else:
            res = mod_obj.get_object_reference(cr, uid, 'sale', 'view_order_form')
            result['views'] = [(res and res[1] or False, 'form')]
            result['res_id'] = ids and ids[0] or False
        return result


    @api.one
    @api.depends('devis_lines.price_subtotal','tax_lines.amount')
    def _amount_all(self):
        '''
           Methode qui calcule les montants suivants
           amount_untaxed
           amount_tax
           amount_total
           undiscount_total
           discount_total  
        '''  
        self.amount_untaxed = sum(line.price_subtotal for line in self.devis_lines)
        self.amount_tax = sum(line.amount for line in self.tax_lines)
        self.discount_total = sum( (line.product_qty * line.price_unit * ((line.discount or 0.0)/100.0) ) for line in self.devis_lines ) 
        self.undiscount_total = sum(line.product_qty * line.price_unit for line in self.devis_lines) 
        self.amount_total = self.amount_untaxed + self.amount_tax

    _columns = {
        'reference' : fields.char('Référence', size=64, readonly=True),
        'date' : fields.datetime('Date', required=True),
        'partner_id': fields.many2one('res.partner', 'Client', required=True, domain="[('customer','=',True)]"),
        'company_id': fields.many2one('res.company', 'Company'),
        'devis_lines': fields.one2many('sale.devis.line', 'devis_id', 'Ligne de devis'),
        'tax_lines': fields.one2many('sale.devis.taxe', 'devis_id', 'Lignes Tax', ),
        'discount_total':fields.float(string='Total Remise', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_amount_all', track_visibility='always'),
        'undiscount_total':fields.float(string='Total HT sans remise', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_amount_all', track_visibility='always'),
        'amount_untaxed':fields.float(string='Total HT', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_amount_all', track_visibility='always'),
        'amount_tax':fields.float(string='Total Taxe', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_amount_all', track_visibility='always'),
        'amount_total':fields.float(string='Total', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_amount_all', track_visibility='always'),
        'state': fields.selection(
                [('draft', 'draft'),('sent', 'Envoyé'),('confirmed', 'Confirmé')]),
    }
    _defaults = {
        'state': 'draft',
        'company_id': lambda self, cr, uid, c: self.pool.get('res.company')._company_default_get(cr, uid, 'procurement.order', context=c),
    }

    def button_reset_taxes(self, cr, uid, ids, context=None):    
        '''
           Action du bouton reset Taxes
        '''       
        self.reset_taxes(cr, uid, ids, context)
        return True

    def reset_taxes(self, cr, uid, ids, context=None):       
        '''
           Methode qui permet de calculer et mettre à jour les lignes de taxes
        '''        
        if context is None:
            context = {}
        ctx = context.copy()
        ait_obj = self.pool.get('sale.devis.taxe')
        for id in ids:
            partner = self.browse(cr, uid, id, context=ctx).partner_id
            if partner.lang:
               cr.execute("DELETE FROM sale_devis_taxe WHERE devis_id=%s", (id,))
               ctx.update({'lang': partner.lang})
            for taxe in ait_obj.compute(cr, uid, id, context=ctx).values():
                ait_obj.create(cr, uid, taxe)          
        return True

class sale_devis_line(osv.osv):
    _name = "sale.devis.line"
    _description = "Sales Devis Line"

    @api.one
    @api.depends('price_unit', 'discount', 'tax_ids', 'product_qty',
        'product_id', 'devis_id.partner_id')#, 'devis_id.currency_id')
    def _amount_line(self):
        '''
           Methode qui permet de calculer le sous total d'une ligne de devis
        '''
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        taxes = self.tax_ids.compute_all(price, self.product_qty, product=self.product_id, partner=self.devis_id.partner_id)
        self.price_subtotal = taxes['total']
        
    def _get_uom_id(self, cr, uid, *args):
        return self.pool["product.uom"].search(cr, uid, [], limit=1, order='id')[0]

    _columns = {
        'devis_id' : fields.many2one('sale.devis' , 'Sale Devis' , ondelete='cascade'),
        'product_id': fields.many2one('product.product', 'Produit', ondelete='restrict'),
        'price_unit': fields.float('Prix'),
        'product_qty': fields.float('Quantité'),
        'discount': fields.float('Remise'),
        'product_uom': fields.many2one('product.uom', 'Unité de mesure', required=True),
        'tax_ids': fields.many2many('account.tax', 'sale_devis_line_tax', 'devis_line_id', 'tax_id', 'Taxes', ),
        'price_subtotal':fields.float(string='Amount', digits= dp.get_precision('Account'),
        store=True, readonly=True, compute='_amount_line'),
    }
    
    _defaults = {
        'product_qty': lambda *a: 1.0,
        'product_uom': _get_uom_id,
        'discount': lambda *a: 0.0,
        'price_unit': lambda *a:  0.0,
    }

    def product_id_change(self, cr, uid, ids, product, tax_ids, context=None):

	res_final = {}
        if product:
            #les informations sur le produit
            product_obj = self.pool.get('product.template').browse(cr,uid,product,context=context)
            print "product price : =====",product_obj.list_price
            price = product_obj.list_price
            #les informations sur les taxes du produit
	    taxes = self.pool.get('product.template').browse(cr,uid,product,context=context)

            res_final = {'value':{'price_unit':price, 'tax_ids': taxes.taxes_id}}
        return res_final

class sale_devis_taxe(osv.osv):
    _name = "sale.devis.taxe"
    _description = "Sale Devis Tax"

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
        'devis_id': fields.many2one('sale.devis', 'Devis', ondelete='cascade', select=True),
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

    def compute(self, cr, uid, devis_id, context=None):           
        tax_grouped = {}
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        devis = self.pool.get('sale.devis').browse(cr, uid, devis_id, context=context)
        #cur = devis.currency_id
        company_currency = devis.company_id.currency_id.id

        for line in devis.devis_lines:
            prod = self.pool.get('product.product').browse(cr, uid, line.product_id, context=context)
            price=line.price_unit* (1-(line.discount or 0.0)/100.0)
            for tax in tax_obj.compute_all(cr, uid, line.tax_ids, price, line.product_qty, line.product_id, devis.partner_id)['taxes']:
                val={}
                val['devis_id'] = devis.id
                val['name'] = tax['name'][-5:].replace('-','')
                val['amount'] = tax['amount']
                val['manual'] = False
                val['sequence'] = tax['sequence']
                val['base'] = tax['price_unit'] * line['product_qty']

                
                val['base_code_id'] = tax['base_code_id']
                val['tax_code_id'] = tax['tax_code_id']
                    
                val['base_amount'] = cur_obj.compute(cr, uid, company_currency, company_currency, val['base'] * tax['base_sign'], context={'date': devis.date or time.strftime('%Y-%m-%d')}, round=False)
                    
                val['tax_amount'] = cur_obj.compute(cr, uid, company_currency, company_currency, val['amount'] * tax['tax_sign'], context={'date': devis.date or time.strftime('%Y-%m-%d')}, round=False)
                val['account_id'] = tax['account_collected_id'] or line.account_id.id
            
                key = (val['tax_code_id'], val['base_code_id'], val['account_id'])
                if not key in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base'] += val['base']
                    tax_grouped[key]['base_amount'] += val['base_amount']
                    tax_grouped[key]['tax_amount'] += val['tax_amount']

        return tax_grouped


   


