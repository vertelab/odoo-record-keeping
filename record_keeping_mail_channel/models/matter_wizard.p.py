import logging
from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)

class EventMatterWizard(models.TransientModel):
    _name = 'rk.wizard.mailchannel'
    _description = 'Wizard for attaching an chat to a Record-keeping Matter'
    _inherit = ['rk.wizard']

    def _get_model(self):
        # #if VERSION <= "16.0"
        return self.env['mail.channel'].browse(self.env.context.get('active_ids'))
        # #elif VERSION >= "17.0"
        return self.env['discuss.channel'].browse(self.env.context.get('active_ids'))
        # #endif

    model = fields.Many2one(
        # #if VERSION <= "16.0"
        comodel_name='mail.channel',
        # #elif VERSION >= "17.0"
        comodel_name='discuss.channel',
        # #endif
        default=_get_model,
        readonly=True,
    )