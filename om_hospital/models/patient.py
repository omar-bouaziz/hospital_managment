from odoo import api, fields, models
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = 'mail.thread'
    _description = "hospital patient"

    name = fields.Char(string="Name", tracking=True)
    date_of_birth = fields.Date(string="date of birth")
    ref = fields.Char(string="Reference", help="Reference from patient record")
    age = fields.Integer(string="Age", compute="_compute_age",inverse='_inverse_compute_age', search='_search_age')

    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")
    active = fields.Boolean(string="Active", default=True)
    appointement_id = fields.Many2one("hospital.appointement", string="Appointement")
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag', string="Tags")
    appointement_count = fields.Integer(string="Appointement Count", compute="_compute_appointement_count", store=True)
    appointement_ids = fields.One2many("hospital.appointement", 'patient_id', string="Appointement")
    parent = fields.Char(string="Parent")
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')], string="Marital Status",
                                      tracking=True)
    partner_name = fields.Char(string="Partner Name")
    is_birthday = fields.Boolean(string="Birthday ?", compute='_compute_is_birthday')
    Phone=fields.Char(string="Phone")
    Email=fields.Char(string="Email")


    @api.depends('appointement_ids')
    def _compute_appointement_count(self):
        for rec in self:
            rec.appointement_count = self.env['hospital.appointement'].search_count([('patient_id', '=', rec.id)])

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(("the entered date of birth is not acceptable ! "))


    @api.ondelete(at_uninstall=False)
    def _check_appointements(self):
        for rec in self:
            if rec.appointement_ids:
                raise ValidationError(("you cannot delete a patient with appointement !"))


    @api.model
    def create(self, vals):
        print("odoo mates", vals)
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).write(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        print("self............", self)
        for rec in self:
            today = date.today()
            print("date.today", date.today())
            if rec.date_of_birth:
                rec.age = (today.year - rec.date_of_birth.year)
            else:
                rec.age = 0



    def action_test(self):
        print("Clicked")

    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)

    def _search_age(self,operator,value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1,month=1)
        end_of_year = date_of_birth.replace(day=31,month=12)
        return [('date_of_birth','>=',start_of_year), ('date_of_birth','<=', end_of_year)]



    def name_get(self):
        # return [(record.id, "[%s] %s" % (record.ref,record.name))for record in self]
        patient_list = []
        for record in self:
            name = record.ref + record.name
            patient_list.append((record.id, name))
        return patient_list


    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday=False
            if rec.date_of_birth:
                today=date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday





