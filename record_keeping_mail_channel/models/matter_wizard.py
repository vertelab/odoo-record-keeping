# -*- coding: utf-8 -*-

import logging
from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class EventMatterWizard(models.TransientModel):
    _name = 'rk.wizard.mailchannel'
    _description = 'Wizard for attaching an chat to a Record-keeping Matter'
    _inherit = ['rk.wizard']

    def _get_model(self):
        return self.env['mail.channel'].browse(self.env.context.get('active_ids'))

    model = fields.Many2one(
        comodel_name='mail.channel',
        default=_get_model,
        readonly=True,
    )
