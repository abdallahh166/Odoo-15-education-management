from datetime import datetime

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class OpAdmission(models.Model):
    _name = "op.admission"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "application_number"
    _description = "Admission"
    _order = 'id DESC'

    name = fields.Char(
        'Name', size=128, required=True, translate=True)
    first_name = fields.Char(
        'First Name', size=128, required=True, translate=True)
    middle_name = fields.Char(
        'Middle Name', size=128, translate=True,
        states={'done': [('readonly', True)]})
    last_name = fields.Char(
        'Last Name', size=128, required=True, translate=True,
        states={'done': [('readonly', True)]})
    title = fields.Many2one(
        'res.partner.title', 'Title', states={'done': [('readonly', True)]})
    application_number = fields.Char(
        'Application Number', size=16, copy=False,
        required=True, readonly=True, store=True,
        default=lambda self:
        self.env['ir.sequence'].next_by_code('op.admission'))
    admission_date = fields.Date(
        'Admission Date', copy=False,
        states={'done': [('readonly', True)]})
    application_date = fields.Datetime(
        'Application Date', required=True, copy=False,
        states={'done': [('readonly', True)]},
        default=lambda self: fields.Datetime.now())
    birth_date = fields.Date(
        'Birth Date', required=True, states={'done': [('readonly', True)]})
    course_id = fields.Many2one(
        'op.course', 'Course', required=True,
        states={'done': [('readonly', True)]})
    batch_id = fields.Many2one(
        'op.batch', 'Batch', required=False,
        states={'done': [('readonly', True)],
                'submit': [('required', True)],
                'fees_paid': [('required', True)]})
    street = fields.Char(
        'Street', size=256, states={'done': [('readonly', True)]})
    street2 = fields.Char(
        'Street2', size=256, states={'done': [('readonly', True)]})
    phone = fields.Char(
        'Phone', size=16, states={'done': [('readonly', True)],
                                  'submit': [('required', True)]})
    mobile = fields.Char(
        'Mobile', size=16,
        states={'done': [('readonly', True)], 'submit': [('required', True)]})
    email = fields.Char(
        'Email', size=256, required=True,
        states={'done': [('readonly', True)]})
    city = fields.Char('City', size=64, states={'done': [('readonly', True)]})
    zip = fields.Char('Zip', size=8, states={'done': [('readonly', True)]})
    state_id = fields.Many2one(
        'res.country.state', 'States', states={'done': [('readonly', True)]})
    country_id = fields.Many2one(
        'res.country', 'Country', states={'done': [('readonly', True)]})
    image = fields.Image('image', states={'done': [('readonly', True)]})
    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submitted'),
         ('confirm', 'Confirmed'), ('admission', 'Admission Confirm'),
         ('reject', 'Rejected'), ('pending', 'Pending'),
         ('cancel', 'Cancelled'), ('done', 'Done')],
        'State', default='draft', tracking=True)
    prev_institute_id = fields.Char('Previous Institute',
                                    states={'done': [('readonly', True)]})
    prev_course_id = fields.Char('Previous Course',
                                 states={'done': [('readonly', True)]})
    prev_result = fields.Char(
        'Previous Result', size=256, states={'done': [('readonly', True)]})
    family_business = fields.Char(
        'Family Business', size=256, states={'done': [('readonly', True)]})
    family_income = fields.Float(
        'Family Income', states={'done': [('readonly', True)]})
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female'), ('o', 'Other')],
        string='Gender',
        required=True,
        states={'done': [('readonly', True)]})
    student_id = fields.Many2one(
        'op.student', 'Student', states={'done': [('readonly', True)]})
    nbr = fields.Integer('No of Admission', readonly=True)
    register_id = fields.Many2one(
        'op.admission.register', 'Admission Register', required=True,
        states={'done': [('readonly', True)]})
    partner_id = fields.Many2one('res.partner', 'Partner')
    is_student = fields.Boolean('Is Already Student')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id)

    _sql_constraints = [
        ('unique_application_number',
         'unique(application_number)',
         'Application Number must be unique per Application!'),
    ]

    @api.onchange('first_name', 'middle_name', 'last_name')
    def _onchange_name(self):
        if not self.middle_name:
            self.name = str(self.first_name) + " " + str(
                self.last_name
            )
        else:
            self.name = str(self.first_name) + " " + str(
                self.middle_name) + " " + str(self.last_name)

    @api.onchange('student_id', 'is_student')
    def onchange_student(self):
        if self.is_student and self.student_id:
            sd = self.student_id
            self.title = sd.title and sd.title.id or False
            self.first_name = sd.first_name
            self.middle_name = sd.middle_name
            self.last_name = sd.last_name
            self.birth_date = sd.birth_date
            self.gender = sd.gender
            self.image = sd.image_1920 or False
            self.street = sd.street or False
            self.street2 = sd.street2 or False
            self.phone = sd.phone or False
            self.mobile = sd.mobile or False
            self.email = sd.email or False
            self.zip = sd.zip or False
            self.city = sd.city or False
            self.country_id = sd.country_id and sd.country_id.id or False
            self.state_id = sd.state_id and sd.state_id.id or False
            self.partner_id = sd.partner_id and sd.partner_id.id or False
        else:
            self.birth_date = ''
            self.gender = ''
            self.image = False
            self.street = ''
            self.street2 = ''
            self.phone = ''
            self.mobile = ''
            self.zip = ''
            self.city = ''
            self.country_id = False
            self.state_id = False
            self.partner_id = False

    @api.onchange('register_id')
    def onchange_register(self):
        self.course_id = self.register_id.course_id
        self.company_id = self.register_id.company_id

    @api.constrains('register_id', 'application_date')
    def _check_admission_register(self):
        for rec in self:
            start_date = fields.Date.from_string(rec.register_id.start_date)
            end_date = fields.Date.from_string(rec.register_id.end_date)
            application_date = fields.Date.from_string(rec.application_date)
            if application_date < start_date or application_date > end_date:
                raise ValidationError(_(
                    "Application Date should be between Start Date & \
                    End Date of Admission Register."))

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))
            elif record:
                today_date = fields.Date.today()
                day = (today_date - record.birth_date).days
                years = day // 365
                if years < self.register_id.minimum_age_criteria:
                    raise ValidationError(_(
                        "Not Eligible for Admission minimum required age is : %s " % self.register_id.minimum_age_criteria))

    def submit_form(self):
        self.state = 'submit'

    def admission_confirm(self):
        self.state = 'admission'

    def confirm_in_progress(self):
        for record in self:
            record.state = 'confirm'

    def get_student_vals(self):
        for student in self:
            student_user = self.env['res.users'].create({
                'name': student.name,
                'login': student.email,
                'image_1920': self.image or False,
                'is_student': True,
                'company_id': self.company_id.id,
                'groups_id': [
                    (6, 0,
                     [self.env.ref('base.group_portal').id])]
            })
            details = {
                'phone': student.phone,
                'mobile': student.mobile,
                'email': student.email,
                'street': student.street,
                'street2': student.street2,
                'city': student.city,
                'country_id':
                    student.country_id and student.country_id.id or False,
                'state_id': student.state_id and student.state_id.id or False,
                'image_1920': student.image,
                'zip': student.zip,
            }
            student_user.partner_id.write(details)
            details.update({
                'title': student.title and student.title.id or False,
                'first_name': student.first_name,
                'middle_name': student.middle_name,
                'last_name': student.last_name,
                'birth_date': student.birth_date,
                'gender': student.gender,
                'image_1920': student.image or False,
                'course_detail_ids': [[0, False, {
                    'course_id':
                        student.course_id and student.course_id.id or False,
                    'batch_id':
                        student.batch_id and student.batch_id.id or False,
                    'academic_years_id': student.register_id.academic_years_id.id or False,
                    'academic_term_id': student.register_id.academic_term_id.id or False,
                }]],
                'user_id': student_user.id,
                'company_id': self.company_id.id,
                'partner_id': student_user.partner_id.id,
            })
            return details

    def enroll_student(self):
        for record in self:
            if record.register_id.max_count:
                total_admission = self.env['op.admission'].search_count(
                    [('register_id', '=', record.register_id.id),
                     ('state', '=', 'done')])
                if not total_admission < record.register_id.max_count:
                    msg = 'Max Admission In Admission Register :- (%s)' % (
                        record.register_id.max_count)
                    raise ValidationError(_(msg))
            if not record.student_id:
                vals = record.get_student_vals()
                record.partner_id = vals.get('partner_id')
                record.student_id = student_id = self.env[
                    'op.student'].create(vals).id

            else:
                student_id = record.student_id.id
                record.student_id.write({
                    'course_detail_ids': [[0, False, {
                        'course_id':
                            record.course_id and record.course_id.id or False,
                        'batch_id':
                            record.batch_id and record.batch_id.id or False,
                        'fees_term_id': record.fees_term_id.id,
                        'fees_start_date': record.fees_start_date,
                    }]],
                })
            record.write({
                'nbr': 1,
                'state': 'done',
                'admission_date': fields.Date.today(),
                'student_id': student_id,
                'is_student': True,
            })
            reg_id = self.env['op.subject.registration'].create({
                'student_id': student_id,
                'batch_id': record.batch_id.id,
                'course_id': record.course_id.id,
                'min_unit_load': record.course_id.min_unit_load or 0.0,
                'max_unit_load': record.course_id.max_unit_load or 0.0,
                'state': 'draft',
            })
            if not record.phone or not record.mobile:
                raise UserError(
                    _('Please fill in the mobile number'))
            reg_id.get_subjects()

    def confirm_rejected(self):
        self.state = 'reject'

    def confirm_pending(self):
        self.state = 'pending'

    def confirm_to_draft(self):
        self.state = 'draft'

    def confirm_cancel(self):
        self.state = 'cancel'
        if self.is_student and self.student_id:
            self.student_id.state = 'cancel'

    def open_student(self):
        form_view = self.env.ref('core.view_op_student_form')
        tree_view = self.env.ref('core.view_op_student_tree')
        value = {
            'domain': str([('id', '=', self.student_id.id)]),
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'op.student',
            'view_id': False,
            'views': [(form_view and form_view.id or False, 'form'),
                      (tree_view and tree_view.id or False, 'tree')],
            'type': 'ir.actions.act_window',
            'res_id': self.student_id.id,
            'target': 'current',
            'nodestroy': True
        }
        self.state = 'done'
        return value
