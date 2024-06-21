import datetime
from odoo import api,fields,models




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

    appointement_id=fields.Many2one('hospital.appointement', string='Appointement')
    reason=fields.Text(string="Reason")
    date_cancel=fields.Date(string="Cancellation Date")


    def action_cancel(self):
        return