import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class AccountMatterWizard(models.TransientModel):
    _name = "rk.wizard.account"

    _inherit = ["rk.wizard"]

    def _get_model(self):
        sale_order = self.env["account.move"].browse(self.env.context.get('active_ids'))
        return sale_order

    model = fields.Many2one(
        comodel_name="account.move",
        default=_get_model,
        readonly=True,
    )
