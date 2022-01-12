# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class EventMatterWizard(models.TransientModel):
    _name = 'rk.wizard.event'
    _description = 'Wizard for attaching an event to a Record-keeping Matter'
    _inherit = ['rk.wizard']

    def _get_model(self):
        return self.env['event.event'].browse(self.env.context.get('active_ids'))

    model = fields.Many2one(
        comodel_name='event.event',
        default=_get_model,
        readonly=True,
    )
