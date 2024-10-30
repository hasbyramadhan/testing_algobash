from odoo import models, fields, api
from odoo.exceptions import UserError

class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    approval_status = fields.Selection([
        ('waiting_approval', 'Waiting for Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Approval Status', default='waiting_approval')

    @api.model
    def create(self, vals):
        vals['approval_status'] = 'waiting_approval' 
        return super(StockInventory, self).create(vals)

    def action_submit_for_approval(self):
        self.approval_status = 'waiting_approval'
        self.state = 'confirm'

    def action_approve(self):
        for record in self:
            if not self.env.user.has_group('custom_testing_modul_3.group_warehouse_manager'):
                raise UserError("You do not have the required permissions to approve this inventory adjustment.")
                
            if record.approval_status == 'waiting_approval':
                record.approval_status = 'approved'  
                record.state = 'done'  
            else:
                raise UserError("Cannot approve inventory adjustment that is not in waiting approval status.")

    def action_reject(self):
        for record in self:
            if not self.env.user.has_group('custom_testing_modul_3.group_warehouse_manager'):
                raise UserError("You do not have the required permissions to reject this inventory adjustment.")
                
            if record.approval_status == 'waiting_approval':
                record.approval_status = 'rejected'  
                record.state = 'draft' 
            else:
                raise UserError("Cannot reject inventory adjustment that is not in waiting approval status.")