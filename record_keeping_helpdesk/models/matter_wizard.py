# -*- coding: utf-8 -*-

import logging
from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class HelpDeskTicketMatterWizard(models.TransientModel):
    _name = 'rk.wizard.helpdeskticket'
    _description = 'Wizard for attaching an helpdesk to a Record-keeping Matter'
    _inherit = ['rk.wizard']

    def _get_model(self):
        return self.env['helpdesk.ticket'].browse(self.env.context.get('active_ids'))

    model = fields.Many2one(
        comodel_name='helpdesk.ticket',
        default=_get_model,
        readonly=True,
    )
