# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime

class releve_client_wizard(osv.osv_memory):
    _name = "releve.client.wizard"
    _description = " "

    _columns = { 
        'fournisseur_id': fields.many2one('res.partner', 'Client',required=True),
        'date_debut': fields.datetime('Date Début', required=True, select=True), 
        'date_fin': fields.datetime('Date Fin', required=True, select=True), 
    }

    def create_report(self, cr, uid, ids, context={}):
        data = self.read(cr,uid,ids,)[-1]
        print data,' create_report('
	res={}
	res={
            'type'         : 'ir.actions.report.xml',
            'report_name'   : 'jasper_rapport_releve_client_print',
            'datas': {
                    'model':'reglement.piece',
                    'id': context.get('active_ids') and context.get('active_ids')[0] or False,
                    'ids': context.get('active_ids') and context.get('active_ids') or [],
                    #'report_type': data['report_type'],
                    'form':data
                    },
            'nodestroy': False
        }
        return res

   
releve_client_wizard()
