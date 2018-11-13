# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _

class wizard_recap_mouvement(osv.osv_memory):
    _name = "wizard.recap.mouvement"
    _description = " "

    _columns = { 
        #'date_debut': fields.date('Année Début', required=True, select=True), 
        'date_debut':fields.selection([("2010","2010"),
                                  ("2011","2011"),
                                  ("2012","2012"),
                                  ("2013","2013"),
                                  ("2014","2014"),
                                  ("2015","2015"),
                                  ("2016","2016"),
                                  ("2017","2017"),
                                  ("2018","2018"),
                                  ("2019","2019"),
                                  ("2020","2020"),
                                 ],'Année Début',required=True, ),
        'date_fin':fields.selection([("2010","2010"),
                                  ("2011","2011"),
                                  ("2012","2012"),
                                  ("2013","2013"),
                                  ("2014","2014"),
                                  ("2015","2015"),
                                  ("2016","2016"),
                                  ("2017","2017"),
                                  ("2018","2018"),
                                  ("2019","2019"),
                                  ("2020","2020"),
                                 ],'Année Fin (inclus)',required=True, ),
        

    }

    def create_report(self, cr, uid, ids, context={}):
        data = self.read(cr,uid,ids,)[-1]
        print data,' create_report('
	res={}
	res={
            'type'         : 'ir.actions.report.xml',
            'report_name'   : 'jasper_recap_mouvement_print',
            'datas': {
                    'model':'account.invoice',
                    'id': context.get('active_ids') and context.get('active_ids')[0] or False,
                    'ids': context.get('active_ids') and context.get('active_ids') or [],
                    
                    'form':data
                    },
            'nodestroy': False
        }
        return res

  
wizard_recap_mouvement()
