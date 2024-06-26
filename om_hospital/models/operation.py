from odoo import api, fields, models
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class HospitalOperation(models.Model):
    _name = "hospital.operation"
    _description = "hospital operation"
    _log_access = False

    doctor_id = fields.Many2one('res.users', string='Doctor')
    operation_name=fields.Char(string="Name")
    reference_record = fields.Reference(selection=[('hospital.patient', 'Patient'),
                                                   ('hospital.appointement', 'Appointement')], string="Record")

    @api.model
    def name_create(self,name):
        return self.create({'operation_name' : name}).name_get()[0]


