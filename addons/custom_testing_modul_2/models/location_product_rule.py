from odoo import models, fields

class LocationProductRule(models.Model):
    _name = 'location.product.rule'
    _description = 'Location Product Rule'

    location_id = fields.Many2one(
        'stock.location', 
        string='Location', 
        required=True, 
        domain="[('usage', '=', 'internal')]",
        help="The location where this product is allowed."
    )
    product_id = fields.Many2one(
        'product.product', 
        string='Product', 
        required=True,
        help="The product allowed in the specified location."
    )

    _sql_constraints = [
        ('unique_location_product', 'unique(location_id, product_id)', 'A product can only be assigned to a location once.')
    ]
