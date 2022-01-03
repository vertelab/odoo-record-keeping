import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class EventMatterWizard(models.TransientModel):
    _name = "rk.wizard.event"

    _inherit = ["rk.wizard"]

    def _get_model(self):
        sale_order = self.env["event.event"].browse(self.env.context.get('active_ids'))
        return sale_order

    model = fields.Many2one(
        comodel_name="event.event",
        default=_get_model,
        readonly=True,
    )
