# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions


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
    # instructor_id = fields.Many2one('res.partner', string="Instructor",
    #                                 domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', "Teacher")])

    instructor_id = fields.Many2one('res.partner', string="Instructor")
    course_id = fields.Many2one('module_test.module_test', ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many(comodel_name="res.partner", relation="group_partner_rel", column1="group_id",
                                    column2="partner_id", string="Attendees")
    state = fields.Selection([('draft', "Draft"), ('confirmed', "Confirmed"), ('done', "Done"), ], default='draft')

    @api.multi
    def action_draft(self):
        print("draft1")
        self.state = 'draft'
        print("draft2")

    @api.multi
    def action_confirm(self):
        print("confirm1")
        self.state = 'confirmed'
        print("confirm2")

    @api.multi
    def action_done(self):
        self.state = 'done'

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative",
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees",
                },
            }

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A session's instructor can't be an attendee")
