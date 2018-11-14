# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Course(models.Model):
    _name = 'module_test.module_test'

    name = fields.Char(string="Title", required=True)
    _rec_name = 'name'

    description = fields.Text()
    responsible_id = fields.Many2one('res.users', ondelete='set null', string="Responsible", index=True)
    session_ids = fields.One2many('module_test.session', 'course_id', string="Sessions")


class Session(models.Model):
    _name = 'module_test.session'

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    instructor_id = fields.Many2one('res.partner', string="Instructor")
    course_id = fields.Many2one('module_test.module_test', ondelete='cascade', string="Course", required=True)
    # attendee_ids = fields.Many2many('res.partner', relation='attendiesSession',
    #                                 column1='name', column2='description', string="Attendees")
    attendee_ids = fields.Many2many(comodel_name="res.partner", relation="group_partner_rel", column1="group_id",
                                   column2="partner_id", string="Opérateurs économiques")
    # attendee_ids = fields.Many2many('res.partner', string="Attendees")
