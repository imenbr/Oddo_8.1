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

from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp

class quotation_request(osv.osv):
    _name = 'quotation.request'
   
    def create(self, cr, uid, vals, context=None):
       #vals['quotation_request_ref'] = self.pool.get('ir.sequence').get(cr, uid, 'request.quotation')
       vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'request.quotation')
       return super(quotation_request, self).create(cr, uid, vals, context)

    _columns = {
         #'quotation_request_ref': fields.char('Quotation Request Reference', size=64),
         'ref_supplier' : fields.char('Reference Fournisseur', size=64),
         'name': fields.char('Référence', size=64),
         'date_quotation_req':fields.date('Date Quotation Request'),
         'partner_id':fields.many2one('res.partner', 'Supplier', required=True),
         'notes': fields.text('Notes'),
         'quotation_request_line': fields.one2many('quotation.request.line', 'quotation_request_id', 'Quotation Request Line'),    
         'company_id': fields.many2one('res.company', 'Company'),    
    }
    _defaults = {
        'company_id': lambda self, cr, uid, c: self.pool.get('res.company')._company_default_get(cr, uid, 'procurement.order', context=c),
    }
quotation_request()

class quotation_request_line(osv.osv):
    _name = 'quotation.request.line'
   
    _columns = {
        'name': fields.char('Name', size=256, required=True),
        'product_uom': fields.many2one('product.uom', 'Product UOM', required=True),
        'product_id': fields.many2one('product.product', 'Product', domain=[('purchase_ok','=',True)], change_default=True),
        'product_qty': fields.float('Quantity', required=True, digits=(16,2)),
        'quotation_request_id': fields.many2one('quotation.request', 'Quotation Request Reference', ondelete='cascade'),
        'ref_supplier' : fields.char('Reference Fournisseur', size=64),

    }

    _defaults = {
        'product_qty': lambda *a: 1.0,
    }
    def product_id_change(self, cr, uid, ids,partner_id, product, uom, name=False):
        if not product:
            return {'value': {'name': name or '', 'product_uom' : uom or False}}
        prod = self.pool.get('product.product').browse(cr, uid, product)
        prod_uom_po = prod.uom_po_id.id
        if not uom:
            uom = prod_uom_po
        prod_name = self.pool.get('product.product').name_get(cr, uid, [prod.id])[0][1]
        res = {}
	ref_supplier=' '
        
        cr.execute("""SELECT product_name
        FROM product_supplierinfo,  product_product
        WHERE 
        product_product.product_tmpl_id = product_supplierinfo.product_tmpl_id 
        AND product_supplierinfo.name=%s AND product_product.id=%s 
        """,(partner_id,product)) 
        line = cr.dictfetchone()
        
        if line :
            ref_supplier = line['product_name'] 
        res.update({'value': {'name': prod_name, 'product_uom': uom,'ref_supplier':ref_supplier}})
        return res

quotation_request_line()
