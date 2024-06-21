from odoo import api, fields, models
from datetime import date
from odoo.exceptions import ValidationError



class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = 'mail.thread'
    _description = "hospital patient"

    name = fields.Char(string="Name",tracking=True)
    date_of_birth=fields.Date(string="date of birth")
    ref=fields.Char(string="Reference",help="Reference from patient record")
    age=fields.Integer(string="Age",compute="_compute_age",readonly=True)
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")
    active = fields.Boolean(string="Active", default=True)
    appointement_id=fields.Many2one("hospital.appointement",string="Appointement")
    image=fields.Image(string="Image")
    tag_ids=fields.Many2many('patient.tag',string="Tags")
    appointement_count=fields.Integer(string="Appointement Count", compute="_compute_appointement_count",store=True)
    appointement_ids= fields.One2many("hospital.appointement",'patient_id',string="Appointement")
    @api.depends('appointement_ids')
    def _compute_appointement_count(self):
        for rec in self :
            rec.appointement_count=self.env['hospital.appointement'].search_count([('patient_id','=',rec.id)])

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self :
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(("the entered date of birth is not acceptable ! "))


    @api.model
    def create(self,vals):
        print("odoo mates",vals)
        vals['ref']= self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient,self).create(vals)

    def write(self,vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient,self).write(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        print("self............",self)
        for rec in self:
            today = date.today()
            print("date.today",date.today())
            if rec.date_of_birth:
                rec.age = (today.year - rec.date_of_birth.year)
            else:
                rec.age = 0

    def name_get(self):
       # return [(record.id, "[%s] %s" % (record.ref,record.name))for record in self]
         patient_list=[]
         for record in self:
             name=record.ref + record.name
             patient_list.append((record.id,name))
         return patient_list



