# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY OpenERP S.A. <http://www.openerp.com>
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
from openerp.osv import fields, osv
#import netsvc
class res_partner(osv.osv):

    def create(self, cr, uid, vals, context=None):
        vals['reference'] = self.pool.get('ir.sequence').get(cr, uid, 'partner.reference')
        return super(res_partner, self).create(cr, uid, vals, context)

    _inherit = "res.partner"
    _columns = {
        'reference': fields.char('Référence', select=1),
	'exoner':fields.boolean('Exonere'),
	'timbre':fields.boolean('Timbre'),
        'mf':fields.char('M.F', size=64),
        'code_tva':fields.char('Code TVA', size=32),
        'code_categ':fields.char('Code Categorie', size=32),
        'num_etab':fields.char('Num Etablissement', size=32),
	}   

res_partner()

