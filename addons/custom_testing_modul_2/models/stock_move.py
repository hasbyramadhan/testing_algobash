from odoo import models, fields, api, _
from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = 'stock.move'

    valid_product_ids = fields.Many2many(
        'product.product', 
        string='Valid Products',
        compute='_compute_valid_products',
        store=False
    )

    @api.depends('location_dest_id')
    def _compute_valid_products(self):
        for move in self:
            if move.location_dest_id:
                valid_products = self.env['location.product.rule'].search([
                    ('location_id', '=', move.location_dest_id.id)
                ]).mapped('product_id')
                move.valid_product_ids = valid_products
            else:
                move.valid_product_ids = False

    @api.constrains('location_dest_id', 'product_id')
    def _check_product_location(self):
        for move in self:
            valid_products = self.env['location.product.rule'].search([
                ('location_id', '=', move.location_dest_id.id)
            ]).mapped('product_id')

            if move.product_id not in valid_products:
                raise UserError(_('Produk %s tidak valid untuk lokasi %s.') % (move.product_id.name, move.location_dest_id.name))