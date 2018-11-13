# -*- coding: utf-8 -*-
from osv import osv,fields
from tools.translate import _

class wizard_liste_cheque(osv.osv_memory):
    _name = "wizard.liste.cheque"
    _description = " "

    _columns = { 
        'date_debut': fields.date('Date Début', required=True, select=True), 
        'date_fin': fields.date('Date Fin', required=True, select=True), 
        'mode_reglement_id': fields.many2one('reglement.mode', 'Mode Reglement'),
        'etat_cheque': fields.selection([('free', 'Libre'),('integrated', 'Intégré'),('pimpaid', 'Partiellement Payé'),('impaid', 'Impayé'),('cashed', 'Encaissé')], 'Etat Piéce'),
        'fournisseur_id': fields.many2one('res.partner', 'Fourniseur',required=True),
        'banque_id': fields.many2one('reglement.banque', 'Banque',required=False),
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
        print data,' create_report('
	res={}
	res={
            'type'         : 'ir.actions.report.xml',
            'report_name'   : 'jasper_liste_cheque_print',
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
wizard_liste_cheque()
