from odoo import _, api, fields, models
import logging

_logger = logging.getLogger(__name__)

class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    active = fields.Boolean(
        string="Archived",
        default=True,
        help="If an attachment is set to archived, it is not displayed.",
    )

    receiver = fields.Many2one('res.partner')
    secrecy = fields.Boolean(default=False)
    sender = fields.Many2one('res.partner')