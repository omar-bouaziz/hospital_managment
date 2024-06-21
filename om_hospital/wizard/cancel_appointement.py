import datetime
from odoo import api,fields,models
from odoo.exceptions import ValidationError




class CancelAppointementWizard(models.TransientModel):
    _name = "cancel.appointement.wizard"
    _description = " Cancel Appointement Wizard"

    @api.model
    def default_get(self, fields):
        res=super(CancelAppointementWizard,self).default_get(fields)
        res['date_cancel']=datetime.date.today()
        if self.env.context.get('active_id'):
            res['appointement_id'] = self.env.context.get('active_id')
        return res

    appointement_id=fields.Many2one('hospital.appointement', string='Appointement',domain=[('state','=','draft')])

    reason=fields.Text(string="Reason")
    date_cancel=fields.Date(string="Cancellation Date")


    def action_cancel(self):
        if self.appointement_id.Booking_date==fields.Date.today():
            raise ValidationError(("Sorry, cancellation is not allowed on the same day of booking"))
        return