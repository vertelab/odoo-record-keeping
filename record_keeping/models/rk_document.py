from datetime import datetime
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import logging

from werkzeug.exceptions import default_exceptions

_logger = logging.getLogger(__name__)


class RecordKeepingDocument(models.Model):
    _name = 'rk.document'
    _description = 'Record-keeping Document'
    _inherit = ['mail.activity.mixin', 'mail.thread']

    name = fields.Char(
        default=lambda self: _('New')
    )
    draw_up_date = fields.Date(
        default=False,
        help='The date when the document is ready to be used or sent',
        string='Drawn up',
        tracking=True,
    )
    is_official = fields.Boolean(
        default=False,
        help='Check this option if this document is an official document',
        string='Official document',
        tracking=True,
    )
    is_secret = fields.Boolean(
        default=False,
        help='Check this option if it can be assumed that information contained '
             'in this document should not be disclosed on grounds of secrecy.',
        string='Secrecy marker',
        tracking=True,
    )
    law_section_id = fields.Many2one(
        comodel_name='rk.law.section',
        help='The specified secrecy provision when the document has a secrecy marker',
        string='Secrecy provision',
        tracking=True,
    )
    receive_date = fields.Date(
        default=False,
        help='The date when the document has been received by a competent person.',
        string='Received',
        tracking=True,
    )
    receiver_id = fields.Many2one(
        comodel_name='res.partner',
        string='Receiver',
        tracking=True,
    )
    secrecy_grounds = fields.Char(
        default=False,
        help='If marked as secret, please provide more information',
        string='Secrecy grounds',
        tracking=True,
    )
    sender_id = fields.Many2one(
        comodel_name='res.partner',
        help='A partner designated as sender',
        string='Sender',
        tracking=True,
    )

    @api.model
    def create(self, vals):
        if vals.get('is_official'):
            if vals.get('is_secret') and not vals.get('law_section_id'):
                raise ValidationError(_('Secrecy provision cannot be empty'))
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'rk.document') or vals['name']
        return super().create(vals)

    def write(self, vals):
        # if not vals.get('is_official', True):
        #     vals.update({'is_secret': False, 'law_section_id': False})
        # if not vals.get('is_secret', True):
        #     vals.update({'law_section_id': False})
        # if not vals.get('law_section_id', True) and self.is_secret:
        #     raise ValidationError(_('Secrecy provision cannot be empty'))

        _logger.warning(vals)
        if vals.get('is_official'):
            vals['name'] = self.env['ir.sequence'].next_by_code('rk.document') or vals['name']
        return super(RecordKeepingDocument, self).write(vals)
