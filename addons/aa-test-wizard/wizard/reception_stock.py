# -*- coding: utf-8 -*-
import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime
from openerp import api

class reception_stock(osv.osv_memory):
	_name = "reception.stock"
	_description = " Wizard reception stock"

	
		


	
	_columns = {
		'qt_recu':fields.float('Quantite recu',required=True),
		'product_id': fields.char( 'Code à Barre du Produit',  select=True),
		'commande_id':fields.char( 'Code à Barre du Commande',  select=True),
		#'message':fields.char( compute='_message_commande', type="char", method=True),


	}




	@api.cr_uid_ids_context
	def create_move(self, cr, uid, ids,context=None):
		
		
		#obj_move_ids=self.pool.get('stock.move').search(cr, uid, [('product_id.default_code','=','FORMATION'),('product_id.type','=','service')])
		#obj_move = self.pool.get('stock.move').browse(cr, uid, obj_move_ids)


		
		#if obj_move :
		#	for move in obj_move:

		#		print "devis_id===================",move.picking_id.name
				




		#else :
			#raise osv.except_osv(_('Paramètre(s) incorrecte(s)!'), _('Vérifier les codes à barre du produit et son bon de commande'))
		
		return True















