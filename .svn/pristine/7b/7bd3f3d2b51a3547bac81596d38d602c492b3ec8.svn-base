# -*- coding: utf-8 -*-
from osv import osv,fields
from tools.translate import _
import time
from datetime import datetime

class wizard_grand_livre(osv.osv_memory):
    _name = "wizard.grand.livre"
    _description = " "

    _columns = { 
        'fournisseur_id': fields.many2one('res.partner', 'Fournisseur',required=True),
        'date_debut': fields.date('Date Début', required=True, select=True), 
        'date_fin': fields.date('Date Fin', required=True, select=True), 
    }

    def create_report(self, cr, uid, ids, context={}):
        data = self.read(cr,uid,ids,)[-1]
        print data,' create_report('
	res={}
	res={
            'type'         : 'ir.actions.report.xml',
            'report_name'   : 'jasper_rapport_grand_livre_print',
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

   
wizard_grand_livre()
