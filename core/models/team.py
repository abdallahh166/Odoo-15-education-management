from odoo import models, fields, api, _


class OpTeam(models.Model):
    _name = 'op.student.team'
    _description = "Create the team of students"
    _inherit = "mail.thread"

    name = fields.Char('Name', size=128, required=True)
    code = fields.Char('Code', size=256, required=True)
    student_name = fields.Many2one(
        'op.student', 'name', tracking=True)
    project_name = fields.Many2one(
        'op.project', 'Project Name', tracking=True)

    faculty_name = fields.Many2one(
        'op.faculty', 'Faculty Name', tracking=True)

    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_team_code',
         'unique(code)', 'Code should be unique per Team!'),
    ]
