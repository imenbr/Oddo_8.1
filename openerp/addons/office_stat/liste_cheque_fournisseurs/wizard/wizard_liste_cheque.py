# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime

class wizard_liste_cheque_fournisseur(osv.osv_memory):
    _name = "wizard.liste.cheque.fournisseur"
    _description = " "

    _columns = { 
        #'date_debut': fields.date('Date Début', required=True, select=True), 
        #'date_fin': fields.date('Date Fin', required=True, select=True), 
        'date_debut': fields.date('Date Début', select=True), 
        'date_fin': fields.date('Date Fin', select=True),
        'partner_ids':fields.many2many('res.partner','wizard_liste_partner_rel','wizard_cheque_id','partner_id', String='Fournisseur'),#-----
        'type_paiement': fields.many2one('reglement.mode','Type', select=True, domain="[('designation','in',('Traite','Chèque'))]"),#----- 
        'report_type':fields.selection([("pdf","PDF"),
                                        ("xls","Excel"),
                                        ("html","HTML")
                                        ],'Type'),
        
        'state': fields.selection([('choose','choose'),
                                    ('get','get'),
                                   ]),

    }

    def create_report(self, cr, uid, ids, context={}):
        data = self.read(cr,uid,ids,)[-1]
        print data,' create_report(test'
	res={}
	res={
            'type'         : 'ir.actions.report.xml',
            'report_name'   : 'jasper_liste_cheque_fournisseur_print',
            'datas': {
                    'model':'reglement.piece',
                    'id': context.get('active_ids') and context.get('active_ids')[0] or False,
                    'ids': context.get('active_ids') and context.get('active_ids') or [],
                    'report_type': data['report_type'],
                    'form':data
                    },
            'nodestroy': False
        }
        return res

    _defaults = {
                     'report_type': lambda *a: 'pdf',
                     'state': lambda *a: 'choose',
    }
wizard_liste_cheque_fournisseur()
