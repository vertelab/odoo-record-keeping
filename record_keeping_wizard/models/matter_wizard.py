# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class MatterWizard(models.TransientModel):
    _name = "rk.wizard"
    _description = 'Wizard for attaching a record to a Record-keeping Matter'

    @property
    def model(self):
        raise NotImplementedError("Expects attribute 'model' to be implemented in inheritance.")

    def _get_model(self):
        raise NotImplementedError("Expects function '_get_model' to be implemented in inheritance.")

    # Remember: In inheritance, implement field 'model'
    matter_id = fields.Many2one(
        comodel_name='rk.matter',
        help='The matter this document belongs to',
        string='Matter',
    )
    is_official = fields.Boolean(
        default=True,
        help='Check this option if this document is an official document',
        string='Official document',
    )
    is_secret = fields.Boolean(
        default=False,
        help='Check this option if it can be assumed that information contained '
             'in this document should not be disclosed on grounds of secrecy.',
        string='Secrecy marker',
    )
    law_section_id = fields.Many2one(
        comodel_name='rk.law.section',
        help='The specified secrecy provision when the document has a secrecy marker',
        string='Secrecy provision',
    )
    secrecy_grounds = fields.Char(
        default=False,
        help='If marked as secret, please provide more information',
        string='Secrecy grounds',
    )

    def save_button(self):
        data = {
            'matter_id': self.matter_id,
            'is_official': self.is_official,
            'is_secret': False,
            'law_section_id': False,
            'secrecy_grounds': False,
        }

        if self.is_secret:
            data['is_secret'] = self.is_secret
            data['law_section_id'] = self.law_section_id
            data['secrecy_grounds'] = self.secrecy_grounds

        self.model.write(data)
