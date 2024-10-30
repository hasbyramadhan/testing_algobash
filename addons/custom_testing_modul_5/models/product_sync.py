import logging
import requests
from odoo import models, api

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        product = super(ProductTemplate, self).create(vals)
        self.sync_to_z_app(product)
        return product

    def write(self, vals):
        # Update produk
        result = super(ProductTemplate, self).write(vals)
        for product in self:
            self.sync_to_z_app(product)
        return result

    def sync_to_z_app(self, product):
        # Format data untuk dikirim
        data_to_send = {
            'id': product.id,
            'name': product.name,
            'price': product.list_price,
            'quantity': product.qty_available,
        }

    
        try:
            url = "http://localhost:8069/sync"
            response = requests.post(url, json=data_to_send)
            response.raise_for_status()  

            _logger.info("Data produk '%s' telah disinkronkan ke aplikasi Z*", product.name)

        except requests.exceptions.RequestException as e:
            _logger.error("Gagal mengirim data produk '%s' ke aplikasi Z*: %s", product.name, e)
