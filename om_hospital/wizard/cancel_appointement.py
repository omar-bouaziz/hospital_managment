import datetime
from odoo import api,fields,models
from odoo.exceptions import ValidationError
from datetime import date
from dateutil import relativedelta





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

        cancel_day = self.env['ir.config_parameter'].get_param('om_hospital.cancel_day')
        allowed_date = self.appointement_id.Booking_date - relativedelta.relativedelta(days=int(cancel_day))
        if allowed_date < date.today():
            raise ValidationError(("sorry, cancellation is not allowed for this booking"))
        self.appointement_id.state = 'cancel'
        return{
            'type': 'ir.actions.client',
            'tag': 'reload',

        }



