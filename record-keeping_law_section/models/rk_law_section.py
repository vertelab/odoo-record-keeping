# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class RecordKeepingLawSection(models.Model):
    """
    In order for a public authority to refuse to disclose information in an of-
    ficial document to a natural or legal person, or any kind of information 
    to another public authority, in principle the information must be subject 
    to secrecy. The public authority must examine whether there is any secrecy 
    provision that may cover the information in question. If there is not, the 
    information is public in all circumstances and must be disclosed. 
    """
    _name = 'rk.law.section'
    _description = 'Record keeping law section. '
    _order = 'id desc'

    name = fields.Char()
    active = fields.Boolean(default=True)
    description = fields.Html()
    sequence = fields.Integer()
    url = fields.Char()


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'
    law_section_ids = fields.Many2many('rk.law.section')

    def write(self, vals):
        if vals.get('is_secret'):
            if not vals.get('law_section_ids'):
                raise ValidationError(_('Law Section is required when marking an official document as secret.'))
        else:
            vals.update({'law_section_ids': [(5, 0, 0)]})
        return super(IrAttachment, self).write(vals)
