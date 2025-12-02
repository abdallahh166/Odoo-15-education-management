from odoo import models, fields, api


class OpClassroom(models.Model):
    _name = "op.classroom"
    _description = "Classroom"

    name = fields.Char('Name', size=16, required=True)
    code = fields.Char('Code', size=16, required=True)
    course_id = fields.Many2one('op.course', 'Course')
    batch_id = fields.Many2one('op.batch', 'Batch')
    capacity = fields.Integer(string='No of Person')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_classroom_code',
         'unique(code)', 'Code should be unique per classroom!')]

    @api.onchange('course_id')
    def onchange_course(self):
        self.batch_id = False
