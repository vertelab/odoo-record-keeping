from odoo import _, api, fields, models
import logging

_logger = logging.getLogger(__name__)


class RkMatter(models.Model):
    _inherit = 'rk.matter'

    def add_file_wizard_context(self):
        return {
            'default_rk_matter_id': self.id,
        }

    def action_add_file_wizard(self):
        return {
            'name': _('Wizard for adding a file to a matter'),
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'rk.add.file.wizard',
            'type': 'ir.actions.act_window',
            'context': self.add_file_wizard_context()
        }