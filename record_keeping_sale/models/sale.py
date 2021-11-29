# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class Order(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order']
    _inherits = {'rk.document': 'document_id'}

    document_id = fields.Many2one(
        comodel_name='rk.document',
        help='The record-keeping document id',
        ondelete='restrict',
        readonly=True,
        required=True,
        string='Document',
    )
    document_ref = fields.Reference(
        compute='_compute_document_ref',
        help='The record-keeping document reference',
        readonly=True,
        selection='_selection_target_model',
        string='Document Reference',
    )

    @api.depends('document_id')
    def _compute_document_ref(self):
        for rec in self:
            rec.document_ref = f"rk.document,{rec.document_id.id or 0}"

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
    def _selection_target_model(self):
        models = self.env['ir.model'].search([('model', '=', 'rk.document')])
        return [(model.model, model.name) for model in models]

    @api.model
    def create(self, vals):
        record = super(Order, self).create(vals)
        vals = {'res_model': record._name, 'res_id': record.id}
        record.document_id = self.env['rk.document'].create(vals)
        return record
