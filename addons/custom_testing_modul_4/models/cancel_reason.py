from odoo import models, fields

class CancelReason(models.Model):
    _name = 'cancel.reason'
    _description = 'Cancel Reason'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True) 