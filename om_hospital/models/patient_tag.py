from odoo import api, fields, models



class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "  Patient Tag"

    name=fields.Char(string="Name",required=True)
    active=fields.Boolean(string="Active", default=True , copy=False)
    color=fields.Integer(string="Color")
    sequence=fields.Integer(string="sequence",default=True)

    @api.returns('self',lambda value:value.id)
    def copy(self,default=None):
        if default is None:
            default={}
        if not default.get('name'):
            default['name']=("%s (copy)",self.name)
        default['sequence'] =10
        return super(PatientTag,self).copy(default)

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Name must be unique'),
        ('unique_sequence', 'unique(sequence>0)', 'sequence must be not zero positive number!')
    ]



