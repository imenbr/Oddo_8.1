# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class wizard_etat_inventaire(osv.osv_memory):
    _name = "wizard.etat.inventaire"
    _description = '''Wizard pour la generation de l etat d inventaire  '''

    _columns = { 
        'inventory_id':fields.many2one('stock.inventory', 'Inventaire', ),
    }

    def create_report(self, cr, uid, ids, context={}):
        data = self.read(cr,uid,ids,)[-1]
        print data,' create_report('
	res={}
	res={
            'type'         : 'ir.actions.report.xml',
            'report_name'   : 'jasper_report_etat_inventaire_print',
            'datas': {
                    'model':'stock.inventory',
                    'id': context.get('active_ids') and context.get('active_ids')[0] or False,
                    'ids': context.get('active_ids') and context.get('active_ids') or [],
                    'form':data
                    },
            'nodestroy': False
        }
        return res
wizard_etat_inventaire()
