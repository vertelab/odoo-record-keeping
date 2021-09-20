from odoo import _, api, fields, models
import logging

_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    active = fields.Boolean(
        default=True,
        string='Archived',
        help='Uncheck this to archive the document. It will not be displayed.',
    )
    is_secret = fields.Boolean(
        default=False,
        string='Is subject to secrecy',
        help='Check this if document contains information that is subject to'
             'secrecy. Combine with proper law section.'
    )
    is_official_document = fields.Boolean(
        default=False,
        string='Is official document',
        help='Check this if the document is official.'
    )
    receiver_id = fields.Many2one('res.partner')
    sender_id = fields.Many2one('res.partner')
    
