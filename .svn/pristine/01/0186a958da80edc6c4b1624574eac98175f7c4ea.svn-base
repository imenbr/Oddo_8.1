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
from openerp.tools import Number_To_Word


class reglement_avance(osv.osv):
    
	_name = "reglement.avance"
	_description = "Reglement Avance" 
	_rec_name = "code_avance"
	_columns = {
        	'code_avance': fields.char('Reference', size=64, select=True,readonly='True'),
		'date_avance': fields.date('Date', required=True,readonly=True,states={'draft':[('readonly',False)]}),
		'partner_id': fields.many2one('res.partner', 'Client', required=True,readonly=True,states={'draft':[('readonly',False)]}),
		'montant_avance': fields.float('Montant Avance', digits_compute=dp.get_precision('Account'), required=True,readonly=True,states={'draft':[('readonly',False)]}),
		'montant_paye': fields.float('Montant Paye', digits_compute=dp.get_precision('Account'),readonly='True'),
		'mode_reglement': fields.many2one('reglement.mode', 'Mode Reglement', ondelete='set null', required=True,readonly=True,states={'draft':[('readonly',False)]}),		
		'currency_id': fields.many2one('res.currency', 'Devise',readonly=True,states={'draft':[('readonly',False)]}),
		'piece_id': fields.many2one('reglement.piece', 'Cheque', ondelete='set null',domain="[('partner_id','=', partner_id), ('state','in',['cashed'])]",readonly=True,states={'draft':[('readonly',False)]}),
		'state': fields.selection([('draft', 'Draft'),('closed', 'Closed'),('ppaid', 'Partially Paid'),('paid', 'Paid')],'State',readonly='True'),
		'type': fields.selection([('supplier', 'Fournisseur'), ('client', 'Client'),], 'Type Avance', required=True, select=True,),
	}
	
	_defaults = {
        'state': lambda *a: 'draft',
        'montant_paye': 0.0,
	}

	def	create(self, cr, uid, vals, context=None):
                if vals['montant_avance'] == 0.0:
                   raise osv.except_osv(_('Le montant de l avance est null !'),_("Veuillez saisir un montant different de 0 !") )
               
                if context['type'] == 'client':
                   vals['code_avance']=self.pool.get('ir.sequence').get(cr, uid, 'reglement.avance.client')
                if context['type'] == 'supplier':
                   vals['code_avance']=self.pool.get('ir.sequence').get(cr, uid, 'reglement.avance.fournisseur')
		vals['type']=context['type']
		res = super(reglement_avance, self).create(cr, uid, vals, context)
		return res


        def	reg_close(self, cr, uid, ids):
                self.write(cr, uid, ids, { 'state': 'closed' })
                return True

        def	reg_draft(self, cr, uid, ids):
                self.write(cr, uid, ids, { 'state': 'draft' })
                return True
reglement_avance()
