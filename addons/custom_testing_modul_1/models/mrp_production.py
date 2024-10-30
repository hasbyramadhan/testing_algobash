from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    estimated_production_time = fields.Float(
        string="Estimated Production Time (Hours)",
        compute="_compute_estimated_production_time",
        store=True,
        help="Estimated production time in hours, calculated based on the Bill of Material (BOM)."
    )

    @api.depends('product_id', 'bom_id')
    def _compute_estimated_production_time(self):
        for record in self:
            if record.bom_id:
                total_time = sum(line.product_qty * line.product_id.produce_time for line in record.bom_id.bom_line_ids)
                record.estimated_production_time = total_time
            else:
                record.estimated_production_time = 1.0

    def action_plan_production(self):
        for record in self:
            if record.date_planned_start and record.estimated_production_time:
                record.date_planned_finished = record.date_planned_start + timedelta(
                    hours=record.estimated_production_time
                )
            else:
                raise UserError("Tanggal mulai dan estimasi waktu produksi harus diisi untuk melanjutkan.")
