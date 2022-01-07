import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class AttachmentMatterWizard(models.TransientModel):
    _name = "rk.wizard.attachment"

    _inherit = ["rk.wizard"]

    def _get_model(self):
        sale_order = self.env["ir.attachment"].browse(self.env.context.get('active_ids'))
        return sale_order

    model = fields.Many2one(
        comodel_name="ir.attachment",
        default=_get_model,
        readonly=True,
    )
