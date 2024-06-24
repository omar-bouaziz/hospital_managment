from typing import Dict, List

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class HospitalAppointement(models.Model):
    _name = "hospital.appointement"
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "hospital appointement"
    _rec_name = 'ref'


    patient_id=fields.Many2one("hospital.patient",string="Patient")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender", related="patient_id.gender")
    appointement_time=fields.Datetime(string="appointement_time",default=fields.Datetime.now)
    Booking_date=fields.Date(string="booking date",default=fields.Date.context_today)
    ref = fields.Char(string="Reference")
    prescription=fields.Html("Prescription")
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], default="draft", string="Status", required=True)
    doctor_id=fields.Many2one('res.users',string="Doctor")
    pharmacy_line_ids=fields.One2many('appointement.pharmacy.lines','appointement_id',string='Pharmacy Lines')
    hide_sales_price=fields.Boolean(string="Hide Sale Price")


    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref=self.patient_id.ref

    def unlink(self):
        if self.state != 'draft':
            raise ValidationError(("you can delete appointement only in draft status!"))
        return super(HospitalAppointement,self).unlink()


    def action_test(self):
        print("button clickable !!!!!")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Click Successfull',
                'type': 'rainbow_man',
            }
        }
    def action_in_consultation(self):
        for rec in self:
            if rec.stats=='draft':
                rec.state = "in_consultation"



    def action_done(self):
        for rec in self:
            rec.state = "done"

    def action_cancel(self):
        action=self.env.ref('om_hospital.action_cancel_appointement').read()[0]
        return action


    def action_draft(self):
        for rec in self:
            rec.state = "draft"

class AppointementPharmacyLines(models.Model):
    _name = "appointement.pharmacy.lines"
    _description = "appointement pharmacy lines"

    product_id=fields.Many2one('product.product',required=True)
    price_unit=fields.Float(related='product_id.list_price')
    qty=fields.Integer(string="Quantity",default=1)
    appointement_id=fields.Many2one('hospital.appointement', string='Appointement')



