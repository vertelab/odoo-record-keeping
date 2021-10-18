# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class Attachment(models.Model):
    _name = 'ir.attachment'
    _inherit = ['ir.attachment', 'mail.thread']
    _inherits = {'rk.document': 'rk_id'}

    rk_id = fields.Many2one(
        comodel_name='rk.document',
        help='The record-keeping document of this attachment',
        ondelete='restrict',
        required=True,
        readonly=True,
        string='Record-keeping Document',
    )

    rk_ref = fields.Reference(
        help='The record-keeping document of this attachment',
        readonly=True,
        selection='_selection_target_model',
        string='Registration Number',
    )

    @api.model
    def _selection_target_model(self):
        models = self.env['ir.model'].search([('model', '=', 'rk.document')])
        return [(model.model, model.name) for model in models]

    @api.onchange('is_official')
    def _onchange_is_official(self):
        if not self.is_official:
            self.is_secret = False

    @api.onchange('is_secret')
    def _onchange_is_secret(self):
        if not self.is_secret:
            self.law_section_id = False
            self.secrecy_grounds = False

    @api.model
    def create(self, vals):
        attachment = super(Attachment, self).create(vals)
        attachment.rk_ref = f'{attachment.rk_id._name},{attachment.rk_id.id}'
        attachment.rk_res_model = attachment._name
        attachment.rk_res_id = attachment.id
        return attachment
