# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class Property(models.Model):
    _name = 'property.property'
    _inherit = ['mail.thread', 'property.property']
    _inherits = {'rk.document': 'rk_id'}

    rk_id = fields.Many2one(
        comodel_name='rk.document',
        help='The record-keeping document of this property',
        ondelete='restrict',
        required=True,
        readonly=True,
        string='Record-keeping Document',
    )

    rk_ref = fields.Reference(
        help='The record-keeping document of this property',
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
        property = super(Property, self).create(vals)
        property.rk_ref = f'{property.rk_id._name},{property.rk_id.id}'
        property.rk_res_model = property._name
        property.rk_res_id = property.id
        return property
