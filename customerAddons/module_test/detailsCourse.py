from openerp import fields, models


class DetailsCourse(models.Model):
    _inherit = 'module_test.module_test'
    duration = fields.Integer(string="dure du cours")

