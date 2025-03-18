import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class SaleMatterWizard(models.TransientModel):
    _name = "rk.wizard.sale"

    _inherit = ["rk.wizard"]

    def _get_model(self):
        sale_order = self.env["sale.order"].browse(self.env.context.get('active_ids'))
        return sale_order

    model = fields.Many2one(
        comodel_name="sale.order",
        default=_get_model,
        readonly=True,
    )
