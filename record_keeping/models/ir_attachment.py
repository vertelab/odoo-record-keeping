from datetime import datetime
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import logging

from werkzeug.exceptions import default_exceptions

_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    active = fields.Boolean(
        default=True,
        help='True if the document is visible. ',
        string='Active',
    )
    drawn_up_date = fields.Date(
        default=False,
        help='The date when the document is ready to be used or sent',
        string='Drawn up',
    )
    is_secret = fields.Boolean(
        default=False,
        help='Check this option if it can be assumed that information contained '
             'in this document should not be disclosed on grounds of secrecy.',
        string='Secrecy marker',
    )
    is_official = fields.Boolean(
        default=False,
        help='Check this option if this document is an official document',
        string='Official document',
    )
    received_date = fields.Date(
        default=False,
        help='The date when the document has been received by a competent person.',
        string='Received',
    )
    receiver_id = fields.Many2one(
        comodel_name='res.partner',
        string='Receiver',
    )
    sender_id = fields.Many2one(
        comodel_name='res.partner',
        help='A partner designated as sender',
        string='Sender',
    )
    task_id = fields.Many2one(
        comodel_name='project.task',
        help='The task which this document is connected to',
        string='Task number',
    )

    @api.onchange('is_official', 'is_secret')
    def _onchange_official_document(self):
        if self.is_secret:
            self.is_official = True

    @api.model
    def create(self, vals):
        if vals.get('is_secret'):
            vals.update({'is_official': True})
        return super(IrAttachment, self).create(vals)

    def write(self, vals):
        if vals.get('is_secret'):
            _logger.warning(f'---write 1---{vals}')
            vals.update({'is_official': True})
        else:
            if self.is_secret and vals.get('is_official') is False:
                _logger.warning(f'---write 2---{vals}')
                raise ValidationError(
                    _('Cannot uncheck official document if it has a secrecy marker.'))

        return super(IrAttachment, self).write(vals)
