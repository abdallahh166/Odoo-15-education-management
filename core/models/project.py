from odoo import models, fields, api, _


class OpProject(models.Model):
    _name = 'op.project'
    _inherit = "mail.thread"
    _description = 'Manage the process of Graduation project'

    name = fields.Char('Name', size=128, required=True)
    code = fields.Char('Code', size=256, required=True)
    description = fields.Char('description', size=256, required=True)

    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_project_code',
         'unique(code)', 'Code should be unique per project!'),
    ]
