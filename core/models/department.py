

from odoo import models, fields, api


class OpDepartment(models.Model):
    _name = "op.department"
    _description = "Department of the university"

    name = fields.Char('Name')
    code = fields.Char('Code')
    parent_id = fields.Many2one('op.department', 'Parent Department')

    @api.model
    def create(self, vals):
        department = super(OpDepartment, self).create(vals)
        self.env.user.write({'department_ids': [(4, department.id)]})
        return department
