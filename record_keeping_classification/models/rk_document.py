from odoo import models, fields

class RkDocument(models.Model):
    _inherit = 'rk.document'

    classification_id = fields.Many2one(
        related='matter_id.classification_id',
        readonly=True
    )
